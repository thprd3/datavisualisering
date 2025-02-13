from flask import Flask, render_template
import os
import sqlite3

app = Flask(__name__)
db_info = "app.db"

def init_db():
    with sqlite3.connect(db_info) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS 'users' (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT NOT NULL, 
                        password TEXT NOT NULL,
                        role TEXT default 'user',
                        is_active TEXT default 'yes')
                    '''
        )

init_db()

@app.cli.command("reset") # kjører med flask reset
def reset():
    if os.path.exists(db_info):
        os.remove(db_info)

@app.route('/')
def index_page():
    with sqlite3.connect(db_info) as conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        users = cursor.fetchall()
        return render_template("index.html")

if __name__ == '__main__':
    app.run()