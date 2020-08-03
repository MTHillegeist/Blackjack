import tkinter as tk
from PIL import Image, ImageTk
import os
from os import path
import random as rand
from blackjack import *
from dialog_config import *
# 500x726,0.6887
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
        self.card_width = 100
        self.card_height = 145

        self.images_load()
        self.widgets_create()
        self.scene_update()

    def board_clear(self):
        self.game.clear()
        self.b_hit["state"] = "disabled"

        self.scene_update()

    def board_deal(self):
        self.game.clear()
        self.game.deal()
        self.b_hit["state"] = "normal"

        self.scene_update()

    def board_hit(self):
        self.game.hit()

        self.scene_update()

    def board_shuffle(self):
        self.game.reset()
        self.b_hit["state"] = "disabled"

        self.scene_update()

    def dialog_config(self):
        config = DialogConfig(master=self).show()
        self.game.decks = config["decks"]
        self.b_hit["state"] = "disabled"

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

        # Update card sprites
        num_to_card = Blackjack.number_to_card
        len_h = len(self.game.house)
        len_p = len(self.game.player)

        house_card1 = "back"
        house_card2 = num_to_card( self.game.house[1] ) if len_h >= 2 else "back"

        # Render each player card on top of each other.
        ph_image = None
        if len_p > 0:
            ph_image = Image.new("RGBA", (self.card_width + (len_p-1) * 20, self.card_height))

            for num, card in enumerate(self.game.player):
                card_name = num_to_card(card)
                ph_image.paste(self.card_sprites[card_name], (20 * num, 0 ), self.card_sprites[card_name])
        else:
            ph_image = None

        # Render each dealer card on top of each other.
        hh_image = None
        if len_p > 0:
            hh_image = Image.new("RGBA", (self.card_width + (len_h-1) * 20, self.card_height))

            for num, card in enumerate(self.game.house):
                card_name = None

                # First dealer card is hidden.
                # if num == 0:
                #     card_name = "back"
                # else:
                card_name = num_to_card(card)

                hh_image.paste(self.card_sprites[card_name], (20 * num, 0 ), self.card_sprites[card_name])
        else:
            hh_image = None

        Application.tk_set_image(self.deck, self.card_sprites["back"])
        Application.tk_set_image(self.house_hand, hh_image)
        Application.tk_set_image(self.player_hand, ph_image)

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

        self.f_house = tk.Frame(self.f2)
        self.f_house["bg"] = self.bg_color
        self.f_house.pack(side="top")

        self.house_hand = tk.Label(self.f_house)
        self.house_hand["bg"] = self.bg_color
        self.house_hand.grid(row=0, column=1, padx=card_padx, pady=card_pady)

        self.f_split = tk.Frame(self.f2)
        self.f_split["bg"] = self.bg_color
        self.f_split.pack(side="top", fill="both", expand=1)

        self.f_player = tk.Frame(self.f2)
        self.f_player["bg"] = self.bg_color
        self.f_player.pack(side="top", fill="x", expand=0, padx=card_padx, pady=card_pady)

        self.player_hand = tk.Label(self.f_player)
        self.player_hand["bg"] = self.bg_color
        self.player_hand.pack(side="bottom")

        self.f_buttons = tk.Frame(self.f3)
        self.f_buttons["bg"] = self.bg_color
        self.f_buttons.pack(side="bottom")

        self.b_hit = tk.Button(self.f_buttons)
        self.b_hit["text"] = "Hit"
        self.b_hit["command"] = self.board_hit
        self.b_hit["state"] = "disabled"
        self.b_hit.grid(row=0, column=0, sticky="nsew")

        self.b_deal = tk.Button(self.f_buttons)
        self.b_deal["text"] = "Deal Cards"
        self.b_deal["command"] = self.board_deal
        self.b_deal.grid(row=1, column=0, sticky="nsew")

        self.b_clear = tk.Button(self.f_buttons)
        self.b_clear["text"] = "Clear Board"
        self.b_clear["command"] = self.board_clear
        self.b_clear.grid(row=2, column=0, sticky="nsew")

        self.b_shuffle = tk.Button(self.f_buttons)
        self.b_shuffle["text"] = "Shuffle"
        self.b_shuffle["command"] = self.board_shuffle
        self.b_shuffle.grid(row=3, column=0, sticky="nsew")


root = tk.Tk()
app = Application(master=root)

# def on_closing():
#     app.close()
    # root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
