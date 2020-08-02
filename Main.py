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
        self.card_width = 100
        self.card_height = 145

        self.images_load()
        self.widgets_create()

    def board_clear(self):
        self.game.clear()

        self.sprites_update()

    def board_deal(self):
        self.game.clear()
        self.game.deal()

        self.sprites_update()

    def board_shuffle(self):
        self.game.reset()
        self.sprites_update()

    def dialog_config(self):
        config = DialogConfig(master=self).show()
        self.game.decks = config["decks"]

        self.game.reset()
        self.sprites_update()

    def images_load(self):
        self.card_sprites = dict()
        files = os.listdir("sprites")

        for file in files:
            image = Image.open("sprites/" + file)
            image = image.resize((self.card_width, self.card_height), Image.ANTIALIAS)

            self.card_sprites[file.replace(".png", "")] = ImageTk.PhotoImage(image)

    def sprites_update(self):

        num_to_card = Blackjack.number_to_card
        len_h = len(self.game.house)
        len_p = len(self.game.player)

        house_card1 = "back"
        house_card2 = num_to_card( self.game.house[1] ) if len_h >= 2 else "back"
        player_card1 = num_to_card( self.game.player[0] ) if len_p >= 1 else "back"
        player_card2 = num_to_card( self.game.player[1] ) if len_p >= 2 else "back"

        self.house_hidden["image"] = self.card_sprites[house_card1]
        self.house_vis1["image"] = self.card_sprites[house_card2]
        self.player_c1["image"] = self.card_sprites[player_card1]
        self.player_c2["image"] = self.card_sprites[player_card2]

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
        self.f1.pack(side="left", fill="both", expand=1)

        self.f2 = tk.Frame(self)
        self.f2["bg"] = self.bg_color
        self.f2.pack(side="left", fill="y", expand=0)

        self.f3 = tk.Frame(self)
        self.f3["bg"] = self.bg_color
        self.f3.pack(side="left", fill="both", expand=1)

        self.deck = tk.Label(self.f2, image=self.card_sprites["back"])
        # self.deck["visible"] = False
        self.deck.grid(row=0, column=0, padx=20, pady=10)

        self.house_hidden = tk.Label(self.f2, image=self.card_sprites["back"])
        self.house_hidden["width"] = self.card_width
        self.house_hidden.grid(row=0, column=1, padx=card_padx, pady=card_pady)

        self.house_vis1 = tk.Label(self.f2, image=self.card_sprites["back"])
        self.house_vis1.grid(row=0, column=2, padx=card_padx, pady=card_pady)

        self.f_split = tk.Frame(self.f2)
        self.f_split["height"] = 100
        self.f_split["bg"] = self.bg_color
        self.f_split.grid(row=1, column=0, columnspan=3)

        self.player_c1 = tk.Label(self.f2, image=self.card_sprites["back"])
        self.player_c1.grid(row=2, column=1, padx=card_padx, pady=card_pady)

        self.player_c2 = tk.Label(self.f2, image=self.card_sprites["back"])
        self.player_c2.grid(row=2, column=2, padx=card_padx, pady=card_pady)

        self.f_buttons = tk.Frame(self.f3)
        self.f_buttons.pack(side="bottom")

        self.b_deal = tk.Button(self.f_buttons)
        self.b_deal["text"] = "Deal Cards"
        self.b_deal["command"] = self.board_deal
        self.b_deal.grid(row=0, column=0, sticky="nsew")

        self.b_clear = tk.Button(self.f_buttons)
        self.b_clear["text"] = "Clear Board"
        self.b_clear["command"] = self.board_clear
        self.b_clear.grid(row=1, column=0, sticky="nsew")

        self.b_shuffle = tk.Button(self.f_buttons)
        self.b_shuffle["text"] = "Re-Shuffle"
        self.b_shuffle["command"] = self.board_shuffle
        self.b_shuffle.grid(row=2, column=0, sticky="nsew")


root = tk.Tk()
app = Application(master=root)

# def on_closing():
#     app.close()
    # root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
