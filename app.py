
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("database/disaster.db")

def create_table():
    with connect_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disaster_type TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            )
        """)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        disaster = request.form["disaster"]
        location = request.form["location"]
        description = request.form["description"]

        with connect_db() as db:
            db.execute(
                "INSERT INTO reports "
                "(disaster_type, location, description) "
                "VALUES (?, ?, ?)",
                (disaster, location, description)
            )

        return redirect("/")

    with connect_db() as db:
        reports = db.execute(
            "SELECT * FROM reports ORDER BY id DESC"
        ).fetchall()

    return render_template_string("""
    <h1>DisasterShield</h1>
    <h2>Disaster Reporting System</h2>

    <form method="POST">
        <input name="disaster" placeholder="Disaster type" required>
        <input name="location" placeholder="Location" required>
        <textarea name="description"
                  placeholder="Describe the disaster"
                  required></textarea>
        <button type="submit">Submit Report</button>
    </form>

    <h2>Reported Disasters</h2>
    {% for r in reports %}
        <p>
            <b>{{ r[1] }}</b> - {{ r[2] }}<br>
            {{ r[3] }}<br>
            Status: {{ r[4] }}
        </p>
        <hr>
    {% endfor %}
    """, reports=reports)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
