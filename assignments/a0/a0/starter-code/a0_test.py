from elections import Election, Jurisdiction
from datetime import date
import unittest


class TestSetUp(unittest.TestCase):
    def test_basic(self):
        result = Election(date(2000, 1, 12))
        exp_date = date(2000, 1, 12)
        exp_riding = []
        exp_party = []
        exp_result = {}
        actual_date = result._d
        actual_riding = result._ridings
        actual_party = result._parties
        actual_result = result._results
        self.assertEqual(exp_date, actual_date)
        self.assertEqual(exp_riding, actual_riding)
        self.assertEqual(exp_party, actual_party)
        self.assertEqual(exp_result, actual_result)

    def test_basic_2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "liberal", 4)
        exp_date = date(2000, 1, 12)
        exp_riding = ["ez4"]
        exp_party = ["liberal"]
        exp_result = {"ez4": {"liberal": 4}}
        act_date = result._d
        act_riding = result._ridings
        act_party = result._parties
        act_result = result._results
        self.assertEqual(exp_date, act_date)
        self.assertEqual(exp_riding, act_riding)
        self.assertEqual(exp_party, act_party)
        self.assertEqual(exp_result, act_result)


class TestRiding(unittest.TestCase):
    def test_empty(self):
        result = Election(date(2000, 1, 12))
        exp_riding = []
        act_riding = result.ridings_of()
        self.assertEqual(exp_riding, act_riding)

    def test_one_riding(self):
        result = Election(date(2000, 11, 12))
        result.update_results("ez4", "", 1)
        exp_riding = ["ez4"]
        act_riding = result.ridings_of()
        self.assertEqual(exp_riding, act_riding)

    def test_duplicate_riding(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "", 2)
        result.update_results("ez4", "", 2)
        exp_riding = ["ez4"]
        act_riding = result.ridings_of()
        self.assertEqual(exp_riding, act_riding)

    def test_different_riding(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "", 3)
        result.update_results("ez5", "", 4)
        exp_riding = ["ez4", "ez5"]
        act_riding = result.ridings_of()
        self.assertCountEqual(exp_riding, act_riding)

    def test_random_combination(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "", 3)
        result.update_results("ez5", "", 4)
        result.update_results("ez6", "", 5)
        result.update_results("ez6", "", 5)
        result.update_results("ez5", "", 4)
        result.update_results("ez4", "", 3)
        exp_riding = ["ez4", "ez5", "ez6"]
        act_riding = result.ridings_of()
        self.assertCountEqual(exp_riding, act_riding)


class TestRead(unittest.TestCase):
    # TODO
    pass


class TestResultsFor(unittest.TestCase):
    def test_none(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "", 1)
        exp_result = None
        act_result = result.results_for("r1", "liberal")
        self.assertEqual(exp_result, act_result)

    def test_none_2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 1)
        exp_result = None
        act_result = result.results_for("ez4", "math")
        self.assertEqual(exp_result, act_result)

    def test_regular(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 1)
        exp_result = 1
        act_result = result.results_for("ez4", "cs")
        self.assertEqual(exp_result, act_result)

    def test_regular2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 1)
        result.update_results("ez4", "cs", 4)
        exp_result = 5
        act_result = result.results_for("ez4", "cs")
        self.assertEqual(exp_result, act_result)

    def test_regular3(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 1)
        result.update_results("ez4", "math", 3)
        exp_result = 3
        act_result = result.results_for("ez4", "math")
        self.assertEqual(exp_result, act_result)

    def test_doc_example(self):
        e = Election(date(2000, 2, 8))
        e.update_results('r1', 'ndp', 1234)
        e.update_results('r1', 'lib', 1345)
        e.update_results('r1', 'pc', 1456)
        e.update_results('r2', 'pc', 1)
        act_1 = e.results_for('r1', 'pc')
        exp_1 = 1456
        act_2 = e.results_for('r2', 'pc')
        exp_2 = 1
        self.assertEqual(exp_1, act_1)
        self.assertEqual(exp_2, act_2)


