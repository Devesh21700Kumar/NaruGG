# main.py

import pdb
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)

def wait_and_find_element(driver, by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException:
        logging.error(f"Timeout waiting for element: {by}={value}")
        return None

def wait_and_click(driver, element, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '.')))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        logging.error(f"Error clicking element: {str(e)}")

def main():
    driver = setup_driver()
    try:
        # Open the URL
        driver.get(config.URL)
        driver.implicitly_wait(5)
        logging.info(f"Opened URL: {config.URL}")

        # Find and select date
        date = wait_and_find_element(driver, By.CSS_SELECTOR, f"[aria-label='{config.DATE}']")
        if date:
            wait_and_click(driver, date)
        else:
            logging.error("Date element not found. Exiting.")
            return

        # Find all book buttons and click the second one
        book_buttons = driver.find_elements(By.XPATH, f"//button[.='{config.BOOK_BUTTON_TEXT}']")
        if len(book_buttons) >= 1:
            wait_and_click(driver, book_buttons[0])
        else:
            logging.error("Not enough book buttons found. Exiting.")
            return

        # Select time
        time_element = wait_and_find_element(driver, By.XPATH, f"//span[.='{config.TIME_1}']")
        if time_element:
            wait_and_click(driver, time_element)
        else:
            logging.error(f"Time slot {config.TIME_1} not found. Exiting.")
            return

        # Add guests
        guests_inc = wait_and_find_element(driver, By.CSS_SELECTOR, f"[aria-label='{config.PLUS_ICON}']")
        if guests_inc:
            for _ in range(config.NUM_GUESTS):
                wait_and_click(driver, guests_inc)
        else:
            logging.error("Guest increment button not found. Exiting.")
            return

        # Click continue
        continue_button = wait_and_find_element(driver, By.XPATH, f"//button[.='{config.CONTINUE_BUTTON_TEXT}']")
        if continue_button:
            wait_and_click(driver, continue_button)
        else:
            logging.error("Continue button not found. Exiting.")
            return

        # Fill name, email, mobile
        name_field = wait_and_find_element(driver, By.CSS_SELECTOR, "input[type='text'].form-control[name='name']")
        email_field = wait_and_find_element(driver, By.CSS_SELECTOR, "input[type='email'].form-control[name='email']")
        mobile_field = wait_and_find_element(driver, By.CSS_SELECTOR, "input[type='tel'].form-control[name='mobile']")
        
        if all([name_field, email_field, mobile_field]):
            name_field.send_keys(config.NAME)
            email_field.send_keys(config.EMAIL)
            mobile_field.send_keys(config.MOBILE)
        else:
            logging.error("One or more input fields not found. Exiting.")
            return

        # Checkbox for terms and conditions
        checkbox = wait_and_find_element(driver, By.CSS_SELECTOR, "input[type='checkbox']")
        if checkbox:
            wait_and_click(driver, checkbox)
        else:
            logging.error("Terms and conditions checkbox not found. Exiting.")
            return

        # Proceed to payment
        proceed_button = wait_and_find_element(driver, By.XPATH, f"//button[.='{config.PROCEED_TO_PAYMENT}']")
        if proceed_button:
            wait_and_click(driver, proceed_button)
        else:
            logging.error("Proceed to payment button not found. Exiting.")
            return

        logging.info("Booking process completed successfully.")
        pdb.set_trace()

    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()