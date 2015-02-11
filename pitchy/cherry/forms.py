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
    artists = forms.ModelMultipleChoiceField(queryset=Artist.objects.all())

    def save(self):
        instance = forms.ModelForm.save(self)
        for artist in self.cleaned_data['artists']:
            tag_art = TagArtist(artist=artist, tag=instance)
            tag_art.save()

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Tag
        fields = ('name',)


class ArtistForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter artist name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    def save(self):
        instance = forms.ModelForm.save(self)
        for tag in self.cleaned_data['tags']:
            tag_art = TagArtist(artist=instance, tag=tag)
            tag_art.save()

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Artist
        fields = ('name',)