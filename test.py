# from tkinter import *
import tkinter as tk
import pandas as pd
import webcolors
import os
from PIL import Image, ImageDraw



class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = label(self,text)
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text="Get", command=self.on_button)
        self.entry.pack()
        self.button.pack()

    def on_button(self):
        print(self.entry.get())

app = SampleApp()
app.mainloop()
