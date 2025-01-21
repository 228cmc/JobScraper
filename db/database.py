import sqlite3
import csv
from datetime import datetime, timedelta

DB_PATH = "db/jobs.db"

def create_tables():
    """
    Creates the necessary tables if they don't exist.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            salary TEXT,
            expected_commencement TEXT,
            applications_close_on TEXT,
            original_applications_close_on TEXT,
            link TEXT NOT NULL UNIQUE
        );
    """)
    connection.commit()
    connection.close()

def add_original_date_column():
    """
    Adds a column to store the original applications close date if it doesn't exist.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    try:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN original_applications_close_on TEXT;
        """)
        print("Column 'original_applications_close_on' added.")
    except sqlite3.OperationalError:
        print("Column 'original_applications_close_on' already exists.")
    connection.commit()
    connection.close()

def format_date(date_str):
    """
    Converts a date string in various formats to YYYY-MM-DD.
    """
    try:
        return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")
        except ValueError:
            try:
                return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                return None

def save_to_database(jobs):
    """
    Saves jobs to the database, avoiding duplicates.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for job in jobs:
        try:
            original_close_date = job.get('applications_close_on', 'Not listed')
            formatted_close_date = format_date(original_close_date) if original_close_date != 'Not listed' else None

            cursor.execute("""
                INSERT OR IGNORE INTO jobs (
                    title, company, location, salary, expected_commencement,
                    applications_close_on, original_applications_close_on, link
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                job['title'],
                job['company'],
                job['location'],
                job.get('salary', 'Not listed'),
                job.get('expected_commencement', 'Not listed'),
                formatted_close_date or 'Not listed',
                original_close_date,
                job['link']
            ))
        except sqlite3.Error as e:
            print(f"Error saving job: {e}")

    connection.commit()
    connection.close()

def export_to_csv(file_path="jobs_export.csv"):
    """
    Exports the jobs table to a CSV file.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, company, location, salary, expected_commencement,
               applications_close_on, original_applications_close_on, link
        FROM jobs
        ORDER BY applications_close_on;
    """)
    jobs = cursor.fetchall()
    connection.close()

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Title", "Company", "Location", "Salary", "Expected Commencement", "Applications Close On", "Original Close Date", "Link"])
        writer.writerows(jobs)

    print(f"Jobs exported to {file_path}")

def get_all_jobs():
    """
    Retrieves all jobs from the database, ordered by applications_close_on.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT title, company, location, salary, expected_commencement,
               applications_close_on, original_applications_close_on, link
        FROM jobs
        ORDER BY applications_close_on;
    """)
    jobs = cursor.fetchall()
    connection.close()
    return jobs

def get_closing_soon_jobs(days=7):
    """
    Retrieves jobs that are closing within the next `days` days.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT title, company, location, salary, expected_commencement,
               applications_close_on, original_applications_close_on, link
        FROM jobs
        WHERE applications_close_on BETWEEN ? AND ?
        ORDER BY applications_close_on;
    """, (current_date, end_date))
    jobs = cursor.fetchall()
    connection.close()
    return jobs

def get_jobs_grouped_by_company():
    """
    Retrieves jobs grouped by company from the database.
    Returns a dictionary where the keys are company names and the values are lists of jobs.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT company, title, location, salary, expected_commencement,
               applications_close_on, original_applications_close_on, link
        FROM jobs
        ORDER BY company, applications_close_on;
    """)
    rows = cursor.fetchall()
    connection.close()

    grouped_jobs = {}
    for row in rows:
        company = row[0]
        job_data = {
            "title": row[1],
            "location": row[2],
            "salary": row[3],
            "expected_commencement": row[4],
            "applications_close_on": row[5],
            "original_applications_close_on": row[6],
            "link": row[7]
        }
        if company not in grouped_jobs:
            grouped_jobs[company] = []
        grouped_jobs[company].append(job_data)

    return grouped_jobs
