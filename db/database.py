import sqlite3

def create_database():
    conn = sqlite3.connect("db/jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE
        );
    """)
    conn.commit()
    conn.close()

def save_to_database(title, company, location, link):
    conn = sqlite3.connect("db/jobs.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO jobs (title, company, location, link)
            VALUES (?, ?, ?, ?)
        """, (title, company, location, link))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Job already exists in database: {title}")
    finally:
        conn.close()
