from django.conf.urls import patterns, url
from cherry import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^tags/$', views.tags, name='tags'),
                       url(r'^add_tag/$', views.add_tag, name='add_tag'),
                       url(r'^tags/(?P<tag_name_slug>[\w\d-]+)/$', views.tag, name='tag'),
                       url(r'^artists/$', views.artists, name='artists'),
                       url(r'artists/(?P<artist_name_slug>[\w\d-]+)/$', views.artist, name='artist'),
                       url(r'^add_artist/$', views.add_artist, name='add_artist'),
                       url(r'^tags/(?P<tag_name_slug>[\w\d-]+)/add_artist/$', views.add_artist_to_tag,
                           name='add_artist_to_tag'),
                       )
