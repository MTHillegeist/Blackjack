import tkinter as tk
from PIL import Image, ImageTk
import os
from os import path
import random as rand
from blackjack import *
# 500x726,0.6887
class Application(tk.Frame):
    """docstring for Application."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Blackjack - Basic Strategy")
        # self.master.iconbitmap('out3_nr3_icon.ico')
        self.master.geometry("800x500")
        self.pack(fill="both", expand=1)

        self.game = Blackjack()

        self.images_load()
        self.widgets_create()

    def widgets_create(self):
        self.panel1 = tk.Frame(self)
        self.panel1["bg"] = "#006644"
        self.panel1.pack(side="top", fill="y", expand=1)

        self.button1 = tk.Button(self.panel1)
        self.button1["text"] = "Press the button!"
        self.button1["command"] = self.change_dealer_card
        self.button1.grid(row=1, column=1, sticky="e")

        self.deck = tk.Label(self.panel1, image=self.card_sprites["back"])
        self.deck["padx"] = 200
        self.deck.grid(row=0, column=0)

        self.house_hidden = tk.Label(self.panel1, image=self.card_sprites["back"])
        self.house_hidden.grid(row=0, column=1)

        self.house_vis1 = tk.Label(self.panel1, image=self.card_sprites["red_joker"])
        self.house_vis1.grid(row=0, column=2)

        self.player_c1 = tk.Label(self.panel1, image=self.card_sprites["red_joker"])
        self.player_c1.grid(row=2, column=1)

        self.player_c2 = tk.Label(self.panel1, image=self.card_sprites["red_joker"])
        self.player_c2.grid(row=2, column=2)


    def images_load(self):
        self.card_sprites = dict()
        files = os.listdir("sprites")

        for file in files:
            image = Image.open("sprites/" + file)
            image = image.resize((100, 145), Image.ANTIALIAS)

            self.card_sprites[file.replace(".png", "")] = ImageTk.PhotoImage(image)


    def change_dealer_card(self):
        # rand_num = rand.choice(range(0,52))
        # card_name = Blackjack.number_to_card(rand_num)
        # self.house_vis1["image"] = self.card_sprites[card_name]
        self.game.clear()
        self.game.deal()

        house_card2 = Blackjack.number_to_card( self.game.house[1] )
        player_card1 = Blackjack.number_to_card( self.game.player[0] )
        player_card2 = Blackjack.number_to_card( self.game.player[1] )

        self.house_vis1["image"] = self.card_sprites[house_card2]
        self.player_c1["image"] = self.card_sprites[player_card1]
        self.player_c2["image"] = self.card_sprites[player_card2]




root = tk.Tk()
app = Application(master=root)

# def on_closing():
#     app.close()
    # root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
