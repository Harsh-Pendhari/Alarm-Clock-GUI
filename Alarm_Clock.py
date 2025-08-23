import tkinter as tk
import datetime
from tkinter import font, messagebox
import threading
import time

root = tk.Tk()
root.geometry("400x550")
root.resizable(False, False)
root.iconbitmap(r'icon.ico')
root.title("Alarm Clock")
root.configure(bg="#222E36")

def update_time():
    current_time = datetime.datetime.now().strftime('%I:%M:%S %p')
    time_var.set(current_time)
    root.after(1000, update_time)

time_var = tk.StringVar()
time_label = tk.Label(root, textvariable=time_var, font=('Arial', 28, "bold"),
                      bg="#222E36", fg="white")
time_label.pack(pady=30)

frame = tk.Frame(root, bg="#222E36")
frame.pack(pady=20)

custom_font = font.Font(size=16)

hour_var = tk.StringVar(value="12")
minute_var = tk.StringVar(value="00")
ampm_var = tk.StringVar(value="AM")

hour_spin = tk.Spinbox(frame, from_=1, to=12, wrap=True, textvariable=hour_var,
                       font=custom_font, width=5, state="readonly", justify="center")
minute_spin = tk.Spinbox(frame, from_=0, to=59, wrap=True, format="%02.0f", 
                         textvariable=minute_var, font=custom_font, width=5,
                         state="readonly", justify="center")
ampm_spin = tk.Spinbox(frame, values=("AM", "PM"), textvariable=ampm_var,
                       font=custom_font, width=5, state="readonly", justify="center")

hour_spin.grid(row=0, column=0, padx=5)
minute_spin.grid(row=0, column=1, padx=5)
ampm_spin.grid(row=0, column=2, padx=5)

alarm_time = None
alarm_running = False

def set_alarm():
    global alarm_time, alarm_running
    hour = hour_var.get()
    minute = minute_var.get()
    ampm = ampm_var.get()
    alarm_time = f"{int(hour):02d}:{int(minute):02d} {ampm}"
    alarm_running = True
    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")

def check_alarm():
    global alarm_running
    while True:
        if alarm_running and alarm_time:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            if current_time == alarm_time:
                alarm_running = False
                messagebox.showwarning("Alarm!", f"Time's up! It's {alarm_time}")
        time.sleep(30)

set_btn = tk.Button(root, text="Set Alarm", font=('Arial', 16, "bold"),
                    bg="#4CAF50", fg="white", cursor="hand2", command=set_alarm)
set_btn.pack(pady=20)


threading.Thread(target=check_alarm, daemon=True).start()

update_time()
root.mainloop()