class TestRidingWinner(unittest.TestCase):
    def test_single_party(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        exp_result = ["cs"]
        act_result = result.riding_winners("ez4")
        self.assertListEqual(exp_result, act_result)

    def test_single_winner(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 6)
        exp_result = ["math"]
        act_result = result.riding_winners("ez4")
        self.assertListEqual(exp_result, act_result)

    def test_single_winner_2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 6)
        result.update_results("ez4", "cs", 3)
        exp_result = ["cs"]
        act_result = result.riding_winners("ez4")
        self.assertListEqual(exp_result, act_result)

    def test_tie(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 5)
        exp_result = ["cs", "math"]
        act_result = result.riding_winners("ez4")
        self.assertCountEqual(exp_result, act_result)

    def test_tie_2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 5)
        result.update_results("ez4", "eco", 4)
        exp_result = ["cs", "math"]
        act_result = result.riding_winners("ez4")
        self.assertCountEqual(exp_result, act_result)

    def test_tie_3(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 6)
        result.update_results("ez4", "cs", 1)
        result.update_results("ez4", "eco", 6)
        exp_result = ["cs", "math", "eco"]
        act_result = result.riding_winners("ez4")
        self.assertCountEqual(exp_result, act_result)

    def test_multiple_riding(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 6)
        result.update_results("ez5", "cs", 4)
        exp_result = ["cs"]
        act_result = result.riding_winners("ez5")
        self.assertCountEqual(exp_result, act_result)

    def test_multiple_riding2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 6)
        result.update_results("ez5", "cs", 2)
        result.update_results("ez5", "math", 2)
        exp_result = ["math", "cs"]
        act_result = result.riding_winners("ez5")
        self.assertCountEqual(exp_result, act_result)


