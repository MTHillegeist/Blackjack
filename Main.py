import tkinter as tk
from PIL import Image, ImageTk
import os
from os import path
import random as rand
# 500x726,0.6887
class Application(tk.Frame):
    """docstring for Application."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("TTC Manager")
        # self.master.iconbitmap('out3_nr3_icon.ico')
        self.master.geometry("800x500")
        self.pack(fill="both", expand=1)

        self.images_load()
        self.widgets_create()

    def widgets_create(self):
        self.panel1 = tk.Frame(self)
        self.panel1.pack(side="left", fill="y")

        self.button1 = tk.Button(self.panel1)
        self.button1["text"] = "Press the button!"
        self.button1["command"] = self.change_dealer_card
        self.button1.grid(row=1, column=1, sticky="e")
        #
        self.card_dealer = tk.Label(self.panel1, image=self.card_sprites["back"])
        # self.card_dealer["width"] = 100
        # self.card_dealer["width"] = 100
        self.card_dealer.grid(row=0, column=1)

    def images_load(self):
        self.card_sprites = dict()
        files = os.listdir("sprites")

        for file in files:
            image = Image.open("sprites/" + file)
            image = image.resize((100, 145), Image.ANTIALIAS)

            self.card_sprites[file.replace(".png", "")] = ImageTk.PhotoImage(image)


    def change_dealer_card(self):
        self.card_dealer["image"] = rand.choice(list(self.card_sprites.values())) # self.card_sprites["10_of_clubs"]



root = tk.Tk()
app = Application(master=root)

# def on_closing():
#     app.close()
    # root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
