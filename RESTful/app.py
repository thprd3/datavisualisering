from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Oppsett av SQLite-database
def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    # Opprett tabell for værdata
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            temperature REAL NOT NULL
        )
    """)
    
    # Opprett tabell for testdata
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            header TEXT,
            message TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Server index.html når brukeren går til rot (/)
@app.route("/")
def index():
    return render_template("index.html")

# Sender eksempeldata for oppgave 2
@app.route("/examples", methods=["GET"])
def get_examples():
    example_data = {
        "message": "Du klarte det!",
        "items": ["eple", "pære", "banan"]
    }
    return jsonify(example_data)

# Hent værdata fra databasen (oppgave 2)
@app.route("/weather", methods=["GET"])
def get_weather():
    date_filter = request.args.get("date")  # Get ?date=YYYY-MM-DD from the URL
    
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    if date_filter:
        cursor.execute("SELECT id, date, temperature FROM weather WHERE date = ?", (date_filter,))
    else:
        cursor.execute("SELECT date, temperature FROM weather")
        
    rows = cursor.fetchall()  # Henter alle rader fra databasen
    conn.close()

    data = []

    for row in rows:
        entry = {
            "date": row[0],  # Første kolonne (header)
            "temperature": row[1]   # Andre kolonne (message)
        }
        data.append(entry)  # Legger til i listen
    
    
    return jsonify(data) # jsonify() konverterer dataen til JSON

# Legg til en ny temperaturmåling (oppgave 4)
@app.route("/weather", methods=["POST"])
def create_weather():
    data = request.get_json()
    
    if not data or "date" not in data or "temperature" not in data:
        return jsonify({"error": "Invalid data format"}), 400
    
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weather (date, temperature) VALUES (?, ?)", (data["date"], data["temperature"]))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Temperature added successfully"})

# Hent testdata fra databasen (oppgave 4)
@app.route("/tests", methods=["GET"])
def get_test():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT header, message FROM test_data")
    rows = cursor.fetchall()  # Henter alle rader fra databasen

    data = []

    for row in rows:
        entry = {
            "header": row[0],  # Første kolonne (header)
            "message": row[1]   # Andre kolonne (message)
        }
        data.append(entry)  # Legger til i listen
    
    conn.close()
    
    return jsonify(data)

# Send dummy-testdata med POST-request (oppgave 4)
@app.route("/tests", methods=["POST"])
def create_test():
    data = request.get_json()
    if not data or "header" not in data or "message" not in data:
        return jsonify({"error": "Feil data format"}), 400
    
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_data (header, message) VALUES (?, ?)", (data["header"], data["message"]))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Test data saved successfully"})

# Start appen og initialiser database
if __name__ == "__main__":
    init_db()
    app.run(debug=True)