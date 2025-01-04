from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys


def get_driver():

    """
    Sets up and returns a Chrome WebDriver for automated browser tasks.

    Configures Chrome to run in headless mode (without a visible window) and
    uses `webdriver_manager` to automatically handle the correct ChromeDriver version.

    Returns:
        selenium.webdriver.Chrome: A ready-to-use WebDriver.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")#sandbox security thing from chrome it could cause conflict with docker 
    return webdriver.Chrome(service= Service(ChromeDriverManager()))


def scrape_jobs(url, username, password):
    """
    Logs into MyFuture and scrapes job postings.

    Args:
        url (str): URL of the job portal.
        username (str): MyFuture username.
        password (str): MyFuture password.

    Returns:
        list: A list of job postings as dictionaries.
    """
    # Initialize the WebDriver
    driver = get_driver()  # Set up the Chrome WebDriver with the configured options

    try:
        driver.get(url)  # Open the  URL 
        time.sleep(3)  # Wait for the page to load 

        # Log in 
        driver.find_element(By.ID, "username").send_keys(username)  #pass my username
        driver.find_element(By.ID, "password").send_keys(password)  # andd password
        driver.find_element(By.ID, "submitButton").click()  # click the login button to submit the form
        time.sleep(5)  # Allow time for the login to process and redirect to the dashboard


        #according to the html structure reviewed with inspect tool..
        #in this case for my future I have to passs the keyword, contract hours and  location

        keyword_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder= 'eg. Graduate, Intern, Diversity, Disability]")
        keyword_input.send_keys("Intern")


        contract_hours_dropdown = driver.find_element(By.XPATH, "//select[@id='contractHours']" )
        contract_hours_dropdown.send_keys(Keys.DOWN)
        contract_hours_dropdown.send_keys(Keys.RETURN)


        location_input = driver.find_element(By.XPATH,"//button[contains(text(), 'Search')]" )
        location_input.send_keys("London")


        time.sleep(5)

        #extract the results
        jobs = driver.find_elements(By.CLASS_NAME, "")

        for job in jobs:
            
            title = job.find_element(By.CLASS_NAME, "")
            location =job.find_element(By.CLASS_NAME,"" )


    finally:

        driver.quit() #close browser