class TestPopularVote(unittest.TestCase):
    def test_single_riding(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        exp_result = {"cs": 5}
        act_result = result.popular_vote()
        self.assertDictEqual(exp_result, act_result)

    def test_single_riding_2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 6)
        exp_result = {"math": 6, "cs": 5}
        act_result = result.popular_vote()
        self.assertDictEqual(exp_result, act_result)

    def test_single_riding_3(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 6)
        result.update_results("ez4", "cs", 1)
        exp_result = {"cs": 6, "math": 6}
        act_result = result.popular_vote()
        self.assertDictEqual(exp_result, act_result)

    def test_multiple_riding(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez5", "cs", 6)
        exp_result = {"cs": 11}
        act_result = result.popular_vote()
        self.assertDictEqual(exp_result, act_result)

    def test_multiple_riding_2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez5", "eco", 6)
        exp_result = {"cs": 5, "eco": 6}
        act_result = result.popular_vote()
        self.assertDictEqual(exp_result, act_result)

    def test_multiple_riding_3(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "eco", 11)
        result.update_results("ez5", "cs", 6)
        result.update_results("ez6", "math", 20)
        exp_result = {"cs": 11, "eco": 11, "math": 20}
        act_result = result.popular_vote()
        self.assertDictEqual(exp_result, act_result)


class TestPartySeats(unittest.TestCase):
    def test_single_riding(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        exp_result = {"cs": 1}
        act_result = result.party_seats()
        self.assertDictEqual(exp_result, act_result)

    def test_single_riding_2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "eco", 3)
        exp_result = {"cs": 1, "eco": 0}
        act_result = result.party_seats()
        self.assertDictEqual(exp_result, act_result)

    def test_single_riding_tie(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "eco", 5)
        exp_result = {"cs": 0, "eco": 0}
        act_result = result.party_seats()
        self.assertDictEqual(exp_result, act_result)

    def test_multiple_riding(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez5", "cs", 6)
        exp_result = {"cs": 2}
        act_result = result.party_seats()
        self.assertDictEqual(exp_result, act_result)

    def test_multiple_riding_2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 6)
        result.update_results("ez5", "eco", 6)
        exp_result = {"cs": 0, "eco": 1, "math": 1}
        act_result = result.party_seats()
        self.assertDictEqual(exp_result, act_result)

    def test_multiple_riding_3(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez5", "eco", 6)
        result.update_results("ez6", "math", 7)
        exp_result = {"cs": 1, "eco": 1, "math": 1}
        act_result = result.party_seats()
        self.assertDictEqual(exp_result, act_result)

    def test_multiple_riding_4(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "math", 6)
        result.update_results("ez4", "eco", 2)
        result.update_results("ez5", "cs", 6)
        result.update_results("ez5", "math", 4)
        result.update_results("ez5", "ls", 2)
        result.update_results("ez5", "math", 2)
        exp_result = {"cs": 0, "math": 1, "eco": 0, "ls": 0}
        act_result = result.party_seats()
        self.assertDictEqual(exp_result, act_result)

    def test_multiple_riding_tie(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 6)
        result.update_results("ez4", "math", 6)
        result.update_results("ez4", "eco", 2)
        result.update_results("ez5", "cs", 4)
        result.update_results("ez5", "ls", 4)
        result.update_results("ez5", "math", 2)
        exp_result = {"cs": 0, "math": 0, "eco": 0, "ls": 0}
        act_result = result.party_seats()
        self.assertDictEqual(exp_result, act_result)


class TestElectionWinners(unittest.TestCase):
    def test_empty(self):
        result = Election(date(2000, 1, 12))
        exp_result = []
        act_result = result.election_winners()
        self.assertCountEqual(exp_result, act_result)

    def test_single_riding(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        exp_result = ["cs"]
        act_result = result.election_winners()
        self.assertCountEqual(exp_result, act_result)

    def test_single_riding_2(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "eco", 6)
        exp_result = ["eco"]
        act_result = result.election_winners()
        self.assertCountEqual(exp_result, act_result)

    def test_single_riding_tie(self):
        result = Election(date(2000, 1, 12))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "eco", 5)
        exp_result = ["cs", "eco"]
        act_result = result.election_winners()
        self.assertCountEqual(exp_result, act_result)

    def test_multiple_riding(self):
        result = Election(date(2000, 1, 13))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "eco", 6)
        result.update_results("ez4", "ls", 7)
        result.update_results("ez4", "cs", 3)
        result.update_results("ez5", "cs", 8)
        result.update_results("ez5", "eco", 9)
        result.update_results("ez6", "cs", 3)
        result.update_results("ez6", "ls", 7)
        exp_result = ["cs", "eco", "ls"]
        act_result = result.election_winners()
        self.assertEqual(sorted(exp_result), sorted(act_result))

    def test_multiple_tie_1(self):
        result = Election(date(2000, 1, 13))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "eco", 6)
        result.update_results("ez4", "ls", 8)
        result.update_results("ez4", "cs", 3)
        result.update_results("ez5", "cs", 8)
        result.update_results("ez5", "eco", 8)
        result.update_results("ez6", "cs", 3)
        result.update_results("ez6", "ls", 3)
        exp_result = ["cs", "eco", "ls"]
        act_result = result.election_winners()
        self.assertEqual(sorted(exp_result), sorted(act_result))


    def test_multiple_tie_2(self):
        result = Election(date(2000, 1, 13))
        result.update_results("ez4", "cs", 5)
        result.update_results("ez4", "eco", 6)
        result.update_results("ez4", "ls", 8)
        result.update_results("ez4", "cs", 3)
        result.update_results("ez5", "cs", 8)
        result.update_results("ez5", "eco", 8)
        result.update_results("ez6", "cs", 3)
        result.update_results("ez6", "ls", 7)
        exp_result = ["ls"]
        act_result = result.election_winners()
        self.assertEqual(sorted(exp_result), sorted(act_result))


class TestJurisdiction(unittest.TestCase):
    def test_setup(self):
        res = Jurisdiction("ez4")
        exp_name = "ez4"
        act_name = res._name
        exp_history = {}
        act_history = res._history
        self.assertCountEqual(exp_name, act_name)
        self.assertEqual(exp_history, act_history)

    def test_setup_2(self):
        res = Jurisdiction("")
        exp_name = ""
        act_name = res._name
        elec = Election(date(2000, 12,2))
        res._history[date(2000, 12, 2)] = elec
        exp_history = {date(2000, 12, 2):elec}
        act_history = res._history
        self.assertEqual(exp_name, act_name)
        self.assertDictEqual(exp_history, act_history)


