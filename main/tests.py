from django.test import TestCase

from main.models import User, OneLiner, Vote
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


class WishListTests(TestCase):
    '''
    	- must be logged in to add a question
	- option to keep question anonymous
	- multiple possible answers
	- hide questions the owner marked answered
	- email notification triggered by an answer
	- show questions on profile
	- show answers on profile
	- edit question
	- delete question
	'''

# eof
