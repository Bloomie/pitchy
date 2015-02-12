from django import forms
from django.contrib.auth.models import User
from cherry.models import UserProfile, Tag, Artist, TagArtist


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class TagForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter tag name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    artists = forms.CharField(max_length=128, help_text="Please enter artists")

    def save(self):
        instance = forms.ModelForm.save(self)
        artists = [x.strip() for x in self.cleaned_data['artists'].split(',')]
        for artist in artists:
            try:
                artist = Artist.objects.get(name=artist)
            except:
                artist = Artist.objects.create(name=artist)
            tag_art = TagArtist(artist=Artist.objects.get(name=artist), tag=instance)
            tag_art.save()

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Tag
        fields = ('name',)


class ArtistForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter artist name")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    tags = forms.CharField(max_length=128, help_text="Please enter tags")

    def save(self):
        instance = forms.ModelForm.save(self)
        tags = [x.strip() for x in self.cleaned_data['tags'].split(',')]
        for tag in tags:
            try:
                tag = Tag.objects.get(name=tag)
            except:
                tag = Tag.objects.create(name=tag)
            tag_art = TagArtist(artist=instance, tag=Tag.objects.get(name=tag))
            tag_art.save()

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Artist
        fields = ('name',)


class ArtistToTagForm(forms.Form):
    name = forms.CharField(max_length=128, help_text="Please enter artist for this tag")


class TagToArtistForm(forms.Form):
    name = forms.CharField(max_length=128, help_text="Please Enter tag for this artist")