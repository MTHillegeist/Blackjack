from blackjack import *

def hand_value_error(hand, correct, result):
    print("Incorrect hand value {} found for hand:".format( result))
    print(hand)
    print("Correct Value: " + str(correct))

def hand_value_tests():
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
        if(result != test[1]):
            hand_value_error(test[0], test[1], result)
            errors += 1

    if(errors > 0):
        print(str(errors) + " errors found.")
    else:
        print("No errors found.")

hand_value_tests()
