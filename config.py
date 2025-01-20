from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
JOB_URL = os.getenv("JOB_URL")
KEYWORDS = os.getenv("KEYWORDS")  
CONTRACT_HOURS = os.getenv("CONTRACT_HOURS")
LOCATION = os.getenv("LOCATION")
