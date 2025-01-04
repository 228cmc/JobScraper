import os
from config import JOB_URL, USERNAME, PASSWORD
from scraper import scrape_jobs


def main():
    """
    main function to run the job scraper
    """

    if not all([JOB_URL, USERNAME, PASSWORD]):
        print(" missing sm in the config")
        return
    print("starting to scrap")


    try:

        scrape_jobs(JOB_URL,USERNAME, PASSWORD)
    except Exception as e:
        print(f"An error occured : {e }")


        