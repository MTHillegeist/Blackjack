import math
import random as rand

class Blackjack():


    def __init__(self):
        self.decks = 2

        self.reset()

    # Move cards on table into the discard pile.
    def clear(self):
        while(len(self.house) > 0):
            self.discard.append(self.house.pop())

        while(len(self.player) > 0):
            self.discard.append(self.player.pop())

    # Deal out the cards.
    def deal(self):
        # print(self.deck)
        self.house.append(self.deck.pop())
        self.house.append(self.deck.pop())

        self.player.append(self.deck.pop())
        self.player.append(self.deck.pop())

        print(Blackjack.hand_value(self.player))
        print(Blackjack.hand_value(self.house))

    def hand_value(hand):
        mod_hand = [min((x % 13)+1, 10) for x in hand]
        mod_hand = [11 if x == 1 else x for x in mod_hand]

        while( sum(mod_hand) > 21 and 11 in mod_hand):
            for index, card in enumerate(mod_hand):
                if( card == 11):
                    mod_hand[index] = 1
                    break;

        return sum(mod_hand)

    # hit
    def hit(self):
        self.player.append(self.deck.pop())

        print(Blackjack.hand_value(self.player))

    # Reshuffles deck and clears hands and discard pile.
    def reset(self):
        print("Reset call")
        # Cards should be in the range 0 to 51 for each value/suit.
        # Must perform modulus operator for multiple decks.
        self.deck = [x % 52 for x in range(0,52 * self.decks)]
        rand.shuffle(self.deck)

        self.discard = []
        self.house = []
        self.player = []

    # Static functions

    # Convert number between 0 and 51 into a string matching a card sprite file.
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
