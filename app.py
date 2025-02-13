from flask import Flask, render_template, request, session, flash, redirect
from dotenv import load_dotenv
import os
import sqlite3
import bcrypt

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY", "default_key") # parameter 1 = nøkkel i .env, parameter 2 = fallback-verdi. kalles ODP :)
db_info = os.getenv("DATABASE_INFO", "foo.db")

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

@app.errorhandler(404)
def not_found():
    return render_template('404.html'), 404

@app.errorhandler(500)
def RIP_server():
    return "diesofcringe", 500

@app.context_processor # dette kjører før template renderes, er tilgjengelig på alle ruter
def current_user():
    return {
        "current_user": session.get("user"),
        "current_role": session.get("role")
    }

@app.cli.command("reset") # kjører med flask reset
def reset():
    if os.path.exists(db_info):
        os.remove(db_info)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) # bcrypt trenger passord som bytes, ikke tekst

def register_user(username, password, role):
    with sqlite3.connect(db_info) as conn:
        cursor = conn.cursor()
        sql = 'SELECT * FROM users WHERE username = ?'
        cursor.execute(sql, (username,)) # må sende tuple selv om bare 1 verdi
        if cursor.fetchone():
            flash(f"Username '{username}' already in use!")
            return redirect('/register'), 409 # 409 = conflict
        else:
            hashed_password = hash_password(password)
            if role == "admin":
                sql = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
                cursor.execute(sql, (username, hashed_password, role))
            else:
                sql = "INSERT INTO users (username, password) VALUES (?, ?)"
                cursor.execute(sql, (username, hashed_password))
            conn.commit()
            flash(f"User '{username}' of role '{role}' registered.")
            return redirect ('/login')

def login_user(username, password):
    with sqlite3.connect(db_info) as conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM users WHERE username = ?"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        
        if result:
            hash = result[2] # id, username, password
            if bcrypt.checkpw(password.encode('utf-8'), hash):
                session["user"] = username
                session["role"] = result[3]
                return redirect('/login')
            else:
                return "Invalid password", 401
        else: 
            flash(f"No user found with username '{username}' and the provided password.")
            return redirect('/login'), 401

def soft_delete_user(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE username = ?"
    cursor.execute(sql, (username,))
    if cursor.fetchone():
        sql = "UPDATE users SET is_active = 'no' WHERE username = ?"
        cursor.execute(sql, (username))
        conn.commit()
        conn.close()
        return render_template("home.html", message=f"User '{username}' has been soft deleted.")
    else:
        conn.close()
        return render_template("delete.html", message=f"No user found with username '{username}'.")

@app.route('/')
def index_page():
    return redirect('/login')

@app.route('/register', methods=["GET", "POST"])
def register_page():
    print(f"{request.method} received at {request.path}")
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        return register_user(username, password, role)

@app.route('/login', methods=["GET", "POST"])
def login_page():
    print(f"{request.method} received at {request.path}")
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        return login_user(username, password)

@app.route('/logout')
def logout():
    session.pop("user", None) #fjerner nøkkelen hvis den finnes, men gjør ingenting hvis den ikke eksisterer. "Optional Default Parameter", veldig Python-idiomatisk
    session.pop("role", None)
    return redirect('/login')

@app.route("/admin")
def admin_page():
    if session.get("role") == "admin":   
        with sqlite3.connect(db_info) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            users = cursor.fetchall()
            return render_template("admin.html", users = users)
    else:
        flash("Only admins can access /admin")
        return redirect('/login'), 403 # 403 = forbidden

@app.route("/profile")
def user_page():
    if "user" in session:
        with sqlite3.connect(db_info) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM users WHERE username = ?"
            cursor.execute(sql, (session.get("user"),))
            user_info = cursor.fetchone()
            return render_template("profile.html", user_info = user_info)
    else: 
        flash("Must be logged in to access /profile")
        return redirect("/login"), 403

@app.route("/delete", methods=["GET", "POST"])
def delete_page():
    if request.method=="GET": 
        if session.get("role") == "admin":
            return render_template("delete.html")
        else:
            return render_template("home.html", message="Only admins can access /delete.")
    elif request.method=="POST":
        username = request.form.get("username")
        return soft_delete_user(username)

if __name__ == '__main__':
    app.run()