from flask import Flask, render_template, request, redirect
import os
import sys
import winshell
from win32com.client import Dispatch
import traceback

app = Flask(__name__)

# Determine base directory for script or EXE
if getattr(sys, "frozen", False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Create and use a dedicated folder for text files
TEXT_FILES_FOLDER = os.path.join(base_dir, "Text Files")
os.makedirs(TEXT_FILES_FOLDER, exist_ok=True)

def get_file_path(filename):
    return os.path.join(TEXT_FILES_FOLDER, filename)

def read_or_default(filename, default=""):
    try:
        with open(get_file_path(filename), "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return default

def create_shortcut():
    shortcut_path = os.path.join(base_dir, "Stream Controller.lnk")
    icon_path = os.path.join(base_dir, "static", "logo.ico")
    if os.path.exists(icon_path):
        shortcut.IconLocation = icon_path


    if not os.path.exists(shortcut_path):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = os.path.join(os.environ["WINDIR"], "System32", "cmd.exe")
        shortcut.Arguments = '/c start http://localhost:5000/'
        shortcut.IconLocation = icon_path if os.path.exists(icon_path) else ""
        shortcut.WindowStyle = 1
        shortcut.Description = "Stream Controller"
        shortcut.WorkingDirectory = base_dir
        shortcut.save()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            form_data = request.get_json()
            if not form_data:
                form_data = request.form

            for key, value in form_data.items():
                path = get_file_path(f"{key}.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(value))

            return "", 204
        except Exception as e:
            print("=== ERROR WHILE SAVING ===")
            traceback.print_exc()
            return f"Error saving data: {e}", 500

    # Handle GET — load data
    data = {
        "player1": read_or_default("player1.txt", "Player 1"),
        "player2": read_or_default("player2.txt", "Player 2"),
        "score1": read_or_default("score1.txt", "0"),
        "score2": read_or_default("score2.txt", "0"),
        "round": read_or_default("round.txt", "Winners Round 1"),
        "bestof": read_or_default("bestof.txt", "5"),
        "commentator1": read_or_default("commentator1.txt", "Commentator 1"),
        "commentator2": read_or_default("commentator2.txt", "Commentator 2"),
    }
    return render_template("index.html", **data)

if __name__ == "__main__":
    create_shortcut()
    app.run(debug=True)