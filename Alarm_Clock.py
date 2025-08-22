import tkinter as tk
import datetime
from tkinter import font


current_time = datetime.datetime.now().time().strftime('%I:%M %p')
root = tk.Tk()
root.geometry("400x550")
root.resizable(False, False)
root.iconbitmap(r'icon.ico')
root.title("Alarm Clock")
time = tk.Label(root, text=current_time, font = ('Arial', 20))
time.pack(padx=10, pady=10)


root.mainloop()
