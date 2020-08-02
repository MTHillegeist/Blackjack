import tkinter as tk
from PIL import Image, ImageTk

class DialogConfig(tk.Toplevel):
    """Set configuration settings for Blackjack."""

    def __init__(self, master=None):
        #super(RenamePopup, self).__init__()
        super().__init__(master)

        # self.geometry("200x200")

        self.settings = dict()
        self.settings["decks"] = 2

        self.master = master
        self.grab_set()

        self.f_main = tk.Frame(self)
        self.f_main["padx"] = 100
        self.f_main["pady"] = 10
        self.f_main.pack(side="top")

        self.label = tk.Label(self.f_main)
        self.label["text"] = "Decks:"
        self.label.grid(sticky="w", row=0, column=0)

        self.spn_decks = tk.Spinbox(self.f_main, from_=1, to=10)
        self.spn_decks["width"] = 5
        self.spn_decks["state"] = "normal"
        self.spn_decks.grid(row=0, column=1)

        self.submit = tk.Button(self.f_main, command=self.submit)
        self.submit["text"] = "Submit"
        self.submit.grid(row=1, column=0, columnspan=2)

    def submit(self):
        self.settings["decks"] = int(self.spn_decks.get())
        self.destroy()

    def show(self):
        self.deiconify()
        self.wait_window()

        return self.settings
