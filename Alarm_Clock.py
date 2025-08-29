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
    time_var.set(datetime.datetime.now().strftime('%I:%M:%S %p'))
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

def allow_numeric_partial(P, max_len):
    if P == "": 
        return True
    return P.isdigit() and len(P) <= max_len

def v_hour(P):   return allow_numeric_partial(P, 2)
def v_min(P):    return allow_numeric_partial(P, 2)

vcmd_hour = (root.register(v_hour), "%P")
vcmd_min  = (root.register(v_min),  "%P")

hour_spin = tk.Spinbox(
    frame, from_=1, to=12, wrap=True, textvariable=hour_var,
    font=custom_font, width=5, justify="center",
    validate="key", validatecommand=vcmd_hour
)
minute_spin = tk.Spinbox(
    frame, from_=0, to=59, wrap=True, format="%02.0f",
    textvariable=minute_var, font=custom_font, width=5, justify="center",
    validate="key", validatecommand=vcmd_min
)
ampm_spin = tk.Spinbox(
    frame, values=("AM", "PM"), textvariable=ampm_var,
    font=custom_font, width=5, state="readonly", justify="center"
)

hour_spin.grid(row=0, column=0, padx=10)
minute_spin.grid(row=0, column=1, padx=10)
ampm_spin.grid(row=0, column=2, padx=10)

def normalize_hour(*_):
    s = hour_var.get().strip()
    if not s.isdigit():
        hour_var.set("12")
        return
    n = int(s)
    if n < 1: n = 1
    if n > 12: n = 12
    hour_var.set(f"{n:02d}")

def normalize_minute(*_):
    s = minute_var.get().strip()
    if not s.isdigit():
        minute_var.set("00")
        return
    n = int(s)
    if n < 0: n = 0
    if n > 59: n = 59
    minute_var.set(f"{n:02d}")

hour_spin.bind("<FocusOut>", normalize_hour)
minute_spin.bind("<FocusOut>", normalize_minute)

def select_all_on_focus(e):
    e.widget.selection_range(0, "end")
hour_spin.bind("<FocusIn>", select_all_on_focus)
minute_spin.bind("<FocusIn>", select_all_on_focus)

set_lbl_var = tk.StringVar(value="No Alarm Set")
set_lbl = tk.Label(root, textvariable=set_lbl_var, font=("Arial", 14),
                   bg="#222E36", fg="lightgray")
set_lbl.pack(pady=15)

alarm_time = None
alarm_running = False
alarm_thread = None
snooze_minutes = 5

def alarm_beep_loop():
    global alarm_running
    while alarm_running:
        winsound.Beep(2000, 700)
        time.sleep(0.3)

def start_alarm():
    global alarm_running, alarm_thread
    if not alarm_running:
        alarm_running = True
        set_lbl_var.set("⏰ Alarm Ringing!")
        alarm_thread = threading.Thread(target=alarm_beep_loop, daemon=True)
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
        now = datetime.datetime.now()
        snooze_time = now + datetime.timedelta(minutes=snooze_minutes)
        alarm_time = snooze_time.strftime('%I:%M %p')
        set_lbl_var.set(f"Snoozed for {snooze_minutes} minutes")

def set_alarm():
    global alarm_time, alarm_running
    normalize_hour()
    normalize_minute()

    h = hour_var.get()
    m = minute_var.get()
    ap = ampm_var.get().strip()

    if not (h.isdigit() and m.isdigit()):
        messagebox.showerror("Invalid Input", "Hour and Minute must be numbers")
        return

    alarm_time = f"{h}:{m} {ap}"
    alarm_running = False
    set_lbl_var.set(f"Alarm set for {alarm_time}")

def poll_alarm():
    if not alarm_running and alarm_time:
        now = datetime.datetime.now().strftime('%I:%M %p')
        if now == alarm_time:
            start_alarm()
    root.after(500, poll_alarm)

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
poll_alarm()
root.mainloop()
