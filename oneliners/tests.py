from django.test import TestCase, override_settings

from oneliners.models import Tag, OneLiner, User
from oneliners.forms import SearchOneLinerForm, EditOneLinerForm


class Util:
    @staticmethod
    def new_user(username):
        user = User(username=username)
        user.set_password(username)
        user.save()
        return user

    @staticmethod
    def new_oneliner(user, line, summary=None, explanation=None, limitations=None):
        if summary is None:
            summary = '(incorrectly omitted)'
        if explanation is None:
            explanation = '(incorrectly omitted)'
        if limitations is None:
            limitations = '(this is optional)'
        oneliner = OneLiner(user=user, line=line, summary=summary, explanation=explanation, limitations=limitations)
        oneliner.save()
        return oneliner

    @staticmethod
    def new_vote():
        pass


class EditOneLinerTests(TestCase):
    def setUp(self):
        self.jack = Util.new_user('jack')
        self.jacks_oneliner = Util.new_oneliner(self.jack, 'echo jack')

        self.frank = Util.new_user('frank')
        self.franks_oneliner = Util.new_oneliner(self.frank, 'echo frank')

    def test_save_own_success(self):
        oneliner0 = self.jacks_oneliner
        data = {
            'summary': oneliner0.summary,
            'line': oneliner0.line,
            'explanation': oneliner0.explanation,
            'action': EditOneLinerForm.action_save,
        }
        new_summary = oneliner0.summary + ' some change'
        data['summary'] = new_summary

        form = EditOneLinerForm(self.jack, data, instance=oneliner0)
        self.assertTrue(form.is_valid())
        oneliner1 = form.save()

        self.assertEquals(oneliner1.summary, new_summary)
        self.assertEquals(oneliner1.user, self.jack)

    def test_save_own_failure(self):
        oneliner0 = self.jacks_oneliner
        data = {
            'summary': oneliner0.summary,
            'line': oneliner0.line,
            'action': EditOneLinerForm.action_save,
        }
        new_summary = oneliner0.summary + ' some change'
        data['summary'] = new_summary

        form = EditOneLinerForm(self.jack, data, instance=oneliner0)
        self.assertFalse(form.is_valid())

        error_items = form.errors.items()
        self.assertEquals(len(error_items), 1)
        self.assertEquals(list(error_items)[0][0], 'explanation')

    def test_save_notown_failure(self):
        oneliner0 = self.jacks_oneliner
        data = {
            'summary': oneliner0.summary,
            'line': oneliner0.line,
            'explanation': oneliner0.explanation,
            'action': EditOneLinerForm.action_save,
        }

        form = EditOneLinerForm(self.frank, data, instance=self.jacks_oneliner)
        self.assertFalse(form.is_valid())

        error_items = form.errors.items()
        self.assertEquals(len(error_items), 1)
        self.assertEquals(list(error_items)[0][0], '__all__')


class VoteTests(TestCase):
    def setUp(self):
        self.jack = Util.new_user('jack')
        self.jacks_oneliner = Util.new_oneliner(self.jack, 'echo jack')

        self.mike = Util.new_user('mike')
        self.mikes_oneliner = Util.new_oneliner(self.mike, 'echo mike')

        self.frank = Util.new_user('frank')
        self.franks_oneliner = Util.new_oneliner(self.frank, 'echo frank')

    def test_multiple_vote_tolerance(self):
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 0)
        self.jacks_oneliner.vote_up(self.jack)
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 0)
        self.jacks_oneliner.vote_up(self.mike)
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 1)
        self.jacks_oneliner.vote_up(self.mike)
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 1)
        self.jacks_oneliner.vote_up(self.mike)
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 1)

    def test_vote_counts(self):
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 0)
        self.jacks_oneliner.vote_up(self.jack)
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 0)
        self.jacks_oneliner.vote_up(self.mike)
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 1)
        self.jacks_oneliner.vote_up(self.frank)
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 2)
        self.jacks_oneliner.vote_up(self.frank)
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 2)
        self.jacks_oneliner.vote_down(self.frank)
        self.assertEquals(self.jacks_oneliner.get_votes_up(), 1)
        self.assertEquals(self.jacks_oneliner.get_votes_down(), 1)
        self.assertEquals(self.jacks_oneliner.get_votes(), (1, 1))


