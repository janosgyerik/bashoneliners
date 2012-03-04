from django.test import TestCase

from main.models import *
from main.forms import *

class Util:
    @staticmethod
    def new_user(username):
	user = User(username=username)
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

    @staticmethod
    def new_question(user):
	question = Question(user=user)
	question.save()
	return question

    @staticmethod
    def new_answer(question, oneliner):
	answer = Answer(question=question, oneliner=oneliner)
	answer.save()
	return answer


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
	self.assertEquals(error_items[0][0], 'explanation')

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
	self.assertEquals(error_items[0][0], '__all__')


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
	results = OneLiner.search(self.get_form({ 'query': 'msummary' }))
	self.assertEquals(len(results), 1)
	self.assertEquals(results[0], self.msummary_oneliner)

	results = OneLiner.search(self.get_form({ 'query': 'msummary', 'match_summary': False }))
	self.assertEquals(len(results), 0)

    def test_match_line(self):
	results = OneLiner.search(self.get_form({ 'query': 'mline' }))
	self.assertEquals(len(results), 1)
	self.assertEquals(results[0], self.mline_oneliner)

	results = OneLiner.search(self.get_form({ 'query': 'mline', 'match_line': False }))
	self.assertEquals(len(results), 0)

    def test_match_explanation(self):
	results = OneLiner.search(self.get_form({ 'query': 'mexplanation' }))
	self.assertEquals(len(results), 1)
	self.assertEquals(results[0], self.mexplanation_oneliner)

	results = OneLiner.search(self.get_form({ 'query': 'mexplanation', 'match_explanation': False }))
	self.assertEquals(len(results), 0)

    def test_match_limitations(self):
	results = OneLiner.search(self.get_form({ 'query': 'mlimitations' }))
	self.assertEquals(len(results), 1)
	self.assertEquals(results[0], self.mlimitations_oneliner)

	results = OneLiner.search(self.get_form({ 'query': 'mlimitations', 'match_limitations': False }))
	self.assertEquals(len(results), 0)

    def test_match_whole_words(self):
	results = OneLiner.search(self.get_form({ 'query': 'vi', }))
	self.assertEquals(len(results), 2)

	results = OneLiner.search(self.get_form({ 'query': 'vi', 'match_whole_words': True }))
	self.assertEquals(len(results), 1)
	self.assertEquals(results[0], self.vi_oneliner)

    def test_match_nothing(self):
	form = SearchOneLinerForm(data={'query': 'NOTHINGSHOULDMATCH'})
	self.assertTrue(form.is_valid())
	results = OneLiner.search(form)
	self.assertEquals(len(results), 0)


class QuestionTests(TestCase):
    def setUp(self):
	self.user = Util.new_user('user1')

    def test_create_question(self):
	Util.new_question(self.user)

    def test_list_questions(self):
	self.assertTrue(Question.objects.all().count() == 0)
	Util.new_question(self.user)
	self.assertTrue(Question.objects.all().count() > 0)

    def test_list_questions_latestfirst(self):
	q1 = Util.new_question(self.user)
	q2 = Util.new_question(self.user)
	self.assertTrue(Question.objects.latest() == q2)

    def test_list_excludes_nonpublished(self):
	q1 = Util.new_question(self.user)
	q2 = Util.new_question(self.user)
	self.assertEquals(Question.latest(), q2)
	q2.is_published = False
	q2.save()
	self.assertNotEquals(Question.latest(), q2)

    def test_list_excludes_answered(self):
	q1 = Util.new_question(self.user)
	q2 = Util.new_question(self.user)
	self.assertEquals(Question.latest(), q2)
	q2.is_answered = True
	q2.save()
	self.assertNotEquals(Question.latest(), q2)

    def test_answer(self):
	q1 = Util.new_question(self.user)
	jack = Util.new_user('jack')
	o1 = Util.new_oneliner(jack, 'echo jack')
	a1 = Util.new_answer(q1, o1)

    def test_multiple_answers(self):
	q1 = Util.new_question(self.user)
	jack = Util.new_user('jack')
	o1 = Util.new_oneliner(jack, 'echo jack')
	a1 = Util.new_answer(q1, o1)
	mike = Util.new_user('mike')
	o2 = Util.new_oneliner(mike, 'echo mike')
	a2 = Util.new_answer(q1, o2)


class AcceptedAnswerTests(TestCase):
    def setUp(self):
	self.jack = Util.new_user('jack')
	self.oneliner = OneLiner(user=self.jack)
	self.oneliner.save()

	self.bill = Util.new_user('bill')
	OneLiner(user=self.bill).save()

	self.mike = Util.new_user('mike')
	self.question = Question(user=self.mike)
	self.question.save()

    def test_accept(self):
	self.assertEqual(AcceptedAnswer.objects.count(), 0)
	self.assertTrue(not self.question.is_answered)

	self.question.accept_answer(self.oneliner)
	self.assertTrue(self.question.is_answered)
	self.assertEqual(AcceptedAnswer.objects.count(), 1)

	self.question.accept_answer(self.oneliner)
	self.assertTrue(self.question.is_answered)
	self.assertEqual(AcceptedAnswer.objects.count(), 1)

    def test_accept_clear(self):
	self.test_accept()
	self.assertTrue(AcceptedAnswer.objects.count() > 0)
	self.assertTrue(self.question.is_answered)

	self.question.clear_all_answers()
	self.assertFalse(AcceptedAnswer.objects.count() > 0)
	self.assertFalse(self.question.is_answered)

    def test_clear_answers_when_is_answered_is_cleared(self):
	self.test_accept()
	self.assertTrue(AcceptedAnswer.objects.count() > 0)
	self.assertTrue(self.question.is_answered)

	self.question.is_answered = False
	self.question.save()
	self.assertFalse(AcceptedAnswer.objects.count() > 0)


# eof
