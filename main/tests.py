from django.test import TestCase

from main.models import User, OneLiner, Vote

class Util:
    @staticmethod
    def new_user(username):
	user = User(username=username)
	user.save()
	return user

    @staticmethod
    def new_oneliner(user, line):
	oneliner = OneLiner(user=user, line=line)
	oneliner.save()
	return oneliner

    @staticmethod
    def new_vote():
	pass


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


# eof
