# 🕰️ Alarm Clock (Python GUI)

A simple and stylish **Alarm Clock** built with **Python (Tkinter)**.  
This app displays the current time, lets you set an alarm, snooze it, and stop it — with a continuous ringing alarm sound until dismissed.

---

## 🚀 Features

- 📅 **Live Time Display** – Updates every second in 12-hour format with AM/PM.  
- ⏰ **Set Alarm** – Choose **hour, minute, and AM/PM** using spinboxes.  
- 🎵 **Continuous Ringing Alarm** – Beeps continuously until stopped or snoozed.  
- 😴 **Snooze Option** – Snooze the alarm for 5 minutes with one click.  
- 🛑 **Stop Alarm** – Immediately stops the ringing and clears the alarm.  
- ✅ **Input Validation** – Ensures hours (1–12) and minutes (0–59) are valid, auto-corrects on focus-out.  

---

## 🖥️ UI Preview
- Top: Current Time Display  
- Middle: Alarm Set Section (Hour, Minute, AM/PM spinboxes)  
- Bottom: **Set Alarm**, **Stop Alarm**, and **Snooze** buttons  

---

## 🛠️ Requirements

- Python 3.x  
- Works on **Windows** (uses `winsound` for alarm sound).  
  > On Linux/Mac, you’ll need to replace the alarm sound function with another method (e.g., `playsound`).  

Install required libraries (Tkinter is built-in with Python):  
```bash
pip install tk
```

## ▶️ How to Run

1. Clone this repository:
```bash
git clone https://github.com/yourusername/alarm-clock-gui.git
```
```bash
cd alarm-clock-gui
```
2. Run the script:
```bash
python alarm_clock.py
```

## 📷 Example
<img width="422" height="552" alt="image" src="https://github.com/user-attachments/assets/dea1e4f9-b709-45b6-b3ab-dbb1e43d8ac2" />

## 📌 Notes

- Default snooze is set to 5 minutes (can be changed in code).

- Alarm runs on a background thread so the UI stays responsive.

- Input fields are user-friendly:

- Hours: 1–12

- Minutes: 00–59 (auto zero-padded)

- AM/PM: Read-only

## 🤝 Contribution

- Feel free to fork this project and add features like:

- Custom snooze time

- Different/ custom alarm sounds

- Save multiple alarms
