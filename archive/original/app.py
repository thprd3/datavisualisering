from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)
db_info = "app.db"

# Fetcher all data SQL-tabellen, og lagrer den som en Pandas DataFrame
def fetch_data():  # tror vi holder oss til bare .sql to begin with
    df = pd.read_csv("data.csv")  # leser csv filen som df (DataFrame)
    conn = sqlite3.connect("app.db")
    # (tablename, connection, if_exists, bool index column (ID column)
    df.to_sql("weather_data", conn, if_exists="replace", index=False)
    data = pd.read_sql("SELECT * FROM weather_data", conn)
    conn.close()
    return data

# Viser index.html og putter inn rådata fra SQL ved hjelp av fetch_data()
@app.route('/')
def index_page():
    df = fetch_data()
    data = df.values.tolist()
    return render_template("index.html", data=data)

@app.route("/temperature-data")
def return_temperature_data():
    df = fetch_data()
    return jsonify({
        "labels": df["date"].tolist(),
        "values": df["temperature"].tolist()
    })

# hakket mer avansert. henter kolonnen "precipitation" fra fetch_data(), lagrer antall rader med samme verdi som en variabel, sender verdien og antallet til frontenden
@app.route("/precipitation-data")
def return_precipitation_data():
    df = fetch_data()
    category_counts = df["precipitation"].value_counts().to_dict()
    return jsonify({
        "labels": list(category_counts.keys()),
        "values": list(category_counts.values()),
    })

if __name__ == '__main__':
    app.run(debug=True)