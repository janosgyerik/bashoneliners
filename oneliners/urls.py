from django.urls import path
from django.views.generic import RedirectView

from . import views, ajax

urlpatterns = [
    path('', views.oneliners_default, name='oneliners_default'),
    path('sourcecode/', views.sourcecode, name='sourcecode'),
    path('mission/', views.mission, name='mission'),
    path('feeds/', views.feeds, name='feeds'),

    path('newest/', views.oneliners_newest, name='oneliners_newest'),
    path('active/', views.oneliners_active, name='oneliners_active'),
    path('popular/', views.oneliners_popular, name='oneliners_popular'),
    path('tags/', views.oneliners_tags, name='oneliners_tags'),
    path('<int:pk>/', views.oneliner, name='oneliner'),
    path('<int:pk>/edit/', views.oneliner_edit, name='oneliner_edit'),
    path('<int:pk>/tweet/', views.oneliner_tweet, name='oneliner_tweet'),
    path('new/', views.oneliner_new, name='oneliner_new'),
    path('<int:oneliner_pk>/alternative/', views.oneliner_alternative, name='oneliner_alternative'),

    # legacy
    path('oneliner/', RedirectView.as_view(pattern_name='oneliners_default', permanent=True)),
    path('oneliner/newest/', RedirectView.as_view(pattern_name='oneliners_newest', permanent=True)),
    path('oneliner/popular/', RedirectView.as_view(pattern_name='oneliners_popular', permanent=True)),
    path('oneliner/<int:pk>/', RedirectView.as_view(pattern_name='oneliner', permanent=True)),

    path('users/<int:pk>/', views.profile, name='profile_of'),
    path('users/<int:pk>/oneliners/', views.profile_oneliners, name='profile_oneliners_of'),
    path('users/', views.profile, name='profile'),
    path('users/edit/', views.profile_edit, name='profile_edit'),
    path('users/oneliners/', views.profile_oneliners, name='profile_oneliners'),
    path('users/votes/', views.profile_votes, name='profile_votes'),

    path('search/', views.search, name='search'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('help/markdown/', views.help_markdown, name='help_markdown'),
]

urlpatterns += [
    path('ajax/oneliner/<int:oneliner_pk>/vote/', ajax.oneliner_vote, name='oneliner_vote'),
    path('ajax/search/', ajax.search, name='search_by_keyword'),
    path('ajax/search/tag/', ajax.search_by_tag, name='search_by_tag'),
]
