from django.conf.urls import patterns, url

urlpatterns = patterns('oneliners.views',
        url(r'^$', 'oneliner_list', name='index'),
        (r'^sourcecode/$', 'sourcecode'),
        (r'^mission/$', 'mission'),
        (r'^feeds/$', 'feeds'),

        (r'^oneliner/$', 'oneliner_list'),
        url(r'^oneliner/(?P<pk>\d+)/$', 'oneliner', name='oneliner'),
        (r'^oneliner/edit/(?P<pk>\d+)/$', 'oneliner_edit'),
        (r'^oneliner/new/$', 'oneliner_new'),
        (r'^oneliner/new/question/(?P<question_pk>\d+)/$', 'oneliner_answer'),
        (r'^oneliner/new/alternative/(?P<oneliner_pk>\d+)/$', 'oneliner_alternative'),
        (r'^oneliner/comment/(?P<pk>\d+)/$', 'oneliner_comment'),

        (r'^profile/(?P<pk>\d+)/$', 'profile'),
        url(r'^profile/(?P<pk>\d+)/oneliners/$', 'profile_oneliners', name='profile_oneliners'),
        url(r'^profile/(?P<pk>\d+)/questions/$', 'profile_questions', name='profile_questions'),
        (r'^profile/$', 'profile'),
        (r'^profile/edit/$', 'profile_edit'),
        (r'^profile/oneliners/$', 'profile_oneliners'),
        (r'^profile/questions/$', 'profile_questions'),
        url(r'^profile/votes/$', 'profile_votes', name='profile_votes'),

        (r'^question/$', 'question_list'),
        (r'^question/(?P<pk>\d+)/$', 'question'),
        (r'^question/edit/(?P<pk>\d+)/$', 'question_edit'),
        (r'^question/new/$', 'question_new'),

        (r'^comment/$', 'comment_list'),

        (r'^search/$', 'search'),

        (r'^login/$', 'login'),
        (r'^logout/$', 'logout'),

        (r'^help/markdown/$', 'help_markdown'),
        )

urlpatterns += patterns('oneliners.ajax',
        (r'^ajax/question/(?P<question_pk>\d+)/answered_by/oneliner/(?P<oneliner_pk>\d+)/$', 'question_answered'),
        (r'^ajax/oneliner/(?P<oneliner_pk>\d+)/vote/$', 'oneliner_vote'),
        (r'^ajax/search/$', 'search'),
        (r'^ajax/search/tag/$', 'search_by_tag'),
        )

urlpatterns += patterns('oneliners.feeds',
        (r'^feeds/oneliner/$', 'oneliner'),
        (r'^feeds/question/$', 'question'),
        (r'^feeds/comment/$', 'comment'),
        )

# eof