class TestPartyWins(unittest.TestCase):
    def test_single_election(self):
        e = Election(date(2000, 11, 12))
        e.update_results("ez4", "cs", 10)
        res = Jurisdiction("ez4")
        res._history[date(2000, 11, 20)] = e
        exp_res = [date(2000, 11, 20)]
        act_res = res.party_wins("cs")
        self.assertCountEqual(exp_res, act_res)

    def test_single_election_2(self):
        e = Election(date(2000, 11, 12))
        e.update_results("ez4", "cs", 10)
        res = Jurisdiction("ez4")
        res._history[date(2000, 11, 20)] = e
        exp_res = []
        act_res = res.party_wins("math")
        self.assertCountEqual(exp_res, act_res)

    def test_single_election_3(self):
        e = Election(date(2000, 11, 12))
        e.update_results("ez4", "cs", 10)
        e.update_results("ez4", "math", 20)
        res = Jurisdiction("ez4")
        res._history[date(2000, 11, 20)] = e
        exp_res = []
        act_res = res.party_wins("cs")
        self.assertCountEqual(exp_res, act_res)

    def test_single_election_tie(self):
        e = Election(date(2000, 11, 12))
        e.update_results("ez4", "cs", 10)
        e.update_results("ez4", "math", 10)
        res = Jurisdiction("ez4")
        res._history[date(2000, 11, 20)] = e
        exp_res = [date(2000, 11, 20)]
        act_res = res.party_wins("math")
        self.assertCountEqual(exp_res, act_res)

    def test_single_election_tie_2(self):
        e = Election(date(2000, 11, 12))
        e.update_results("ez4", "cs", 10)
        e.update_results("ez4", "math", 9)
        e.update_results("ez5", "cs", 9)
        e.update_results("ez5", "math", 10)
        res = Jurisdiction("ez4")
        res._history[date(2000, 11, 20)] = e
        exp_res = [date(2000,11, 20)]
        act_res = res.party_wins("math")
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election(self):
        e = Election(date(2000, 11, 23))
        e.update_results("ez4", "cs", 20)
        e.update_results("ez4", "math", 10)
        e.update_results("ez4", "eco", 15)
        e2= Election(date(2000, 11, 12))
        e2.update_results("ez4", "cs", 30)
        e2.update_results("ez4", "math", 60)
        res = Jurisdiction("")
        res._history[date(2001, 11, 21)] = e
        res._history[date(2002, 12, 12)] = e2
        exp_res = [date(2001, 11, 21)]
        act_res = res.party_wins("cs")
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_2(self):
        e = Election(date(2000, 11, 23))
        e.update_results("ez4", "cs", 20)
        e.update_results("ez4", "math", 10)
        e.update_results("ez4", "eco", 15)
        e2 = Election(date(2000, 11, 12))
        e2.update_results("ez4", "cs", 30)
        e2.update_results("ez4", "math", 20)
        res = Jurisdiction("")
        res._history[date(2001, 11, 21)] = e
        res._history[date(2002, 12, 12)] = e2
        exp_res = [date(2001, 11, 21), date(2002, 12, 12)]
        act_res = res.party_wins("cs")
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_tie(self):
        e = Election(date(2000, 11, 23))
        e.update_results("ez4", "cs", 10)
        e.update_results("ez4", "math", 10)
        e.update_results("ez4", "eco", 10)
        e.update_results("ez5", "cs", 10)
        e.update_results("ez5", "math", 10)
        e2 = Election(date(2000, 11, 12))
        e2.update_results("ez4", "cs", 30)
        e2.update_results("ez4", "math", 30)
        res = Jurisdiction("")
        res._history[date(2001, 11, 21)] = e
        res._history[date(2002, 12, 12)] = e2
        exp_res = [date(2001, 11, 21), date(2002, 12, 12)]
        act_res = res.party_wins("cs")
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_tie_2(self):
        e = Election(date(2000, 11, 23))
        e.update_results("ez4", "cs", 10)
        e.update_results("ez4", "math", 20)
        e.update_results("ez4", "eco", 15)
        e.update_results("ez5", "cs", 15)
        e.update_results("ez5", "math", 10)
        e.update_results("ez6", "eco", 10)
        e2 = Election(date(2000, 11, 12))
        e2.update_results("ez4", "cs", 30)
        e2.update_results("ez4", "math", 30)
        res = Jurisdiction("")
        res._history[date(2001, 11, 21)] = e
        res._history[date(2002, 12, 12)] = e2
        exp_res = [date(2001, 11, 21), date(2002, 12, 12)]
        act_res = res.party_wins("cs")
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_tie_3(self):
        e = Election(date(2000, 11, 23))
        e.update_results("ez4", "cs", 10)
        e.update_results("ez4", "math", 20)
        e.update_results("ez4", "eco", 15)
        e.update_results("ez5", "cs", 15)
        e.update_results("ez5", "math", 10)
        e.update_results("ez6", "eco", 10)
        e.update_results("ez6", "cs", 5)
        e2 = Election(date(2000, 11, 12))
        e2.update_results("ez4", "cs", 10)
        e2.update_results("ez4", "math", 30)
        res = Jurisdiction("")
        res._history[date(2001, 11, 21)] = e
        res._history[date(2002, 12, 12)] = e2
        exp_res = [date(2001, 11, 21)]
        act_res = res.party_wins("cs")
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_tie_4(self):
        e = Election(date(2000, 11, 23))
        e.update_results("ez4", "cs", 10)
        e.update_results("ez4", "math", 20)
        e.update_results("ez4", "eco", 15)
        e.update_results("ez5", "cs", 15)
        e.update_results("ez5", "math", 10)
        e.update_results("ez6", "eco", 10)
        e.update_results("ez6", "cs", 5)
        e2 = Election(date(2000, 11, 12))
        e2.update_results("ez4", "cs", 10)
        e2.update_results("ez4", "math", 30)
        e2.update_results("ez5", "cs", 20)
        e2.update_results("ez5", "math", 10)
        res = Jurisdiction("")
        res._history[date(2001, 11, 21)] = e
        res._history[date(2002, 12, 12)] = e2
        exp_res = [date(2001, 11, 21), date(2002, 12, 12)]
        act_res = res.party_wins("cs")
        self.assertCountEqual(exp_res, act_res)

    def test_doc_example(self):
        e1 = Election(date(2000, 2, 8))
        e1.update_results('r1', 'ndp', 1)
        e1.update_results('r1', 'lib', 2)
        e1.update_results('r1', 'pc', 3)
        e1.update_results('r2', 'lib', 10)
        e1.update_results('r2', 'pc', 20)
        e1.update_results('r3', 'ndp', 200)
        e1.update_results('r3', 'pc', 100)
        e2 = Election(date(2004, 5, 16))
        e2.update_results('r1', 'ndp', 10)
        e2.update_results('r1', 'lib', 20)
        e2.update_results('r2', 'lib', 50)
        e2.update_results('r2', 'pc', 5)
        e3 = Election(date(2008, 6, 1))
        e3.update_results('r1', 'ndp', 101)
        e3.update_results('r1', 'lib', 102)
        e3.update_results('r2', 'ndp', 1001)
        e3.update_results('r2', 'lib', 1002)
        j = Jurisdiction('Canada')
        j._history[date(2000, 2, 8)] = e1
        j._history[date(2003, 5, 16)] = e2
        j._history[date(2003, 6, 1)] = e3
        exp_res = [date(2003, 5, 16), date(2003, 6, 1)]
        act_res = j.party_wins("lib")
        self.assertCountEqual(exp_res, act_res)

