import os
import cv2
import numpy as np
import pandas as pd
import json
from datetime import datetime, time
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACES_DIR = os.path.join(BASE_DIR, "static", "faces")
ATT_DIR = os.path.join(BASE_DIR, "Attendance")

if not os.path.exists(FACES_DIR):
    os.makedirs(FACES_DIR)
if not os.path.exists(ATT_DIR):
    os.makedirs(ATT_DIR)

# -------------------------------
# Attendance configuration
# -------------------------------
OFFICIAL_LOGIN_TIME = time(9, 0)   # 9:00 AM official start
LATE_THRESHOLD = time(9, 15)       # After 9:15 AM marked Late

# -------------------------------
# Home Page
# -------------------------------
@app.route('/')
def index():
    # Load latest attendance file if exists
    today = datetime.now().strftime("%Y-%m-%d")
    att_file = os.path.join(ATT_DIR, f"Attendance_{today}.csv")

    if os.path.exists(att_file):
        attendance = pd.read_csv(att_file).to_dict(orient="records")
    else:
        attendance = []

    return render_template('index.html', attendance=attendance)


# -------------------------------
# Route: Save login time and mark status
# -------------------------------
@app.route('/set_login_time', methods=['POST'])
def set_login_time_route():
    name = request.form.get('name')
    login_time_str = datetime.now().strftime("%H:%M:%S")
    login_time = datetime.strptime(login_time_str, "%H:%M:%S").time()

    # Determine status
    if login_time <= OFFICIAL_LOGIN_TIME:
        status = "Present"
    elif login_time <= LATE_THRESHOLD:
        status = "Late"
    else:
        status = "Absent"

    today = datetime.now().strftime("%Y-%m-%d")
    att_file = os.path.join(ATT_DIR, f"Attendance_{today}.csv")

    # Create new file if not exists
    if not os.path.exists(att_file):
        df = pd.DataFrame(columns=["Name", "Login Time", "Status"])
        df.to_csv(att_file, index=False)

    # Load and update attendance
    df = pd.read_csv(att_file)

    # Update if already marked
    if name in df["Name"].values:
        df.loc[df["Name"] == name, ["Login Time", "Status"]] = [login_time_str, status]
    else:
        df.loc[len(df)] = [name, login_time_str, status]

    df.to_csv(att_file, index=False)

    flash(f"{name} marked as {status} at {login_time_str}.", "info")
    return redirect(url_for('index'))


# -------------------------------
# Route: Download attendance file
# -------------------------------
@app.route('/download/<date>')
def download_attendance(date):
    filename = f"Attendance_{date}.csv"
    path = os.path.join(ATT_DIR, filename)
    if os.path.exists(path):
        return send_from_directory(ATT_DIR, filename, as_attachment=True)
    else:
        flash("Attendance file not found for that date!", "warning")
        return redirect(url_for('index'))


# -------------------------------
# Run app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)

