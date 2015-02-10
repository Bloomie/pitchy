from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class TagArtist(models.Model):

    artist = models.ForeignKey('Artist')
    tag = models.ForeignKey('Tag')


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    artists = models.ManyToManyField('Artist', through=TagArtist)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Artist(models.Model):

    name = models.CharField(max_length=128, unique=True)
    tags = models.ManyToManyField('Tag', through=TagArtist)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Artist, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

