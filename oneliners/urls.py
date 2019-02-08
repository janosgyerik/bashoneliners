from django.conf.urls import url
from django.views.generic import RedirectView

from oneliners import views, ajax

urlpatterns = [
    url(r'^$', views.oneliners_default, name='oneliners_default'),
    url(r'^sourcecode/$', views.sourcecode, name='sourcecode'),
    url(r'^mission/$', views.mission, name='mission'),
    url(r'^feeds/$', views.feeds, name='feeds'),

    url(r'^newest/$', views.oneliners_newest, name='oneliners_newest'),
    url(r'^popular/$', views.oneliners_popular, name='oneliners_popular'),
    url(r'^(?P<pk>\d+)/$', views.oneliner, name='oneliner'),
    url(r'^(?P<pk>\d+)/edit$', views.oneliner_edit, name='oneliner_edit'),
    url(r'^new/$', views.oneliner_new, name='oneliner_new'),
    url(r'^(?P<oneliner_pk>\d+)/alternative$', views.oneliner_alternative, name='oneliner_alternative'),

    # legacy
    url(r'^oneliner/$', RedirectView.as_view(pattern_name='oneliners_default', permanent=True)),
    url(r'^oneliner/newest/$', RedirectView.as_view(pattern_name='oneliners_newest', permanent=True)),
    url(r'^oneliner/popular/$', RedirectView.as_view(pattern_name='oneliners_popular', permanent=True)),
    url(r'^oneliner/(?P<pk>\d+)/$', RedirectView.as_view(pattern_name='oneliner', permanent=True)),

    url(r'^users/(?P<pk>\d+)/$', views.profile, name='profile_of'),
    url(r'^users/(?P<pk>\d+)/oneliners/$', views.profile_oneliners, name='profile_oneliners_of'),
    url(r'^users/$', views.profile, name='profile'),
    url(r'^users/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^users/oneliners/$', views.profile_oneliners, name='profile_oneliners'),
    url(r'^users/votes/$', views.profile_votes, name='profile_votes'),

    url(r'^search/$', views.search, name='search'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^help/markdown/$', views.help_markdown, name='help_markdown'),
]

urlpatterns += [
    url(r'^ajax/oneliner/(?P<oneliner_pk>\d+)/vote/$', ajax.oneliner_vote, name='oneliner_vote'),
    url(r'^ajax/search/$', ajax.search, name='search_by_keyword'),
    url(r'^ajax/search/tag/$', ajax.search_by_tag, name='search_by_tag'),
]
