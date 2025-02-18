import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# https://www.amazon.com/TUDIA-Nothing-Phone-Anti-Yellowing-Semi-Transparent/product-reviews/B0CZ3SGFRQ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews

# Select a Random User-Agent

email_id = 'truemark.woc7@gmail.com'
password = 'k4&XJJmpeq6Fw.3'
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
]

homePage = "https://www.amazon.com/ref=nav_logo"
driver = None 

def setup_driver():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={USER_AGENTS}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--headless")  # Remove this if you want to see the browser

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except WebDriverException as e:
        print(f"WebDriver Error: {e}")
        return -1


def loginAmazon(): 
    global driver
    driver = setup_driver()
    if not driver : 
        return -1 

    # Initialize WebDriver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try : 
        # Open Amazon Login Page
        driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=900&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fpath%3D%252Fgp%252Fyourstore%252Fhome%26signIn%3D1%26useRedirectOnSuccess%3D1%26action%3Dsign-out%26ref_%3Dnav_AccountFlyout_signout&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
        time.sleep(1) 

        # Enter Email
        email_field = driver.find_element(By.ID, "ap_email")
        email_field.send_keys(email_id)
        email_field.send_keys(Keys.RETURN)

        time.sleep(random.uniform(2, 4))  # Wait before next step

        # Enter Password
        password_field = driver.find_element(By.ID, "ap_password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(2)  # Wait for login to process

        # Check if login was successful
        if "https://www.amazon.com/ap/signin" in driver.current_url:
            print("Login failed")
            # return -1 
        else:
            print("Login successful!")
            # return 0 
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Login Error: {e}")
        driver.quit()
        return -1


def getAmazonReviews(product_review_url) : 
    if not driver:
        print("Driver not initialized. Please log in first.")
        return -1
    try:
        driver.get(product_review_url)
        time.sleep(2)

        # Check if "See all reviews" link exists
        try:
            product_review_link = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//a[@data-hook='see-all-reviews-link-foot']")
            )).get_attribute("href")
            driver.get(product_review_link)
            time.sleep(2)
        except TimeoutException:
            print("Could not find 'See all reviews' link. Exiting...")
            return -1

        reviews = []

        while True:
            # Handle translation links if available
            try:
                translate_links = driver.find_elements(By.XPATH, "//a[@data-hook='cr-translate-these-reviews-link']")
                if translate_links:
                    translate_links[0].click()
                    time.sleep(2)
            except Exception:
                pass  # Ignore if no translation link is found

            # Extract Review Titles & Texts
            review_texts = driver.find_elements(By.CLASS_NAME, "review-text-content")
            for text in review_texts:
                reviews.append(text.text.strip())

            # Check if "Next" button is disabled
            try:
                next_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "a-last")
                ))
                if "a-disabled" in next_button.get_attribute("class"):  # If disabled, stop
                    print("No more pages. Scraping complete.")
                    break
                else:
                    next_button.click()
                    time.sleep(2)  # Wait for the next page to load
            except TimeoutException:
                print("Next button not found. Ending scraping process.")
                break

        driver.get(homePage)
        return reviews

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Scraping Error: {e}")
        return -1

    except WebDriverException as e:
        print(f"WebDriver Error: {e}")
        return -1




# print(reviews)

# driver.quit()
