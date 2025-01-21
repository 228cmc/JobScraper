# JobScraper

## Overview

JobScraper is a Python-based project designed to scrape job postings from the MyFuture job portal, save the data in a SQLite database, and provide a web interface using Flask to view and manage the scraped job postings. Additionally, the job data can be exported to a CSV file for further use.



## Features

- **Automated Job Scraping**: Logs into MyFuture, searches for jobs based on user-defined parameters, and retrieves job details.
- **Database Management**: Stores the scraped job data in a SQLite database (`db/jobs.db`).
- **CSV Export**: Exports job data to a CSV file (`jobs_export.csv`) for easy sharing and analysis.
- **Web Interface**: Provides a Flask-based web interface to view job postings and refresh the database with new job postings.



## Project Structure

```
JobScraper/
├── db/
│   ├── database.py         # Database management functions (e.g., create, save, export)
│   ├── jobs.db             # SQLite database storing job postings
├── scraper/
│   ├── scraper.py          # Web scraper for fetching job data
├── templates/
│   ├── index.html          # HTML template for displaying job postings
├── tests/                  # Placeholder for future unit tests
├── venv/                   # Virtual environment (dependencies installed here)
├── .env                    # Environment variables (e.g., credentials, config)
├── .env_example            # Example of environment variables file
├── .gitignore              # Git ignore file
├── app.py                  # Flask application for the web interface
├── config.py               # Configuration file for environment variables
├── jobs_export.csv         # Exported CSV file with job data
├── main.py                 # Main script to run the scraper and database operations
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
```



## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/228cmc/JobScraper.git
   cd JobScraper
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create and configure the `.env` file**:
   Copy the `.env_example` file to `.env` and update the necessary variables:
   ```env
   USERNAME=your_username
   PASSWORD=your_password
   JOB_URL=https://myfuture.bath.ac.uk/students/jobs
   KEYWORDS=Intern
   CONTRACT_HOURS=Full-time
   LOCATION=Anywhere
   ```

5. **Run the scraper**:
   ```bash
   python main.py
   ```

6. **Start the Flask web server**:
   ```bash
   python app.py
   ```

   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to view the job postings.



## Usage

### Running the Scraper

The scraper fetches job postings from the MyFuture portal and saves them in the SQLite database. It can be executed via `main.py`.

### Viewing Jobs in the Web Interface

- Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to view job postings.
- Click the `/refresh` button to fetch the latest job postings and update the database.



## Expected Output

### CSV File (`jobs_export.csv`)

After running the scraper, a CSV file named `jobs_export.csv` will be generated. The file will contain job data in the following format:

| ID  | Title                           | Company               | Location               | Link                                      |
|-----|---------------------------------|-----------------------|------------------------|-------------------------------------------|
| 1   | Example Job Title               | Example Company Name  | Example City, Country  | https://example.com/job-link              |



### SQLite Database (`db/jobs.db`)

The job data is also stored in a SQLite database. To interact with the database, you can use the SQLite command-line tool:

1. Open the database:
   ```bash
   sqlite3 db/jobs.db
   ```
2. View available tables:
   ```sql
   sqlite> .tables
   jobs
   ```
3. Query the table to view its contents:
   ```sql
   sqlite> SELECT * FROM jobs;
   ```
   Example output:
   ```
   1|Example Job Title|Example Company Name|Example City, Country|https://example.com/job-link
   ```



## Authors

 ([228cmc](https://github.com/228cmc))  


