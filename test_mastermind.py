import unittest
import mastermind as mm

"""Test module for the mastermind application
"""

class Tests(unittest.TestCase):
    
    """Test class for mastermind application
    """

    def setUp(self):
        """Setup method
        """
        self.code = (
            mm.Pin.BLACK,
            mm.Pin.BLACK,
            mm.Pin.BLUE,
            mm.Pin.RED
        )
        self.game = mm.Game(code=self.code)

    def test_str2combination(self):
        """Tests validation of guess input
        """
        guess_r = (
            mm.Pin.BLACK,
            mm.Pin.RED,
            mm.Pin.GREEN,
            mm.Pin.WHITE
        )
        guess_f = mm.str2combination('0125')
        self.assertEqual(guess_f, guess_r)
        with self.assertRaises(ValueError):
            mm.str2combination('012')
        with self.assertRaises(ValueError):
            mm.str2combination('01255')
        with self.assertRaises(ValueError):
            mm.str2combination('xxxx')
        with self.assertRaises(ValueError):
            mm.str2combination('6789')

    def test_calc_marking(self):
        """Tests the markings are performed correct
        """
        code = mm.str2combination('0123')

        all_blanks_f = mm.calc_marking(
            code,
            mm.str2combination('4444')
        )
        all_blanks_r = mm.Marking(blacks=0, whites=0, blanks=4)
        self.assertEqual(all_blanks_f, all_blanks_r)

        all_white_f = mm.calc_marking(
            code,
            mm.str2combination('3012')
        )
        all_white_r = mm.Marking(blacks=0, whites=4, blanks=0)
        self.assertEqual(all_white_f, all_white_r)

        two_white_two_black_f = mm.calc_marking(
            code,
            mm.str2combination('3120')
        )
        two_white_two_black_r = mm.Marking(blacks=2, whites=2, blanks=0)
        self.assertEqual(two_white_two_black_f, two_white_two_black_r)

        all_black_f = mm.calc_marking(
            code,
            mm.str2combination('0123')
        )
        all_black_r = mm.Marking(blacks=4, whites=0, blanks=0)
        self.assertEqual(all_black_f, all_black_r)

    def test_gameobj(self):
        """Tests that the game object is consistent
        """"
        self.assertEqual(self.game.code, self.code)
        self.assertEqual(len(self.game.rows), 0)
        self.assertEqual(self.game.turns, 12)
        self.assertEqual(self.game.finished, False)
        self.assertEqual(self.game.won, False)

    def test_win_in_three(self):
        """Test a winning game in three guesses
        """
        self.game.submit_guess(mm.str2combination('0000'))
        self.game.submit_guess(mm.str2combination('1111'))
        self.game.submit_guess(mm.str2combination('0031'))
        self.assertEqual(self.game.is_finished(), True)
        self.assertEqual(self.game.is_won(), True)
        self.assertEqual(self.game.turns, 9)

    def test_lost(self):
        """Test a lost game
        """
        for _ in range(12):
            self.game.submit_guess(mm.str2combination('0000'))

        self.assertEqual(self.game.is_finished(), True)
        self.assertEqual(self.game.is_won(), False)
        self.assertEqual(self.game.turns, 0)

unittest.main()
