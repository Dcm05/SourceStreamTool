from flask import Flask, render_template, request, redirect
import os
import sys
import traceback

app = Flask(__name__)

if getattr(sys, "frozen", False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

def get_file_path(filename):
    return os.path.join(base_dir, filename)

def read_or_default(filename, default=""):
    try:
        with open(get_file_path(filename), "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return default

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Try to read JSON first
            form_data = request.get_json()
            if not form_data:
                # Fallback to form (in case JSON is missing)
                form_data = request.form

            print("Form data received:")
            for key, value in form_data.items():
                print(f"  {key} = {value}")
                path = get_file_path(f"{key}.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(value))

            return "", 204  # No content response
        except Exception as e:
            print("=== ERROR WHILE SAVING ===")
            traceback.print_exc()
            return f"Error saving data: {e}", 500
        
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
    app.run(debug=True)


    