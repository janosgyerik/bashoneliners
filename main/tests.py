from django.test import TestCase

from main.models import Hacker, OneLiner, Vote

class Util:
    @staticmethod
    def new_hacker(username):
	hacker = Hacker(username=username)
	hacker.save()
	return hacker

    @staticmethod
    def new_oneliner(hacker, line):
	oneliner = OneLiner(hacker=hacker, line=line)
	oneliner.save()
	return oneliner

    @staticmethod
    def new_vote():
	pass


class VoteTests(TestCase):
    def setUp(self):
	self.jack = Util.new_hacker('jack')
	self.jacks_oneliner = Util.new_oneliner(self.jack, 'echo jack')

	self.mike = Util.new_hacker('mike')
	self.mikes_oneliner = Util.new_oneliner(self.mike, 'echo mike')

	self.frank = Util.new_hacker('frank')
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
	self.jack = Util.new_hacker('jack')
	self.jacks_oneliner = Util.new_oneliner(self.jack, 'echo jack')

	self.mike = Util.new_hacker('mike')
	self.mikes_oneliner = Util.new_oneliner(self.mike, 'echo mike')

    def test_top(self):
	u1 = Util.new_hacker('u1')
	u2 = Util.new_hacker('u2')
	u3 = Util.new_hacker('u3')

	self.jacks_oneliner.vote_up(u1)
	self.assertEquals(OneLiner.top()[0], self.jacks_oneliner)

	self.mikes_oneliner.vote_up(u1)
	self.mikes_oneliner.vote_up(u2)
	self.assertEquals(OneLiner.top()[0], self.mikes_oneliner)

	self.jacks_oneliner.vote_up(u2)
	self.jacks_oneliner.vote_up(u3)
	self.assertEquals(OneLiner.top()[0], self.jacks_oneliner)

	u4 = Util.new_hacker('u4')
	u5 = Util.new_hacker('u5')
	self.mikes_oneliner.vote_down(u4)
	self.mikes_oneliner.vote_down(u5)
	self.assertEquals(OneLiner.top()[0], self.jacks_oneliner)


# eof
