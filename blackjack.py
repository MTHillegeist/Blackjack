import math
import random as rand
from enum import Enum

class Blackjack():

    class PlayResult(Enum):
        CONTINUE = 0,
        WIN = 1,
        LOSS = 2,
        BUST = 3,
        PUSH = 4,
        BLACKJACK = 5

    def __init__(self):
        self.decks = 2
        self.money = 500
        self.bet = 10

        self.reset()

    # Move cards on table into the discard pile.
    def clear(self):
        while(len(self.house) > 0):
            self.discard.append(self.house.pop())

        while(len(self.player) > 0):
            self.discard.append(self.player.pop())

    # Deal out the cards.
    def deal(self):
        self.house.append(self.deck.pop())
        self.house.append(self.deck.pop())

        self.player.append(self.deck.pop())
        self.player.append(self.deck.pop())

        h_val = Blackjack.hand_value(self.house)
        p_val = Blackjack.hand_value(self.player)

        if(p_val == 21):
            return Blackjack.PlayResult.BLACKJACK
        else:
            return Blackjack.PlayResult.CONTINUE

    # Calculate the greatest value of this hand under 21.
    def hand_value(hand):
        # Convert card numbers that can be 0 to 51 into their blackjack values.
        mod_hand = [min((x % 13)+1, 10) for x in hand]
        # Start by converting all aces to 11.
        mod_hand = [11 if x == 1 else x for x in mod_hand]

        # If total value is greater than 21, convert aces to ones until it is
        # less.
        while( sum(mod_hand) > 21 and 11 in mod_hand):
            for index, card in enumerate(mod_hand):
                if( card == 11):
                    mod_hand[index] = 1
                    break;

        return sum(mod_hand)

    # hit
    def hit(self):
        self.player.append(self.deck.pop())

        h_val = Blackjack.hand_value(self.house)
        p_val = Blackjack.hand_value(self.player)

        if(p_val > 21):
            return Blackjack.PlayResult.BUST
        elif(p_val == 21):
            return Blackjack.PlayResult.BLACKJACK
        else:
            return Blackjack.PlayResult.CONTINUE

    # House plays a card.
    def house_play(self):
        h_val = Blackjack.hand_value(self.house)
        p_val = Blackjack.hand_value(self.player)

        print("House Val: {} Player Val: {}".format(h_val, p_val))

        # Typically, the house will always draw if their value is less than 17.
        # This holds true regardless of the player's hand.
        if(h_val < 17):
            self.house.append(self.deck.pop())
            h_val = Blackjack.hand_value(self.house)
            return Blackjack.PlayResult.CONTINUE
        else: #Evaluate the result.
            if(h_val > 21 or h_val < p_val):
                if(p_val == 21):
                    return Blackjack.PlayResult.BLACKJACK
                else:
                    return Blackjack.PlayResult.WIN
            elif(h_val > p_val):
                return Blackjack.PlayResult.LOSS
            else:# (h_val == p_val):
                return Blackjack.PlayResult.PUSH

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
