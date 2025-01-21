from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)  # Initializes the Flask application

# Path to the SQLite database
DB_PATH = os.path.join("db", "jobs.db")

@app.route("/")
def index():
    """
    Displays the jobs stored in the database on the home page.
    """
    connection = sqlite3.connect(DB_PATH)  # Connects to the SQLite database
    cursor = connection.cursor()
    cursor.execute("SELECT title, company, location, link FROM jobs;")  # Query to retrieve job details
    jobs = cursor.fetchall()  # Fetches all rows from the query
    connection.close()  # Closes the database connection
    return render_template("index.html", jobs=jobs)  # Renders the `index.html` template with jobs data

@app.route("/refresh")
def refresh():
    """
    Refreshes the database by running the scraper.
    """
    from main import main  # Dynamically imports the `main()` function
    main()  # Runs the scraping process and updates the database
    return "The jobs database has been successfully updated."  # Confirmation message

if __name__ == "__main__":
    app.run(debug=True)  # Starts the Flask application in debug mode
