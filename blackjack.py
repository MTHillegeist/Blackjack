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
        BLACKJACK = 5,
        TWENTYONE = 6

    class PlayerHand:
        def __init__(self):
            self.cards = []
            self.double = False

        def __init__(self, hand):
            self.cards = hand
            self.double = False

    def __init__(self):
        self.decks = 2
        self.money = 500
        self.bet = 10
        self.max_splits = 4

        self.reset()

    # Move cards on table into the discard pile.
    def clear(self):
        while(len(self.house) > 0):
            self.discard.append(self.house.pop())

        while(len(self.player_hands) > 0):
            self.player = self.player_hands.pop()
            while(len(self.player.cards) > 0):
                self.discard.append(self.player.cards.pop())
        self.player = None


    # Deal out the cards.
    def deal(self):
        self.house.append(self.deck.pop())
        self.house.append(self.deck.pop())

        self.player_hands.append(Blackjack.PlayerHand())

        self.player = self.player_hands[0]
        self.player.cards.append(self.deck.pop())
        self.player.cards.append(self.deck.pop())

        h_val = Blackjack.hand_value(self.house)
        p_val = Blackjack.hand_value(self.player.cards)

        if(p_val == 21):
            return Blackjack.PlayResult.BLACKJACK
        else:
            return Blackjack.PlayResult.CONTINUE

    # Gets a tuple including the final result of a hand and the total won/lost.
    # Should only be called after the house is done playing.
    def get_final_result(self, hand_index):
        hand = self.player_hands[hand_index]
        h_val = Blackjack.hand_value(self.house)
        p_val = Blackjack.hand_value(hand.cards)
        double_ratio = 2 if hand.double else 1
        result = None
        net_money = None

        if(p_val > 21):
            result = Blackjack.PlayResult.BUST
            net_money = -1 * double_ratio * self.bet
        elif(p_val == 21 and len(hand.cards) == 2 and h_val != 21):
            result = Blackjack.PlayResult.BLACKJACK
            net_money = int(self.bet * 1.5)
        elif(h_val > 21 or p_val > h_val):
            result = Blackjack.PlayResult.WIN
            net_money = double_ratio * self.bet
        elif(h_val == p_val):
            result = Blackjack.PlayResult.PUSH
            net_money = 0
        elif(h_val >= p_val):
            result = Blackjack.PlayResult.LOSS
            net_money = -1 * double_ratio * self.bet
        else:
            raise ValueError("Invalid branch reached in get_final_result.\n" +
                             "House: {} \n".format(self.house) +
                             "Player Hand Index, Cards: {0},{1}\n"
                             .format(hand_index, hand.cards))

        return (result, net_money)


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
        self.player.cards.append(self.deck.pop())

        h_val = Blackjack.hand_value(self.house)
        p_val = Blackjack.hand_value(self.player.cards)

        if(p_val > 21):
            return Blackjack.PlayResult.BUST
        elif(p_val == 21):
            return Blackjack.PlayResult.TWENTYONE
        else:
            return Blackjack.PlayResult.CONTINUE

    # House plays a card.
    def house_play(self):
        h_val = Blackjack.hand_value(self.house)
        p_val = Blackjack.hand_value(self.player.cards)

        print("House Val: {} Player Val: {}".format(h_val, p_val))

        # Typically, the house will always draw if their value is less than 17.
        # This holds true regardless of the player's hand.
        if(h_val < 17):
            self.house.append(self.deck.pop())
            h_val = Blackjack.hand_value(self.house)
            return Blackjack.PlayResult.CONTINUE
        else: #Evaluate the result.
            if(h_val > 21 or h_val < p_val):
                if(p_val == 21 and len(self.player.cards) == 2):
                    return Blackjack.PlayResult.BLACKJACK
                else:
                    return Blackjack.PlayResult.WIN
            elif(h_val > p_val):
                return Blackjack.PlayResult.LOSS
            else:# (h_val == p_val):
                return Blackjack.PlayResult.PUSH

    # Should be called after a hand is done being played. Moves to the next_split
    # hand in line.
    def next_split(self):
        curr_index = self.player_hands.index(self.player)
        if(curr_index == 0):
            raise ValueError("Attempt to move to next hand when at hand 0.")
        self.player = self.player_hands[curr_index - 1]

    # Reshuffles deck and clears hands and discard pile.
    def reset(self):
        print("Reset call")
        # Cards should be in the range 0 to 51 for each value/suit.
        # Must perform modulus operator for multiple decks.
        self.deck = [x % 52 for x in range(0,52 * self.decks)]
        rand.shuffle(self.deck)

        # Indicator for which player hand  is in play (splits.)
        self.current_hand = 0

        self.discard = []
        self.house = []
        self.player_hands = []
        # self.player will be the hand currently in play.
        # Set on deal.
        self.player = None

    # Split current hand into two hands and draw a card for each.
    # Only works if the current hand has exactly two of the same cards
    # and this is not the fourth hand (after three splits.)
    def split(self):
        if(len(self.player_hands) == self.max_splits):
            raise ValueError("Attempt to call split function when their are" +
                             " already 4 splits on table.")
        # Create a new hand and take the top card from the current hand.
        new_hand = Blackjack.PlayerHand()
        new_hand.cards.append( self.player.cards.pop() )
        # Add a new card to each of the splits.
        self.player.cards.append(self.deck.pop())
        new_hand.cards.append(self.deck.pop())
        # Add the new hand to the list of hands.
        self.player_hands.append(new_hand)
        # Make the new hand the current hand. It will be played first.
        self.player = new_hand

    # Special functions
    # These functions will not be used during the normal course of play.
    # They exist to set the board up with specific cards for debuggin purposes
    # or for setting up scenarios for the player.
    def spec_house_set_hand(self, hand):
        self.house = hand

    def spec_player_add_hand(self, hand):
        self.player_hands.append(Blackjack.PlayerHand(hand))

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
