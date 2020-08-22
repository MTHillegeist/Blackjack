import unittest
from blackjack import Blackjack

class TestBlackjack(unittest.TestCase):
    """docstring for TestBlackjack."""

    def test_hand_value(self):
        errors = 0
        tests = [([9, 9], 20),
                 ([0, 9], 21),
                 ([0, 9, 9], 21),
                 ([0, 0, 9], 12),
                 ([0, 0, 0, 0, 5], 20),
                 ([13, 27, 51], 13)]#0, 1, 12 -> Ace, 2, King

        for test in tests:
            hand = test[0]
            correct = test[1]
            result = Blackjack.hand_value(hand)
            self.assertEqual(result, correct)

    # def __init__(self, arg):
    #     super(TestBlackjack, self).__init__()
    #     self.arg = arg

# hand_value_tests()
if __name__ == '__main__':
    unittest.main()