class TestPartyHistory(unittest.TestCase):
    def test_single_election(self):
        e = Election(date(2000, 11, 21))
        e.update_results("ez4", "cs", 20)
        e.update_results("ez4", "math", 30)
        e.update_results("ez4", "eco", 50)
        j = Jurisdiction("")
        j._history[date(2011, 11, 21)] = e
        exp_res = {date(2011, 11, 21): 0.2}
        act_res = j.party_history("cs")
        self.assertDictEqual(exp_res, act_res)

    def test_empty_party(self):
        e = Election(date(2000, 11, 21))
        e.update_results("ez4", "cs", 20)
        e.update_results("ez4", "math", 30)
        e.update_results("ez4", "eco", 50)
        j = Jurisdiction("")
        j._history[date(2011, 11, 21)] = e
        exp_res = {date(2011, 11, 21): 0.0}
        act_res = j.party_history("ls")
        self.assertDictEqual(exp_res, act_res)

    def test_multiple_election(self):
        e = Election(date(2000, 11, 21))
        e.update_results("ez4", "cs", 20)
        e.update_results("ez4", "math", 30)
        e.update_results("ez4", "eco", 50)
        e2 = Election(date(2011, 12, 20))
        e2.update_results("ez4", "cs", 30)
        e2.update_results("ez4", "math", 60)
        e2.update_results("ez5", "cs", 10)
        j = Jurisdiction("")
        j._history[date(2011, 11, 21)] = e
        j._history[date(2014, 1,2)] = e2
        exp_res = {date(2011, 11, 21): 0.2, date(2014,1,2):0.4}
        act_res = j.party_history("cs")
        self.assertDictEqual(exp_res, act_res)

    def test_multiple_election_2(self):
        e = Election(date(2000, 11, 21))
        e.update_results("ez4", "cs", 20)
        e.update_results("ez4", "math", 30)
        e.update_results("ez4", "eco", 50)
        e2 = Election(date(2011, 12, 20))
        e2.update_results("ez4", "cs", 30)
        e2.update_results("ez4", "math", 60)
        e2.update_results("ez5", "cs", 10)
        j = Jurisdiction("")
        j._history[date(2011, 11, 21)] = e
        j._history[date(2014, 1, 2)] = e2
        exp_res = {date(2011, 11, 21): 0.0, date(2014, 1, 2): 0.0}
        act_res = j.party_history("ls")
        self.assertDictEqual(exp_res, act_res)

    def test_multiple_election_3(self):
        e = Election(date(2000, 11, 21))
        e.update_results("ez4", "cs", 20)
        e.update_results("ez4", "math", 30)
        e.update_results("ez5", "eco", 50)
        e2 = Election(date(2011, 12, 20))
        e2.update_results("ez4", "cs", 30)
        e2.update_results("ez4", "math", 60)
        e2.update_results("ez5", "cs", 10)
        j = Jurisdiction("")
        j._history[date(2011, 11, 21)] = e
        j._history[date(2014, 1, 2)] = e2
        exp_res = {date(2011, 11, 21): 0.5, date(2014, 1, 2): 0.0}
        act_res = j.party_history("eco")
        self.assertDictEqual(exp_res, act_res)

    def test_doc_example(self):
        j = Jurisdiction('Canada')
        e1 = Election(date(2000, 2, 8))
        e1.update_results('r1', 'ndp', 1)
        e1.update_results('r1', 'lib', 2)
        e1.update_results('r1', 'pc', 3)
        e1.update_results('r2', 'pc', 4)
        e1.update_results('r2', 'lib', 5)
        e1.update_results('r2', 'green', 6)
        e1.update_results('r2', 'ndp', 7)
        j._history[date(2000, 2, 8)] = e1
        e2 = Election(date(2004, 5, 16))
        e2.update_results('r1', 'ndp', 40)
        e2.update_results('r1', 'lib', 5)
        e2.update_results('r2', 'lib', 10)
        e2.update_results('r2', 'pc', 20)
        j._history[date(2004, 5, 16)] = e2
        exp_res = {date(2000, 2, 8): 0.25,date(2004, 5, 16): 0.2}
        act_res = j.party_history("lib")
        self.assertDictEqual(exp_res, act_res)

