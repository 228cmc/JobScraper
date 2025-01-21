from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import KEYWORDS, CONTRACT_HOURS, LOCATION

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
    options.add_argument("--no-sandbox")  # sandbox security thing from chrome it could cause conflict with docker
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver

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
    wait = WebDriverWait(driver, 10)  # Wait instance for dynamic elements

    driver.get(url)  # Open the URL
    time.sleep(10)  # Wait for the page to load

    # Log in
    # Use find_element of selenium to interact with buttons
    current_student_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Current Student or Staff')]")
    current_student_button.click()
    time.sleep(10)
    try:
        username_field = driver.find_element(By.ID, "username")
        print("Página de inicio de sesión cargada correctamente.")
    except Exception as e:
        print("Error: No se pudo cargar la página de inicio de sesión.")
        print(e)

    driver.find_element(By.ID, "username").send_keys(username)  # Pass my username
    driver.find_element(By.ID, "password").send_keys(password)  # And password
    driver.find_element(By.XPATH, "//input[@value='LOGIN']").click()
    time.sleep(5)  # Allow time for the login to process and redirect to the dashboard

    # According to the HTML structure reviewed with the inspect tool...
    # In this case for MyFuture I have to pass the keyword, contract hours and location

    keyword_input = driver.find_element(By.ID, "keywords")
    # Enter the keywords from the config file
    keyword_input.send_keys(KEYWORDS)

    # Handle "Contract hours" dropdown
    dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Contract hours']/following-sibling::div//button")))
    dropdown_button.click()  # Click to open dropdown

    # Select the contract hours option from the config file
    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//ul[@role='menu']//a[@role='menuitem' and text()='{CONTRACT_HOURS}']")
    ))   
    option.click()

    # Enter the location if specified in the config file
    """
    if LOCATION:
        location_input = driver.find_element(By.ID, "locations")
        location_input.send_keys(LOCATION) """

    # Click the search button (location filter appears to be set via dropdowns/buttons)
    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
    search_button.click()

    time.sleep(5)

    # Extract the results
    jobs = []  # List to store all job postings
    job_elements = driver.find_elements(By.CLASS_NAME, "job-search-results-list-item")  # Update with the correct class name

    for job_element in job_elements:
        try:
            title = job_element.find_element(By.XPATH, ".//h4").text  # Extract job title
            link = job_element.find_element(By.XPATH, ".//h4/ancestor::a").get_attribute("href")  # Extract job link
            company = job_element.find_element(By.XPATH, ".//a[contains(@href, '/myfuture/organisations/detail')]").text  # Extract company name
            location = job_element.find_element(By.XPATH, ".//div[contains(@class, 'BTZdAcRyXRGVGrcXspx9')]").text  # Extract location
            jobs.append({"title": title, "company": company, "location": location, "link": link})
        except Exception as e:
            print(f"Error extracting job details: {e}")

    driver.quit()  # Close the browser
    return jobs
