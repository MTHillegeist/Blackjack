import tkinter as tk
# import Image
from PIL import Image, ImageTk
# from tkinter import *
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

        self.create_widgets()

    def create_widgets(self):
        self.panel1 = tk.Frame(self)
        self.panel1.pack(side="left", fill="y")

        self.button1 = tk.Button(self.panel1)
        self.button1["text"] = "Press the button!"
        self.button1.grid(row=1, column=1, sticky="e")

        load = Image.open("sprites/red_joker.png")
        load = load.resize((100, 145), Image.ANTIALIAS)
        self.card_image = ImageTk.PhotoImage(load)
        #
        self.card_dealer = tk.Label(self.panel1, image=self.card_image)
        # self.card_dealer["width"] = 100
        # self.card_dealer["width"] = 100
        self.card_dealer.grid(row=0, column=1)


root = tk.Tk()
app = Application(master=root)

# def on_closing():
#     app.close()
    # root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
