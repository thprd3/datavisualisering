# denne filen fyller app.db med testdata
import sqlite3

def populate_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # Slett eksisterende data (valgfritt, for å unngå duplikater)
    cursor.execute("DELETE FROM weather")
    cursor.execute("DELETE FROM test_data")

    # Sett inn testdata for værdata
    weather_data = [
        ("2024-02-20", 3.5),
        ("2024-02-21", 4.0),
        ("2024-02-22", 2.8),
        ("2024-02-23", 5.2),
        ("2024-02-24", 6.1)
    ]
    cursor.executemany("INSERT INTO weather (date, temperature) VALUES (?, ?)", weather_data)

    # Sett inn testdata for test_data-tabellen
    test_data = [
        ("Test 1", "Dette er en testmelding"),
        ("Test 2", "Enda en testmelding"),
        ("Info", "Database fungerer!")
    ]
    cursor.executemany("INSERT INTO test_data (header, message) VALUES (?, ?)", test_data)

    # Lagre og lukk forbindelsen
    conn.commit()
    conn.close()
    print("Testdata lagt inn i databasen")

# Kjør funksjonen hvis scriptet kjøres direkte
if __name__ == "__main__":
    populate_db()
