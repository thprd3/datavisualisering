# denne versjonen inneholder bruk av ekstern API (ssb/oslo kommune)

from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
import requests

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

API_URL = "https://statistikkbanken.oslo.kommune.no/statbank/api/v1/no/db1/Kriminalitet/KRI008.px"

# Fetches and structures crime data for display.
def fetch_crime_data():
    json_payload = {
        "query": [
            {
                "code": "Gjerningsbydel (hovedlovbrudd)",
                "selection": {
                    "filter": "item",
                    "values": ["14"]  # Request data for "Sentrum" (bydel 17)
                }
            },
            {
                "code": "Alder",
                "selection": {
                    "filter": "item",
                    "values": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                }
            }
        ],
        "response": {"format": "json-stat2"}  # Required response format
    }

    response = requests.post(API_URL, json=json_payload)

    if response.status_code != 200:
        return {"error": f"Failed to fetch data: {response.status_code}"}

    data = response.json()

    # Extract useful parts from JSON-STAT response
    extracted_data = []
    if "value" in data:
        values = data["value"]  # The crime data
        dimensions = data["dimension"]

        # Map crime data to readable labels
        age_groups = dimensions["Alder"]["category"]["label"]
        # "Sentrum"
        bydel = dimensions["Gjerningsbydel (hovedlovbrudd)"]["category"]["label"]["14"]

        # Organizing data for display
        for i, (age_key, age_label) in enumerate(age_groups.items()):
            crime_count = values[i]  # Match index with data value
            extracted_data.append(
                {"age_group": age_label, "crimes": crime_count})

    return {
        "title": f"Crime Data for {bydel}",
        "crime_data": extracted_data
    }

@app.route("/crime-chart-data")
def fetch_crime_chart_data():
    data = fetch_crime_data()
    if "error" in data:
        return jsonify(data)
    
    return jsonify({
        "labels": [entry["age_group"] for entry in data["crime_data"]],
        "values": [entry["crimes"] for entry in data["crime_data"]],
    })

@app.route("/crime")
def crime_page():
    data = fetch_crime_data()
    return render_template("crime.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)