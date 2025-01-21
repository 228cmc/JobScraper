from config import JOB_URL, USERNAME, PASSWORD
from scraper.scraper import scrape_jobs
from db.database import create_tables, save_to_database, export_to_csv

def main():
    """
    Main function to scrape jobs, save to the database, and export to a CSV file.
    """
    if not all([JOB_URL, USERNAME, PASSWORD]):
        print("Missing some configuration values in the environment variables.")
        return

    print("Starting the job scraper...")
    jobs = scrape_jobs(JOB_URL, USERNAME, PASSWORD)  # Scrape jobs and return a list of dictionaries

    print("Initializing database...")
    create_tables()  # Create tables if not already created

    print("Saving jobs to the database...")
    save_to_database(jobs)  # Save the jobs into the database

    print("Exporting jobs to CSV...")
    export_to_csv()  # Export jobs from the database to a CSV file

    print("Done! Jobs are saved and exported to CSV.")

if __name__ == "__main__":
    main()
