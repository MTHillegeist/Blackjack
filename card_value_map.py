from blackjack import Blackjack

# This is just a simple module for printing out the value/card relationships.
card_map = [(x, Blackjack.number_to_card(x) ) for x in range(0, 52)]

for key, value in card_map:
    print(key, value)
