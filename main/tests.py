from django.test import TestCase

from main.models import User, OneLiner, Vote, WishListQuestion, WishListAnswer
from main.forms import EditOneLinerForm, EditHackerProfileForm, EditUserForm

class Util:
    @staticmethod
    def new_user(username):
	user = User(username=username)
	user.save()
	return user

    @staticmethod
    def new_oneliner(user, line, summary=None, explanation=None):
	if summary is None:
	    summary = '(incorrectly omitted)'
	if explanation is None:
	    explanation = '(incorrectly omitted)'
	oneliner = OneLiner(user=user, line=line, summary=summary, explanation=explanation)
	oneliner.save()
	return oneliner

    @staticmethod
    def new_vote():
	pass

    @staticmethod
    def new_question(user):
	question = WishListQuestion(user=user)
	question.save()
	return question

    @staticmethod
    def new_answer(question, oneliner):
	answer = WishListAnswer(question=question, oneliner=oneliner)
	answer.save()
	return answer


class EditUserTests(TestCase):
    def setUp(self):
	self.jack = Util.new_user('jack')
	self.mike = Util.new_user('mike')

    def test_change_username(self):
	user0 = self.jack
	data = {}
	new_username = user0.username + '2'
	data['username'] = new_username

	form = EditUserForm(data, instance=user0)
	self.assertTrue(form.is_valid())
	user1 = form.save()

	self.assertEquals(user1.username, new_username)

    def test_duplicate_username_error(self):
	user0 = self.jack
	data = {}
	data['username'] = self.mike.username

	form = EditUserForm(data, instance=user0)
	self.assertFalse(form.is_valid())

	error_items = form.errors.items()
	self.assertEquals(len(error_items), 1)
	self.assertEquals(error_items[0][0], 'username')

    def test_change_password(self):
	user0 = self.jack
	data = {}
	data['username'] = user0.username
	new_password = 'newpass'
	data['password'] = new_password

	form = EditUserForm(data, instance=user0)
	#form.is_valid()
	#print form.errors.as_text()
	self.assertTrue(form.is_valid())
	user1 = form.save()
	self.assertTrue(user1.check_password(new_password))


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


class TopTests(TestCase):
    def setUp(self):
	self.jack = Util.new_user('jack')
	self.jacks_oneliner = Util.new_oneliner(self.jack, 'echo jack')

	self.mike = Util.new_user('mike')
	self.mikes_oneliner = Util.new_oneliner(self.mike, 'echo mike')

    def test_top(self):
	u1 = Util.new_user('u1')
	u2 = Util.new_user('u2')
	u3 = Util.new_user('u3')

	self.jacks_oneliner.vote_up(u1)
	self.assertEquals(OneLiner.top()[0], self.jacks_oneliner)

	self.mikes_oneliner.vote_up(u1)
	self.mikes_oneliner.vote_up(u2)
	self.assertEquals(OneLiner.top()[0], self.mikes_oneliner)

	self.jacks_oneliner.vote_up(u2)
	self.jacks_oneliner.vote_up(u3)
	self.assertEquals(OneLiner.top()[0], self.jacks_oneliner)

	u4 = Util.new_user('u4')
	u5 = Util.new_user('u5')
	self.mikes_oneliner.vote_down(u4)
	self.mikes_oneliner.vote_down(u5)
	self.assertEquals(OneLiner.top()[0], self.jacks_oneliner)


class SearchTests(TestCase):
    def setUp(self):
	self.jack = Util.new_user('jack')
	self.jacks_oneliner = Util.new_oneliner(self.jack, 'echo jack')

	self.mike = Util.new_user('mike')
	self.mikes_oneliner = Util.new_oneliner(self.mike, 'echo mike')

    def test_search(self):
	self.assertEquals(OneLiner.search('echo').count(), 2)
	self.assertEquals(OneLiner.search('echo jack').count(), 1)
	self.assertEquals(OneLiner.search('echo mike').count(), 1)
	self.assertEquals(OneLiner.search('jack')[0], self.jacks_oneliner)
	self.assertEquals(OneLiner.search('echo jack')[0], self.jacks_oneliner)
	self.assertEquals(OneLiner.search('echo mike')[0], self.mikes_oneliner)


class WishList(TestCase):
    def setUp(self):
	self.user = Util.new_user('user1')

    def test_create_question(self):
	Util.new_question(self.user)

    def test_list_questions(self):
	self.assertTrue(WishListQuestion.objects.all().count() == 0)
	Util.new_question(self.user)
	self.assertTrue(WishListQuestion.objects.all().count() > 0)

    def test_list_questions_latestfirst(self):
	q1 = Util.new_question(self.user)
	q2 = Util.new_question(self.user)
	self.assertTrue(WishListQuestion.objects.latest() == q2)

    def test_list_excludes_nonpublished(self):
	q1 = Util.new_question(self.user)
	q2 = Util.new_question(self.user)
	self.assertEquals(WishListQuestion.latest(), q2)
	q2.is_published = False
	q2.save()
	self.assertNotEquals(WishListQuestion.latest(), q2)

    def test_list_excludes_answered(self):
	q1 = Util.new_question(self.user)
	q2 = Util.new_question(self.user)
	self.assertEquals(WishListQuestion.latest(), q2)
	q2.is_answered = True
	q2.save()
	self.assertNotEquals(WishListQuestion.latest(), q2)

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


# eof