class RecentTests(TestCase):
    def setUp(self):
        self.jack = Util.new_user('jack')
        self.jacks_oneliner = Util.new_oneliner(self.jack, 'echo jack')

        self.mike = Util.new_user('mike')
        self.mikes_oneliner = Util.new_oneliner(self.mike, 'echo mike')

    def xtest_recent(self):
        u1 = Util.new_user('u1')
        u2 = Util.new_user('u2')
        u3 = Util.new_user('u3')

        self.jacks_oneliner.vote_up(u1)
        self.assertEquals(OneLiner.recent()[0], self.jacks_oneliner)

        self.mikes_oneliner.vote_up(u1)
        self.mikes_oneliner.vote_up(u2)
        self.assertEquals(OneLiner.recent()[0], self.mikes_oneliner)

        self.jacks_oneliner.vote_up(u2)
        self.jacks_oneliner.vote_up(u3)
        self.assertEquals(OneLiner.recent()[0], self.jacks_oneliner)

        u4 = Util.new_user('u4')
        u5 = Util.new_user('u5')
        self.mikes_oneliner.vote_down(u4)
        self.mikes_oneliner.vote_down(u5)
        self.assertEquals(OneLiner.recent()[0], self.jacks_oneliner)


class SearchTests(TestCase):
    def setUp(self):
        self.jack = Util.new_user('jack')
        self.jacks_oneliner = Util.new_oneliner(self.jack, 'echo jack')

        self.mike = Util.new_user('mike')
        self.mikes_oneliner = Util.new_oneliner(self.mike, 'echo mike')

        self.vi_oneliner = Util.new_oneliner(self.mike, 'vi is an editor', summary='vi oneliner')
        self.video_oneliner = Util.new_oneliner(self.mike, 'mplayer is a video manipulator', summary='mplayer oneliner')

        self.mline_oneliner = Util.new_oneliner(self.jack, 'mline')
        self.msummary_oneliner = Util.new_oneliner(self.jack, '', summary='msummary')
        self.mexplanation_oneliner = Util.new_oneliner(self.jack, '', explanation='mexplanation')
        self.mlimitations_oneliner = Util.new_oneliner(self.jack, '', limitations='mlimitations')

    def test_simplesearch(self):
        self.assertEquals(OneLiner.simplesearch('echo').count(), 2)
        self.assertEquals(OneLiner.simplesearch('echo jack').count(), 1)
        self.assertEquals(OneLiner.simplesearch('echo mike').count(), 1)
        self.assertEquals(OneLiner.simplesearch('jack')[0], self.jacks_oneliner)
        self.assertEquals(OneLiner.simplesearch('echo jack')[0], self.jacks_oneliner)
        self.assertEquals(OneLiner.simplesearch('echo mike')[0], self.mikes_oneliner)

    def get_form(self, data):
        initial = {
            'match_summary': True,
            'match_line': True,
            'match_explanation': True,
            'match_limitations': True,
        }
        initial.update(data)
        form = SearchOneLinerForm(data=initial)
        self.assertTrue(form.is_valid())
        return form

    def test_match_summary(self):
        results = OneLiner.search(self.get_form({'query': 'msummary', }))
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0], self.msummary_oneliner)

        results = OneLiner.search(self.get_form({'query': 'msummary', 'match_summary': False, }))
        self.assertEquals(len(results), 0)

    def test_match_line(self):
        results = OneLiner.search(self.get_form({'query': 'mline', }))
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0], self.mline_oneliner)

        results = OneLiner.search(self.get_form({'query': 'mline', 'match_line': False, }))
        self.assertEquals(len(results), 0)

    def test_match_explanation(self):
        results = OneLiner.search(self.get_form({'query': 'mexplanation', }))
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0], self.mexplanation_oneliner)

        results = OneLiner.search(self.get_form({'query': 'mexplanation', 'match_explanation': False, }))
        self.assertEquals(len(results), 0)

    def test_match_limitations(self):
        results = OneLiner.search(self.get_form({'query': 'mlimitations', }))
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0], self.mlimitations_oneliner)

        results = OneLiner.search(self.get_form({'query': 'mlimitations', 'match_limitations': False, }))
        self.assertEquals(len(results), 0)

    def test_match_whole_words(self):
        results = OneLiner.search(self.get_form({'query': 'vi', }))
        self.assertEquals(len(results), 2)

        results = OneLiner.search(self.get_form({'query': 'vi', 'match_whole_words': True, }))
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0], self.vi_oneliner)

    def test_match_nothing(self):
        form = SearchOneLinerForm(data={'query': 'NOTHINGSHOULDMATCH'})
        self.assertTrue(form.is_valid())
        results = OneLiner.search(form)
        self.assertEquals(len(results), 0)


