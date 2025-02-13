from flask import Flask, render_template, redirect, request, session, flash
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key=("test123") # denne trenger vi for å bruke sessions

@app.context_processor
def current_user():
    return dict(username=session.get("username"), role=session.get("role"))
    
@app.errorhandler(404)
def not_found(error_code):
    return render_template('404.html'), 404

def start_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'user', is_active TEXT NOT NULL DEFAULT 'yes')"
    cursor.execute(sql)
    conn.commit()
    conn.close()

def test_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO users (username, password) VALUES ('Simen', 'da_goat')"
        cursor.execute(sql)
        sql = "INSERT INTO users (username, password) VALUES ('Simen_', 'not_da_goat')"
        cursor.execute(sql)
        sql = "INSERT INTO users (username, password, role) VALUES ('Simen_admin', 'admin123', 'admin')"
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return "bruker allerede opprettet"

start_db()
# test_db()

def hash_password(password):
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())

def login_user(username, password):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE username = ?"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    if result:
        hash = result[1]
        if bcrypt.checkpw(password.encode('utf-8'), hash):
            session["username"]=username
            session["role"]=result[2]
            conn.close()
            return render_template("home.html", message=username)
        else:
            return render_template("home.html", message="ERROR: wrong password entered")
    else:
        conn.close
        return render_template("home.html", message=f"Bruker med brukernavn '{username}' ikke funnet.")

def register_user(username, password, role):
    password = hash_password(password)
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    if role == "admin":
        sql = "INSERT INTO users (username, password, role) VALUES (?, ?, 'admin')"
    else: 
        sql = "INSERT INTO users (username, password) VALUES (?, ?)"
    cursor.execute(sql, (username, password))
    conn.commit()
    conn.close()
    return render_template("home.html", logged_in_user=f"Bruker med brukernavn {username} ble registrert")

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

@app.route("/")
def root_page():
    return render_template("home.html")

@app.route("/home")
def home_page():
    return render_template("home.html", message="test")

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method=="GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        return register_user(username, password, role)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method=="GET":
        if session.get("username"):
            # flash("Du er allerede logget inn.")
            return render_template("login.html", current_user=session.get("username"))
        else:
            return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        return login_user(username, password)

@app.route("/admin")
def admin_page():
    if session["role"] == "admin":
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        conn.close()
        return render_template('admin.html', users=result)
    else:
        return render_template('home.html', message="ERROR: kunne admins kan gå til /admin"), 401

@app.route("/profile")
def profile_page():
    if session.get("username"):
        return render_template("profile.html")
    else:
        return render_template("home.html", logged_in_user="Du må være logget inn for å se profil")
    
@app.route("/logout")
def logout_user():
    session.pop("username", None)
    session.pop("role", None)
    return redirect("/login")

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

if __name__ =="__main__":
    app.run(debug=True, port=3700, host="0.0.0.0")