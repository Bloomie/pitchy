from django.shortcuts import render
from cherry.models import Tag, Artist
from cherry.forms import UserForm, UserProfileForm
from cherry.forms import TagForm, ArtistForm, ArtistToTagForm, TagArtist, TagToArtistForm
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    context_dict = {}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits
    return render(request, 'cherry/index.html')


def about(request):
    return render(request, 'cherry/about.html')


'''def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'cherry/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )'''


def tags(request):
    tag_list = Tag.objects.all()
    context_dict = {'tags': tag_list}
    return render(request, 'cherry/tags.html', context_dict)


def artists(request):
    artist_list = Artist.objects.all()
    context_dict = {'artists': artist_list}
    return render(request, 'cherry/artists.html', context_dict)

@login_required()
def add_tag(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = TagForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save()

            # Now call the index() view.
            # The user will be shown the homepage.
            return tags(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = TagForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'cherry/add_tag.html', {'form': form})


@login_required()
def add_artist(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = ArtistForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():

            # Save the new category to the database.
            form.save()

            # Now call the index() view.
            # The user will be shown the homepage.
            return artists(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = ArtistForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'cherry/add_artist.html', {'form': form})


def tag(request, tag_name_slug):
    tag = Tag.objects.get(slug=tag_name_slug)
    context_dict = {'name': tag.name}
    artists = Artist.objects.filter(tags=tag)
    context_dict['tag'] = tag
    context_dict['slug'] = tag_name_slug
    context_dict['artists'] = artists
    return render(request, 'cherry/tag.html', context_dict)


@login_required()
def add_artist_to_tag(request, tag_name_slug):
    # A HTTP POST?
    if request.method == 'POST':
        form = ArtistToTagForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():

            try:
                artist = Artist.objects.get(name=form.cleaned_data['name'])
            except:
                artist = Artist.objects.create(name=form.cleaned_data['name'])
            tag_art = TagArtist(artist=artist, tag=Tag.objects.get(slug=tag_name_slug))
            tag_art.save()
            # Save the new category to the database.

            # Now call the index() view.
            # The user will be shown the homepage.
            return tags(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = ArtistToTagForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'cherry/add_artist_to_tag.html', {'form': form, 'tag_name_slug': tag_name_slug})


@login_required()
def add_tag_to_artist(request, artist_name_slug):
    # A HTTP POST?
    if request.method == 'POST':
        form = TagToArtistForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():

            try:
                tag = Tag.objects.get(name=form.cleaned_data['name'])
            except:
                tag = Tag.objects.create(name=form.cleaned_data['name'])
            tag_art = TagArtist(artist=Artist.objects.get(slug=artist_name_slug), tag=tag)
            tag_art.save()
            # Save the new category to the database.

            # Now call the index() view.
            # The user will be shown the homepage.
            return artists(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = TagToArtistForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'cherry/add_tag_to_artist.html', {'form': form, 'artist_name_slug': artist_name_slug})



def artist(request, artist_name_slug):
    artist = Artist.objects.get(slug=artist_name_slug)
    context_dict = {'name': artist.name}
    tags = Tag.objects.filter(artists=artist)
    context_dict['artist'] = artist
    context_dict['slug'] = artist_name_slug
    context_dict['tags'] = tags
    return render(request, 'cherry/artist.html', context_dict)