class TagTests(TestCase):
    def test_tag_generator(self):
        user = Util.new_user('jack')

        line = 'find grep xargs'
        oneliner = Util.new_oneliner(user, line)
        self.assertEquals({'xargs', 'grep', 'find'}, set(oneliner.get_tags()))

        line = '''find /etc -type f -print0 2>/dev/null | xargs -0 grep --color=AUTO -Hn 'nameserver' 2>/dev/null'''
        oneliner = Util.new_oneliner(user, line)
        self.assertEquals({'xargs', 'grep', 'find'}, set(oneliner.get_tags()))

        line = '''MAX=$(NUM=1;cat author.xml |perl -p -e 's/(Times Cited)/\n$1/g'|grep "Times Cited" |perl -p -e 's/^Times Cited:([0-9]*).*$/$1/g'|sort -nr | while read LINE; do if [ $LINE -ge $NUM ]; then echo "$NUM"; fi; NUM=$[$NUM+1]; done;); echo "$MAX"|tail -1'''
        oneliner = Util.new_oneliner(user, line)
        self.assertEquals(
                {u'sort', u'do', u'grep', u'then', u'read', u'tail', u'perl',
                 u'while', u'done', u'echo', u'fi', u'cat', u'if'}, set(oneliner.get_tags()))

    def test_tag_cloud(self):
        user = Util.new_user('jack')

        Util.new_oneliner(user, 'xargs find grep')
        Util.new_oneliner(user, 'xargs ls rm find')
        Util.new_oneliner(user, 'xargs xargs while sleep done do')

        tagcloud = Tag.tagcloud()
        tagcloud = tagcloud.values_list('text', 'count')
        dd = dict(tagcloud)
        self.assertEquals(3, dd['xargs'])
        self.assertEquals(3, dd.get('xargs'))
        self.assertFalse(dd.get('find'))  # occurs 2 times, which is < TAGCLOUD_MIN_COUNT
        self.assertFalse(dd.get('BLAH'))


class TweepyTests(TestCase):
    from oneliners.tweet import TWITTER_CREDENTIAL_KEYS

    @override_settings(TWITTER={k: 'nonempty' for k in TWITTER_CREDENTIAL_KEYS})
    def test_get_twitter_credentials_when_present(self):
        from oneliners.tweet import get_validated_twitter_credentials
        creds = get_validated_twitter_credentials()
        self.assertEquals(creds, {'access_token': 'nonempty', 'access_token_secret': 'nonempty',
                                  'consumer_key': 'nonempty', 'consumer_secret': 'nonempty'})

    @override_settings(TWITTER={'foo': 'bar'})
    def test_get_none_when_twitter_credentials_incomplete(self):
        from oneliners.tweet import get_validated_twitter_credentials
        self.assertIsNone(get_validated_twitter_credentials())


class OnelinerTweetTests(TestCase):
    def setUp(self):
        self.contributor = Util.new_user('contributor')
        self.oneliner = Util.new_oneliner(self.contributor, 'echo jack')

        self.nonstaff = Util.new_user('nonstaff')
        self.nonstaff.save()

        self.staff = Util.new_user('staff')
        self.staff.is_staff = True
        self.staff.save()

    def tweet_oneliner(self):
        return self.client.get('/oneliners/{}/tweet'.format(self.oneliner.pk))

    def test_anon_user_is_not_allowed(self):
        response = self.tweet_oneliner()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login'))

    def test_nonstaff_user_is_not_allowed(self):
        self.client.login(username=self.nonstaff.username, password='nonstaff')
        response = self.tweet_oneliner()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login'))

    def test_contributor_user_is_not_allowed(self):
        self.client.login(username=self.contributor.username, password='contributor')
        response = self.tweet_oneliner()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login'))

    def test_staff_is_allowed(self):
        self.client.login(username=self.staff.username, password='staff')
        response = self.tweet_oneliner()
        self.assertEqual(response.status_code, 200)
