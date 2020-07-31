import math
import random as rand

class Blackjack():


    def __init__(self):
        self.decks = 1

        self.reset()

    def clear(self):
        while(len(self.house) > 0):
            self.discard.append(self.house.pop())

        while(len(self.player) > 0):
            self.discard.append(self.player.pop())

    def deal(self):
        print(self.deck)
        self.house.append(self.deck.pop())
        self.house.append(self.deck.pop())

        self.player.append(self.deck.pop())
        self.player.append(self.deck.pop())

    # Reshuffles deck and clears hands and discard pile.
    def reset(self):
        print("Reset call")
        self.deck = [x for x in range(0,52 * self.decks)]
        rand.shuffle(self.deck)

        self.discard = []
        self.house = []
        self.player = []

    def number_to_card(number):
        suits = {0 : "hearts", 1 : "spades", 2 : "diamonds", 3 : "clubs"}
        suit = math.floor( number / 13)
        card = number % 13

        str_suit = suits[suit]
        str_card = None

        if(card == 0):
            str_card = "ace"
        elif(card in range(1, 10)):
            str_card = str(card + 1)
        elif(card == 10):
            str_card = "jack"
        elif(card == 11):
            str_card = "queen"
        elif(card == 12):
            str_card = "king"
        else:
            raise ValueError("An invalid card value was calculated.")

        return str_card + "_of_" + str_suit
