from flask import Flask, render_template, request
from db.database import (
    create_tables,
    get_all_jobs,
    get_closing_soon_jobs,
    get_jobs_grouped_by_company,
)

app = Flask(__name__)

@app.route("/")
def index():
    """
    Displays all jobs stored in the database, ordered by application close date.
    """
    jobs = get_all_jobs()  # Fetch all jobs from the database
    return render_template("index.html", jobs=jobs)  # Render the main view

@app.route("/closing-soon")
def closing_soon():
    """
    Displays jobs that are closing soon (default: within 7 days).
    """
    days = request.args.get("days", default=7, type=int)
    jobs = get_closing_soon_jobs(days=days)
    return render_template("index.html", jobs=jobs)

@app.route("/grouped-by-company")
def grouped_by_company():
    """
    Displays jobs grouped by company.
    """
    grouped_jobs = get_jobs_grouped_by_company()
    return render_template("grouped.html", grouped_jobs=grouped_jobs)

@app.route("/refresh")
def refresh():
    """
    Refreshes the database by running the scraper and updates the job listings.
    """
    from main import main
    main()
    return "The jobs database has been successfully updated."

if __name__ == "__main__":
    create_tables()  # Ensure tables exist before starting the app
    app.run(debug=True)
