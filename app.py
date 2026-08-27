from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "careertrack.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            location TEXT,
            job_type TEXT,
            salary TEXT,
            applied_date TEXT,
            status TEXT NOT NULL,
            job_url TEXT,
            contact_person TEXT,
            interview_date TEXT,
            follow_up_date TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


init_db()

@app.route("/")
def home():

    conn = get_db_connection()

    # Get all applications
    applications = conn.execute("""
        SELECT *
        FROM applications
        ORDER BY created_at DESC
    """).fetchall()

    # Total applications
    total = conn.execute("""
        SELECT COUNT(*)
        FROM applications
    """).fetchone()[0]

    # Applied
    applied = conn.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Applied'
    """).fetchone()[0]

    # Interviews
    interviews = conn.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Interview'
    """).fetchone()[0]

    # Pending
    pending = conn.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Pending'
    """).fetchone()[0]

    # Selected
    selected = conn.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Selected'
    """).fetchone()[0]

    # Rejected
    rejected = conn.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Rejected'
    """).fetchone()[0]

    # Active applications
    active = total - selected - rejected

    # Success rate
    if total > 0:
        success_rate = round((selected / total) * 100)
    else:
        success_rate = 0
            # Upcoming interviews
    upcoming_interviews = conn.execute("""
        SELECT *
        FROM applications
        WHERE interview_date IS NOT NULL
        AND interview_date != ''
        ORDER BY interview_date ASC
        LIMIT 5
    """).fetchall()

    # Upcoming follow-ups
    upcoming_followups = conn.execute("""
        SELECT *
        FROM applications
        WHERE follow_up_date IS NOT NULL
        AND follow_up_date != ''
        ORDER BY follow_up_date ASC
        LIMIT 5
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        applications=applications,
        total=total,
        applied=applied,
        interviews=interviews,
        pending=pending,
        selected=selected,
        rejected=rejected,
        active=active,
        success_rate=success_rate,
        upcoming_interviews=upcoming_interviews,
        upcoming_followups=upcoming_followups
    )

@app.route("/add", methods=["GET", "POST"])
def add_application():

    if request.method == "POST":

        company = request.form["company"]
        position = request.form["position"]
        location = request.form["location"]
        job_type = request.form["job_type"]
        salary = request.form["salary"]
        applied_date = request.form["applied_date"]
        status = request.form["status"]
        job_url = request.form["job_url"]
        contact_person = request.form["contact_person"]
        interview_date = request.form["interview_date"]
        follow_up_date = request.form["follow_up_date"]
        notes = request.form["notes"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO applications (
                company, position, location, job_type, salary,
                applied_date, status, job_url, contact_person,
                interview_date, follow_up_date, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            company, position, location, job_type, salary,
            applied_date, status, job_url, contact_person,
            interview_date, follow_up_date, notes
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_application.html")
@app.route("/applications")
def applications():

    conn = get_db_connection()

    applications = conn.execute("""
        SELECT *
        FROM applications
        ORDER BY created_at DESC
    """).fetchall()

    conn.close()

    return render_template(
        "applications.html",
        applications=applications
    )
@app.route("/delete/<int:application_id>")
def delete_application(application_id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/applications")
@app.route("/edit/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):

    conn = get_db_connection()

    if request.method == "POST":

        company = request.form["company"]
        position = request.form["position"]
        location = request.form["location"]
        job_type = request.form["job_type"]
        salary = request.form["salary"]
        applied_date = request.form["applied_date"]
        status = request.form["status"]
        job_url = request.form["job_url"]
        contact_person = request.form["contact_person"]
        interview_date = request.form["interview_date"]
        follow_up_date = request.form["follow_up_date"]
        notes = request.form["notes"]

        conn.execute("""
            UPDATE applications
            SET company = ?,
                position = ?,
                location = ?,
                job_type = ?,
                salary = ?,
                applied_date = ?,
                status = ?,
                job_url = ?,
                contact_person = ?,
                interview_date = ?,
                follow_up_date = ?,
                notes = ?
            WHERE id = ?
        """, (
            company, position, location, job_type, salary,
            applied_date, status, job_url, contact_person,
            interview_date, follow_up_date, notes,
            application_id
        ))

        conn.commit()
        conn.close()

        return redirect("/applications")

    application = conn.execute("""
        SELECT *
        FROM applications
        WHERE id = ?
    """, (application_id,)).fetchone()

    conn.close()

    if application is None:
        return "Application not found", 404

    return render_template(
        "edit_application.html",
        application=application
    )
@app.route("/upcoming")
def upcoming():

    conn = get_db_connection()

    interviews = conn.execute("""
        SELECT *
        FROM applications
        WHERE interview_date IS NOT NULL
        AND interview_date != ''
        ORDER BY interview_date ASC
    """).fetchall()

    follow_ups = conn.execute("""
        SELECT *
        FROM applications
        WHERE follow_up_date IS NOT NULL
        AND follow_up_date != ''
        ORDER BY follow_up_date ASC
    """).fetchall()

    conn.close()

    return render_template(
        "upcoming.html",
        interviews=interviews,
        follow_ups=follow_ups
    )
@app.route("/settings")
def settings():
    return render_template("settings.html")
if __name__ == "__main__":
    app.run(debug=True)