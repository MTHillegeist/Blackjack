import unittest
from blackjack import Blackjack

class TestBlackjack(unittest.TestCase):
    """docstring for TestBlackjack."""

    def test_get_final_result_basic(self):
        blackjack = Blackjack()
        blackjack.bet = 10

        blackjack.spec_player_add_hand([0, 9]) # A, 10: 21
        blackjack.spec_house_set_hand([9, 4]) # 10, 5: 15
        result, net_money = blackjack.get_final_result(0)
        self.assertEqual(result, Blackjack.PlayResult.BLACKJACK)
        self.assertEqual(net_money, 15)

        blackjack.clear()

        blackjack.spec_player_add_hand([4, 9]) # 15
        blackjack.spec_house_set_hand([9, 9]) # 20
        result, net_money = blackjack.get_final_result(0)
        self.assertEqual(result, Blackjack.PlayResult.LOSS)
        self.assertEqual(net_money, -10)

        blackjack.clear()

        blackjack.spec_player_add_hand([9, 9]) # 20
        blackjack.spec_house_set_hand([9, 6]) # 17
        result, net_money = blackjack.get_final_result(0)
        self.assertEqual(result, Blackjack.PlayResult.WIN)
        self.assertEqual(net_money, 10)

        blackjack.clear()

        blackjack.spec_player_add_hand([9, 9]) # 20
        blackjack.spec_house_set_hand([9, 9]) # 20
        result, net_money = blackjack.get_final_result(0)
        self.assertEqual(result, Blackjack.PlayResult.PUSH)
        self.assertEqual(net_money, 0)

        blackjack.clear()

        blackjack.spec_player_add_hand([9, 9, 3]) # 22
        blackjack.spec_house_set_hand([9, 9]) # 20
        result, net_money = blackjack.get_final_result(0)
        self.assertEqual(result, Blackjack.PlayResult.BUST)
        self.assertEqual(net_money, -10)

    def test_get_final_result_splits(self):
        blackjack = Blackjack()
        blackjack.bet = 10

        blackjack.spec_player_add_hand([0, 9]) # A, 10: 21
        blackjack.spec_player_add_hand([9, 9]) # 20
        blackjack.spec_house_set_hand([9, 7]) # 18
        result, net_money = blackjack.get_final_result(1)
        self.assertEqual(result, Blackjack.PlayResult.WIN)
        self.assertEqual(net_money, 10)

        blackjack.spec_player_add_hand([27, 37, 44]) # 2D, QD, 6C: 18
        result, net_money = blackjack.get_final_result(2)
        self.assertEqual(result, Blackjack.PlayResult.PUSH)
        self.assertEqual(net_money, 0)

        blackjack.spec_player_add_hand([51, 13]) # KC, AS: 21
        result, net_money = blackjack.get_final_result(3)
        self.assertEqual(result, Blackjack.PlayResult.BLACKJACK)
        self.assertEqual(net_money, 15)

# Static Function Tests
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

if __name__ == '__main__':
    unittest.main()
