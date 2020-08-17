import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os
from os import path
import time
import random as rand
from blackjack import Blackjack
from dialog_config import DialogConfig
from dialog_bet import DialogBet
import math


class Application(tk.Frame):
    """Root window for Blackjack application."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Blackjack - Basic Strategy")
        # self.master.iconbitmap('out3_nr3_icon.ico')
        self.master.geometry("800x500")
        self.pack(fill="both", expand=1)

        self.game = Blackjack()

        self.bg_color = "#006644"
        self.t_color =  "#fcf403"
        self.h_color = "#005634"
        self.card_width = 100
        self.card_height = 145
        self.display_hidden_house = False

        self.images_load()
        self.widgets_create()
        self.scene_update()

    def board_clear(self):
        self.game.clear()
        self.b_hit["state"] = "disabled"
        self.b_double["state"] = "disabled"
        self.b_hold["state"] = "disabled"
        self.l_game_result["text"] = ""
        self.display_hidden_house = False

        self.scene_update()

    def board_deal(self):
        self.l_game_result["text"] = ""
        self.display_hidden_house = False
        self.b_deal["state"] = "disabled"
        self.b_clear["state"] = "disabled"
        self.b_change_bet.grid_remove()

        self.game.clear()
        result = self.game.deal()

        if(result == Blackjack.PlayResult.BLACKJACK):
            result = self.board_house_plays()
            self.board_handle_result(result)
        else:
            self.b_hit["state"] = "normal"
            self.b_double["state"] = "normal"
            self.b_hold["state"] = "normal"
            self.b_split["state"] = "normal"

        self.scene_update()

    def board_double(self):
        self.game.double = True

        result = self.game.hit()

        if(result == Blackjack.PlayResult.CONTINUE or result == Blackjack.PlayResult.TWENTYONE):
            hand_ind = self.game.player_hands.index(self.game.player)
            if(hand_ind == 0):
                result = self.board_house_plays()
                self.board_handle_result(result)
            else:
                self.game.next_split()
        else:
            self.board_handle_result(result)

        self.scene_update()

    def board_handle_result(self, result):
        double_ratio = 2 if self.game.double else 1

        if(result == Blackjack.PlayResult.BUST):
            self.game.money -= double_ratio * self.game.bet
            self.l_game_result["text"] = "Bust!"
        elif(result == Blackjack.PlayResult.BLACKJACK):
            self.game.money += int( self.game.bet * 1.5)
            self.l_game_result["text"] = "Blackjack!"
        elif(result == Blackjack.PlayResult.WIN):
            self.game.money += double_ratio * self.game.bet
            self.l_game_result["text"] = "Win!"
        elif(result == Blackjack.PlayResult.PUSH):
            self.l_game_result["text"] = "Push"
            self.display_hidden_house = True
        elif(result == Blackjack.PlayResult.LOSS):
            self.game.money -= double_ratio * self.game.bet
            self.l_game_result["text"] = "Loss!"
        else:
            raise ValueError("An invalid value was passed to board_handle_result: ".format(result))

        self.b_hit["state"] = "disabled"
        self.b_double["state"] = "disabled"
        self.b_hold["state"] = "disabled"
        self.b_deal["state"] = "normal"
        self.b_clear["state"] = "normal"
        self.b_shuffle["state"] = "normal"
        self.b_change_bet.grid()

    def board_hit(self):
        result = self.game.hit()
        # Player did not bust or hit a blackjack. It is still their turn.
        if(result == Blackjack.PlayResult.CONTINUE):
            pass
        # 21. Player is done and all that is left is for the house to play.
        # Technically, this is not actually Blackjack because they hit once.
        elif(result == Blackjack.PlayResult.TWENTYONE):
            hand_ind = self.game.player_hands.index(self.game.player)
            if(hand_ind == 0):
                result = self.board_house_plays()
                self.board_handle_result(result)
            else:
                self.game.next_split()
        else: #Bust.
            self.board_handle_result(result)

        self.scene_update()

    def board_hold(self):

        hand_ind = self.game.player_hands.index(self.game.player)
        if(hand_ind == 0):
            result = self.board_house_plays()
            self.board_handle_result(result)
        else:
            self.game.next_split()

        self.scene_update()

    # House plays cards till they win, lose or tie.
    # Also handles results in cases
    def board_house_plays(self):
        self.b_hit["state"] = "disabled"
        self.b_double["state"] = "disabled"
        self.b_hold["state"] = "disabled"
        self.b_deal["state"] = "disabled"
        self.b_shuffle["state"] = "disabled"
        self.b_clear["state"] = "disabled"
        self.display_hidden_house = True
        self.scene_update()

        while(True):
            sleep_total = 1
            sleep_step = 0.1
            sleep_reps = math.floor(sleep_total / sleep_step) + 1

            for _ in range(0, sleep_reps):
                time.sleep(sleep_step)
                self.master.update()

            result = self.game.house_play()

            if(result != Blackjack.PlayResult.CONTINUE):
                return result;
            else:
                self.scene_update()

    # Reset the whole board, cards, and buttons.
    def board_shuffle(self):
        self.game.reset()
        self.b_hit["state"] = "disabled"
        self.b_double["state"] = "disabled"
        self.b_hold["state"] = "disabled"
        self.b_deal["state"] = "normal"
        self.b_clear["state"] = "normal"
        self.l_game_result["text"] = ""

        self.scene_update()


    def board_split(self):
        self.game.split()

        self.scene_update()


    def change_bet(self):
        bet = DialogBet(master=self).show()
        self.game.bet = bet["bet"]
        self.scene_update()

    def dialog_config(self):
        config = DialogConfig(master=self).show()
        self.game.decks = config["decks"]
        self.b_hit["state"] = "disabled"
        self.b_hold["state"] = "disabled"

        self.game.reset()
        self.scene_update()

    def images_load(self):
        self.card_sprites = dict()
        files = os.listdir("sprites")

        for file in files:
            image = Image.open("sprites/" + file)
            image = image.resize((self.card_width, self.card_height), Image.ANTIALIAS)

            self.card_sprites[file.replace(".png", "")] = image

    # Update all visuals. This includes deck labels, card sprites, etc.
    def scene_update(self):
        # Update deck labels
        self.l_deck_ct_val["text"] = str(self.game.decks)
        self.l_card_ct_val["text"] = str(len(self.game.deck))
        self.l_money_val["text"] = str(self.game.money)
        self.l_bet_val["text"] = str(self.game.bet)

        # Update card sprites
        num_to_card = Blackjack.number_to_card
        len_h = len(self.game.house)
        len_phs = len(self.game.player_hands)

        house_card1 = "back"
        house_card2 = num_to_card( self.game.house[1] ) if len_h >= 2 else "back"

        # # DEBUG:
        # for index, hand in enumerate(self.game.player_hands):
        #     print("Player hand {0}: {1}".format(index, hand))
        # print(self.game.player_hands)
        # print(self.game.player)

        # Render each player card on top of each other.
        ph_images = []
        for hand in self.game.player_hands:
            len_p = len(hand)
            ph_image = Image.new("RGBA", (self.card_width + (len_p-1) * 20, self.card_height))

            for num, card in enumerate(hand):
                card_name = num_to_card(card)
                ph_image.paste(self.card_sprites[card_name], (20 * num, 0 ), self.card_sprites[card_name])

            if(hand != self.game.player):
                enhancer = ImageEnhance.Brightness(ph_image)
                ph_image = enhancer.enhance(0.5)

            ph_images.append(ph_image)

        # We have to add to append None until we hit 4, since there are 4
        # labels. If there are no cards for the label to display, None must be
        # passed through to get rid of any existing image.
        while len(ph_images) < self.game.max_splits:
            ph_images.append(None)

        for index, ph_image in enumerate(ph_images):
            Application.tk_set_image(self.l_player_hands[index], ph_image)

        # Render each dealer card on top of each other.
        hh_image = None
        if len_h > 0:
            hh_image = Image.new("RGBA", (self.card_width + (len_h-1) * 20, self.card_height))

            for num, card in enumerate(self.game.house):
                card_name = None

                # First dealer card is hidden.
                if num == 0 and self.display_hidden_house == False:
                    card_name = "back"
                else:
                    card_name = num_to_card(card)

                hh_image.paste(self.card_sprites[card_name], (20 * num, 0 ), self.card_sprites[card_name])
        else:
            hh_image = None

        Application.tk_set_image(self.deck, self.card_sprites["back"])
        Application.tk_set_image(self.house_hand, hh_image)




    def tk_set_image(tk_object, img):
        if(img == None):
            tk_object["image"] = ""
            tk_object.image = None
        else:
            pimg = ImageTk.PhotoImage(img)
            tk_object["image"] = pimg
            tk_object.image = pimg

    def widgets_create(self):
        card_padx = 5
        card_pady = 10

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.filemenu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Configuration", command=self.dialog_config)

        self.f1 = tk.Frame(self)
        self.f1["bg"] = self.bg_color
        self.f1.pack(side="left", fill="both", expand=0)

        self.f2 = tk.Frame(self)
        self.f2["bg"] = self.bg_color
        self.f2.pack(side="left", fill="both", expand=1)

        self.f3 = tk.Frame(self)
        self.f3["bg"] = self.bg_color
        self.f3.pack(side="right", fill="y", expand=0)

        self.deck = tk.Label(self.f1)
        # self.deck["visible"] = False
        self.deck.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        self.l_deck_ct = tk.Label(self.f1, text="Decks: ")
        self.l_deck_ct["fg"] = self.t_color
        self.l_deck_ct["bg"] = self.bg_color
        self.l_deck_ct.grid(row=1, column=0, sticky="e")

        self.l_deck_ct_val = tk.Label(self.f1, text=str(self.game.decks))
        self.l_deck_ct_val["fg"] = self.t_color
        self.l_deck_ct_val["bg"] = self.bg_color
        self.l_deck_ct_val.grid(row=1, column=1, sticky="w")

        self.l_card_ct = tk.Label(self.f1, text="Card Count: ")
        self.l_card_ct["fg"] = self.t_color
        self.l_card_ct["bg"] = self.bg_color
        self.l_card_ct.grid(row=2, column=0, sticky="e")

        self.l_card_ct_val = tk.Label(self.f1, text=str(len(self.game.deck)))
        self.l_card_ct_val["fg"] = self.t_color
        self.l_card_ct_val["bg"] = self.bg_color
        self.l_card_ct_val.grid(row=2, column=1, sticky="w")

        self.l_money = tk.Label(self.f1, text="Money: ")
        self.l_money["fg"] = self.t_color
        self.l_money["bg"] = self.bg_color
        self.l_money.grid(row=3, column=0, sticky="e")

        self.l_money_val = tk.Label(self.f1, text=str(self.game.money))
        self.l_money_val["fg"] = self.t_color
        self.l_money_val["bg"] = self.bg_color
        self.l_money_val.grid(row=3, column=1, sticky="w")

        self.l_bet = tk.Label(self.f1, text="Bet: ")
        self.l_bet["fg"] = self.t_color
        self.l_bet["bg"] = self.bg_color
        self.l_bet.grid(row=4, column=0, sticky="e")

        self.l_bet_val = tk.Label(self.f1, text=str(self.game.bet))
        self.l_bet_val["fg"] = self.t_color
        self.l_bet_val["bg"] = self.bg_color
        self.l_bet_val.grid(row=4, column=1, sticky="w")

        self.b_change_bet = tk.Button(self.f1, text="Change", command=self.change_bet)
        self.b_change_bet["fg"] = self.t_color
        self.b_change_bet["bg"] = self.bg_color
        self.b_change_bet["activebackground"] = self.h_color
        self.b_change_bet["activeforeground"] = self.t_color
        self.b_change_bet.grid(row=4, column=2, sticky="w")

        self.f_house = tk.Frame(self.f2)
        self.f_house["bg"] = self.bg_color
        self.f_house.pack(side="top")

        self.house_hand = tk.Label(self.f_house)
        self.house_hand["bg"] = self.bg_color
        self.house_hand.grid(row=0, column=1, padx=card_padx, pady=card_pady)

        self.f_split = tk.Frame(self.f2)
        self.f_split["bg"] = self.bg_color
        self.f_split.pack(side="top", fill="both", expand=1)

        self.l_game_result = tk.Label(self.f_split)
        self.l_game_result["bg"] = self.bg_color
        self.l_game_result["fg"] = self.t_color
        self.l_game_result["font"] = ("Helvetica", 30)
        self.l_game_result.pack(fill="both", expand=1)

        self.f_player = tk.Frame(self.f2)
        self.f_player["bg"] = self.bg_color
        self.f_player.pack(side="top", fill="x", expand=0, padx=card_padx, pady=card_pady)

        self.l_player_hands = []

        l_player_hand0 = tk.Label(self.f_player)
        l_player_hand0["bg"] = self.bg_color
        l_player_hand0.pack(side="left")
        self.l_player_hands.append(l_player_hand0)

        l_player_hand1 = tk.Label(self.f_player)
        l_player_hand1["bg"] = self.bg_color
        l_player_hand1.pack(side="left")
        self.l_player_hands.append(l_player_hand1)

        l_player_hand2 = tk.Label(self.f_player)
        l_player_hand2["bg"] = self.bg_color
        l_player_hand2.pack(side="left")
        self.l_player_hands.append(l_player_hand2)

        l_player_hand3 = tk.Label(self.f_player)
        l_player_hand3["bg"] = self.bg_color
        l_player_hand3.pack(side="left")
        self.l_player_hands.append(l_player_hand3)

        self.f_buttons = tk.Frame(self.f3)
        self.f_buttons["bg"] = self.bg_color
        self.f_buttons.pack(side="bottom")

        self.b_hit = tk.Button(self.f_buttons)
        self.b_hit["text"] = "Hit"
        self.b_hit["command"] = self.board_hit
        self.b_hit["state"] = "disabled"
        self.b_hit.grid(row=0, column=0, sticky="nsew")

        self.b_double = tk.Button(self.f_buttons)
        self.b_double["text"] = "Double"
        self.b_double["command"] = self.board_double
        self.b_double["state"] = "disabled"
        self.b_double.grid(row=1, column=0, sticky="nsew")

        self.b_split = tk.Button(self.f_buttons)
        self.b_split["text"] = "Split"
        self.b_split["command"] = self.board_split
        self.b_split["state"] = "disabled"
        self.b_split.grid(row=2, column=0, sticky="nsew")

        self.b_hold = tk.Button(self.f_buttons)
        self.b_hold["text"] = "Hold"
        self.b_hold["command"] = self.board_hold
        self.b_hold["state"] = "disabled"
        self.b_hold.grid(row=3, column=0, sticky="nsew")

        self.b_deal = tk.Button(self.f_buttons)
        self.b_deal["text"] = "Deal Cards"
        self.b_deal["command"] = self.board_deal
        self.b_deal.grid(row=4, column=0, sticky="nsew")

        self.b_clear = tk.Button(self.f_buttons)
        self.b_clear["text"] = "Clear Board"
        self.b_clear["command"] = self.board_clear
        self.b_clear.grid(row=5, column=0, sticky="nsew")

        self.b_shuffle = tk.Button(self.f_buttons)
        self.b_shuffle["text"] = "Shuffle"
        self.b_shuffle["command"] = self.board_shuffle
        self.b_shuffle.grid(row=6, column=0, sticky="nsew")


root = tk.Tk()
app = Application(master=root)

# def on_closing():
#     app.close()
    # root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
