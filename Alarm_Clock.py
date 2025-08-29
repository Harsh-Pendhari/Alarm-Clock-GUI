import tkinter as tk
from tkinter import font, messagebox
import datetime
import threading
import time
import winsound

root = tk.Tk()
root.geometry("420x520")
root.resizable(False, False)
root.title("Alarm Clock")
root.iconbitmap(r'icon.ico')
root.configure(bg="#222E36")

def update_time():
    current_time = datetime.datetime.now().strftime('%I:%M:%S %p')
    time_var.set(current_time)
    root.after(1000, update_time)

time_var = tk.StringVar()
time_lbl = tk.Label(root, textvariable=time_var, font=("Arial", 30, "bold"),
                    bg="#222E36", fg="white")
time_lbl.pack(pady=30)

frame = tk.Frame(root, bg="#222E36")
frame.pack(pady=30)

custom_font = font.Font(size=16)

hour_var = tk.StringVar(value="12")
minute_var = tk.StringVar(value="00")
ampm_var = tk.StringVar(value="AM")

def validate_hour(P):
    return P.isdigit() and (1 <= int(P) <= 12 or P == "")

def validate_minute(P):
    return P.isdigit() and (0 <= int(P) <= 59 or P == "")

vcmd_hour = (root.register(validate_hour), "%P")
vcmd_minute = (root.register(validate_minute), "%P")

hour_spin = tk.Spinbox(frame, from_=1, to=12, wrap=True, textvariable=hour_var,
                       font=custom_font, width=5, justify="center",
                       validate="key", validatecommand=vcmd_hour)

minute_spin = tk.Spinbox(frame, from_=0, to=59, wrap=True, format="%02.0f",
                         textvariable=minute_var, font=custom_font, width=5,
                         justify="center", validate="key", validatecommand=vcmd_minute)

ampm_spin = tk.Spinbox(frame, values=("AM", "PM"), textvariable=ampm_var,
                       font=custom_font, width=5, state="readonly", justify="center")

hour_spin.grid(row=0, column=0, padx=10)
minute_spin.grid(row=0, column=1, padx=10)
ampm_spin.grid(row=0, column=2, padx=10)

set_lbl_var = tk.StringVar(value="No Alarm Set")
set_lbl = tk.Label(root, textvariable=set_lbl_var, font=("Arial", 14),
                   bg="#222E36", fg="lightgray")
set_lbl.pack(pady=15)

alarm_time = None
alarm_running = False
alarm_thread = None
snooze_minutes = 5

def alarm_sound_loop():
    global alarm_running
    while alarm_running:
        winsound.Beep(2000, 700)
        time.sleep(0.3)

def start_alarm():
    global alarm_running, alarm_thread
    if not alarm_running:
        alarm_running = True
        set_lbl_var.set("⏰ Alarm Ringing!")
        alarm_thread = threading.Thread(target=alarm_sound_loop, daemon=True)
        alarm_thread.start()

def stop_alarm():
    global alarm_running, alarm_time
    alarm_running = False
    alarm_time = None
    set_lbl_var.set("No Alarm Set")

def snooze_alarm():
    global alarm_running, alarm_time
    if alarm_running:
        alarm_running = False
        set_lbl_var.set(f"Snoozed for {snooze_minutes} minutes")
        now = datetime.datetime.now()
        snooze_time = now + datetime.timedelta(minutes=snooze_minutes)
        alarm_time = snooze_time.strftime('%I:%M %p')

def set_alarm():
    global alarm_time, alarm_running
    hour = hour_var.get()
    minute = minute_var.get()
    ampm = ampm_var.get()

    if not hour.isdigit() or not minute.isdigit():
        messagebox.showerror("Invalid Input", "Hour and Minute must be numbers")
        return

    alarm_time = f"{int(hour):02d}:{int(minute):02d} {ampm}"
    alarm_running = False
    set_lbl_var.set(f"Alarm set for {alarm_time}")
    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")

def check_alarm():
    global alarm_running
    while True:
        if not alarm_running and alarm_time:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            if current_time == alarm_time:
                start_alarm()
        time.sleep(20)

btn_frame = tk.Frame(root, bg="#222E36")
btn_frame.pack(pady=20)

set_btn = tk.Button(btn_frame, text="Set Alarm", font=("Arial", 16, "bold"),
                    bg="#4CAF50", fg="white", cursor="hand2", relief="flat",
                    width=12, command=set_alarm)
stop_btn = tk.Button(btn_frame, text="Stop Alarm", font=("Arial", 16, "bold"),
                     bg="#F44336", fg="white", cursor="hand2", relief="flat",
                     width=12, command=stop_alarm)
snooze_btn = tk.Button(root, text="Snooze", font=("Arial", 16, "bold"),
                       bg="#FF9800", fg="white", cursor="hand2", relief="flat",
                       width=26, command=snooze_alarm)

set_btn.grid(row=0, column=0, padx=10)
stop_btn.grid(row=0, column=1, padx=10)
snooze_btn.pack(pady=10)

update_time()
threading.Thread(target=check_alarm, daemon=True).start()

root.mainloop()
