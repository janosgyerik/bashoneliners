from django.urls import path
from django.views.generic.base import RedirectView

from . import views, ajax, feeds

urlpatterns = [
    path('', RedirectView.as_view(url='newest/', permanent=True), name='oneliners_default'),
    path('feeds/', views.feeds, name='feeds'),
    path('feeds/oneliners/', feeds.LatestOneLinersFeed(), name='latest_oneliners'),

    path('newest/', views.oneliners_newest, name='oneliners_newest'),
    path('active/', views.oneliners_active, name='oneliners_active'),
    path('popular/', views.oneliners_popular, name='oneliners_popular'),
    path('tags/', views.oneliners_tags, name='oneliners_tags'),
    path('categories/', views.oneliners_categories, name='oneliners_categories'),
    path('<int:pk>/', views.oneliner, name='oneliner'),
    path('<int:pk>/edit/', views.oneliner_edit, name='oneliner_edit'),
    path('<int:pk>/tweet/', views.oneliner_tweet, name='oneliner_tweet'),
    path('<int:pk>/unpublish/', views.oneliner_unpublish, name='oneliner_unpublish'),
    path('<int:pk>/snapshot/', views.oneliner_snapshot, name='oneliner_snapshot'),
    path('new/', views.oneliner_new, name='oneliner_new'),
    path('<int:oneliner_pk>/alternative/', views.oneliner_alternative, name='oneliner_alternative'),

    path('users/<int:pk>/', views.profile, name='profile_of'),
    path('users/<int:pk>/oneliners/', views.profile_oneliners, name='profile_oneliners_of'),
    path('users/<int:pk>/votes/', views.profile_votes_of, name='profile_votes_of'),
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
    path('ajax/search/category/', ajax.search_by_category, name='search_by_category'),
]
