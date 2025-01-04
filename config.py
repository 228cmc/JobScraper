from dotenv import load_dotenv
import os

load_dotenv()

JOB_URL = "https://myfuture.bath.ac.uk/students/jobs"
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")