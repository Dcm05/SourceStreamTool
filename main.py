from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Path to the folder where text files are stored
TEXT_FOLDER = os.path.join(os.path.dirname(__file__), 'Text Files')
os.makedirs(TEXT_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist

# Define the fields and their default values
FIELDS = {
    "player1_name": "Player 1",
    "player2_name": "Player 2",
    "player1_score": "0",
    "player2_score": "0",
    "commentator1": "Commentator 1",
    "commentator2": "Commentator 2",
    "round": "Winners Round 1",
    "bestof": "3"
}

@app.route('/')
def index():
    data = {}
    for key, default in FIELDS.items():
        file_path = os.path.join(TEXT_FOLDER, f"{key}.txt")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                if key == "bestof":
                    for i in f.read().strip():
                        if i == "1" or i == "3" or i == "5" or i == "7" or i == "9":
                             data[key] = i
                else:
                    data[key] = f.read().strip()
        except FileNotFoundError:
            data[key] = default
    return render_template("index.html", data=data)

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    try:
        for key, value in data.items():
            file_path = os.path.join(TEXT_FOLDER, f"{key}.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                if key == "bestof":
                
                    f.write("Best of " +value)
                else:
                    f.write(value)
        return jsonify({"message": "Data saved successfully!"})
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=False)
