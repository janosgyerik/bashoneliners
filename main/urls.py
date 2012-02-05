from django.conf.urls.defaults import *

urlpatterns = patterns('bashoneliners.main.views',
    (r'^$', 'index'),
    (r'^sourcecode/$', 'sourcecode'),
    (r'^mission/$', 'mission'),

    (r'^oneliner/(?P<pk>\d+)/$', 'oneliner'),
    (r'^oneliner/edit/(?P<pk>\d+)/$', 'oneliner_edit'),
    (r'^oneliner/new/$', 'oneliner_new'),
    (r'^oneliner/new/question/(?P<question_pk>\d+)/$', 'oneliner_new'),

    (r'^profile/(?P<pk>\d+)/$', 'profile'),
    (r'^profile/$', 'profile'),
    (r'^profile/edit/$', 'profile_edit'),

    (r'^question/$', 'question_list'),
    (r'^question/(?P<pk>\d+)/$', 'question'),
    (r'^question/edit/(?P<pk>\d+)/$', 'question_edit'),
    (r'^question/new/$', 'question_new'),

    (r'^search/$', 'search'),

    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),

    (r'^help/markdown/$', 'help_markdown'),
)

urlpatterns += patterns('bashoneliners.main.ajax',
    (r'^ajax/markdown/$', 'markdown'),
    (r'^ajax/question/(?P<question_pk>\d+)/answered_by/oneliner/(?P<oneliner_pk>\d+)/$', 'question_answered'),
    (r'^ajax/search/$', 'search'),
)

# eof
