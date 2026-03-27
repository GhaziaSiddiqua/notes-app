from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

def get_db():
    return sqlite3.connect("database.db")

@app.route('/')
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# SIGNUP
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()

        return redirect("/login")

    return render_template("signup.html")

# LOGIN
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")

# 🔥 UPDATED DASHBOARD (THIS IS THE MAIN CHANGE)
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    db = get_db()

    # SAVE NOTE
    if request.method == "POST":
        note = request.form["note"]
        db.execute(
            "INSERT INTO notes (user, content) VALUES (?, ?)",
            (session["user"], note)
        )
        db.commit()

    # FETCH NOTES
    notes = db.execute(
        "SELECT content FROM notes WHERE user=?",
        (session["user"],)
    ).fetchall()

    return render_template("dashboard.html", notes=notes, user=session["user"])

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)