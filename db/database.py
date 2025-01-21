import sqlite3
import csv

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
            link TEXT NOT NULL UNIQUE
        );
    """)
    connection.commit()
    connection.close()

def save_to_database(jobs):
    """
    Saves jobs to the database, avoiding duplicates.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for job in jobs:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO jobs (title, company, location, link)
                VALUES (?, ?, ?, ?);
            """, (job['title'], job['company'], job['location'], job['link']))
        except sqlite3.Error as e:
            print(f"Error al guardar el trabajo: {e}")

    connection.commit()
    connection.close()

def export_to_csv(file_path="jobs_export.csv"):
    """
    Exports the jobs table to a CSV file.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM jobs;")
    jobs = cursor.fetchall()
    connection.close()

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Title", "Company", "Location", "Link"])
        writer.writerows(jobs)

    print(f"Jobs exported to {file_path}")