class TestRidingChanges(unittest.TestCase):
    def test_single_election_single_riding(self):
        j = Jurisdiction('Canada')
        e1 = Election(date(2000, 2, 8))
        e1.update_results('r1', 'ndp', 1)
        j._history[date(2011, 11, 21)] = e1
        exp_res = []
        act_res = j.riding_changes()
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_1(self):
        j = Jurisdiction('Canada')
        e1 = Election(date(2000, 2, 8))
        e1.update_results('ez4', 'cs', 1)
        e2 = Election(date(2011, 12, 21))
        e2.update_results("ez4", "", 1)
        j._history[date(2011, 11, 21)] = e1
        j._history[date(2001, 12, 22)] = e2
        exp_res = [(set(), set())]
        act_res = j.riding_changes()
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_2(self):
        j = Jurisdiction('Canada')
        e1 = Election(date(2000, 2, 8))
        e1.update_results('ez4', 'cs', 1)
        e2 = Election(date(2011, 12, 21))
        e2.update_results("ez5", "", 1)
        j._history[date(2011, 11, 21)] = e1
        j._history[date(2012, 11,11)] = e2
        exp_res = [({"ez4"}, {"ez5"})]
        act_res = j.riding_changes()
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_3(self):
        j = Jurisdiction('Canada')
        e1 = Election(date(2000, 2, 8))
        e1.update_results('ez4', 'cs', 1)
        e1.update_results("ez5", "cs", 2)
        e2 = Election(date(2011, 12, 21))
        e2.update_results("ez5", "", 1)
        j._history[date(2011, 11, 21)] = e1
        j._history[date(2012, 11, 11)] = e2
        exp_res = [({"ez4"}, set())]
        act_res = j.riding_changes()
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_4(self):
        j = Jurisdiction('Canada')
        e1 = Election(date(2000, 2, 8))
        e1.update_results('ez4', 'cs', 1)
        e2 = Election(date(2011, 12, 21))
        e2.update_results("ez4", "cs", 1)
        e2.update_results("ez5", "", 1)
        j._history[date(2011, 11, 21)] = e1
        j._history[date(2012, 11, 11)] = e2
        exp_res = [(set(), {"ez5"})]
        act_res = j.riding_changes()
        self.assertCountEqual(exp_res, act_res)

    def test_multiple_election_5(self):
        j = Jurisdiction('Canada')
        e1 = Election(date(2000, 2, 8))
        e1.update_results('r1', 'ndp', 1)
        e1.update_results('r1', 'lib', 1)
        e1.update_results('r1', 'pc', 1)
        e1.update_results('r2', 'pc', 1)
        e1.update_results('r2', 'lib', 1)
        e1.update_results('r2', 'green', 1)
        e1.update_results('r2', 'ndp', 1)
        j._history[date(2000, 2, 8)] = e1
        e2 = Election(date(2004, 5, 16))
        e2.update_results('r1', 'ndp', 1)
        e2.update_results('r3', 'pc', 1)
        j._history[date(2004, 5, 16)] = e2
        act_res = j.riding_changes()
        exp_res = [({'r2'}, {'r3'})]
        self.assertCountEqual(exp_res, act_res)


    def test_multiple_election_6(self):
        j = Jurisdiction('Canada')
        e1 = Election(date(2000, 2, 8))
        e1.update_results('ez4', 'ndp', 1)
        e1.update_results('ez5', 'lib', 1)
        e1.update_results('ez6', 'pc', 1)
        e2 = Election(date(2012, 12,12))
        e2.update_results('ez8', 'pc', 1)
        e2.update_results('ez6', 'lib', 1)
        e2.update_results('ez7', 'green', 1)
        e3 = Election(date(2011, 1,23))
        e3.update_results('ez6', 'lib', 1)
        e3.update_results('ez7', 'green', 1)
        e3.update_results('ez8', 'ndp', 1)
        j._history[date(2000, 2, 8)] = e1
        e4 = Election(date(2004, 5, 16))
        e4.update_results('ez6', 'lib', 1)
        e4.update_results('ez5', 'green', 1)
        e4.update_results('ez8', 'ndp', 1)
        j._history[date(2001, 5, 16)] = e2
        j._history[date(2001, 12,22)] = e3
        j._history[date(2002, 11, 21)] = e4
        act_res = j.riding_changes()
        exp_res = [({'ez4', 'ez5'}, {'ez7','ez8'}),  (set(), set()), ({"ez7"}, {"ez5"})]
        self.assertCountEqual(exp_res, act_res)
unittest.main(exit=False)
