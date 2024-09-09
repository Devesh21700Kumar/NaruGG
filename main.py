# main.py

import pdb
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--kiosk")  # This will open Chrome in full screen on Mac
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)

def wait_and_click(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)
        logging.info(f"Clicked element: {value}")
        return True
    except Exception as e:
        logging.error(f"Could not click element {value}: {str(e)}")
        return False

def select_date(driver, target_date):
    # Click on the date navigation button to open the calendar
    wait_and_click(driver, By.XPATH, "//button[contains(@class, 'react-calendar__navigation__label')]")
    
    # Navigate to the correct year and month
    while True:
        current_date_text = driver.find_element(By.XPATH, "//button[contains(@class, 'react-calendar__navigation__label')]").text
        current_date = datetime.strptime(current_date_text, "%b %Y")
        if current_date.year == target_date.year and current_date.month == target_date.month:
            break
        wait_and_click(driver, By.XPATH, "//button[contains(@class, 'react-calendar__navigation__next-button')]")

    # Select the specific day
    day_xpath = f"//button[contains(@class, 'react-calendar__tile') and .//abbr[text()='{target_date.day}']]"
    wait_and_click(driver, By.XPATH, day_xpath)
    logging.info(f"Selected date: {target_date.strftime('%B %d, %Y')}")

def main():
    driver = setup_driver()
    try:
        # Open the URL
        driver.get(config.URL)
        driver.implicitly_wait(5)
        logging.info(f"Opened URL: {config.URL}")

        # Select the date
        target_date = datetime.strptime(config.DATE, "%B %d, %Y")
        select_date(driver, target_date)

        # Find all book buttons and click the second one
        book_buttons = driver.find_elements(By.XPATH, f"//button[.='{config.BOOK_BUTTON_TEXT}']")
        # Scroll the first BOOK button into view and click it
        driver.execute_script("arguments[0].scrollIntoView(true);", book_buttons[0])
        time.sleep(1)  # Give the page a moment to settle after scrolling
        wait_and_click(driver, By.XPATH, f"(//button[.='{config.BOOK_BUTTON_TEXT}'])[1]")
        logging.info("Clicked BOOK button")
        logging.info("Clicked BOOK button")

        # Select time
        wait_and_click(driver, By.XPATH, f"//span[.='{config.TIME_1}']")
        logging.info(f"Selected time: {config.TIME_1}")

        # Add guests
        guests_inc = driver.find_element(By.CSS_SELECTOR, f"[aria-label='{config.PLUS_ICON}']")
        for _ in range(config.NUM_GUESTS):
            guests_inc.click()
            time.sleep(0.5)  # Short delay between clicks
        logging.info(f"Added {config.NUM_GUESTS} guests")

        # Click continue
        wait_and_click(driver, By.XPATH, f"//button[.='{config.CONTINUE_BUTTON_TEXT}']")
        logging.info("Clicked continue button")

        # Fill name, email, mobile
        name_field = driver.find_element(By.CSS_SELECTOR, "input[type='text'].form-control[name='name']")
        name_field.send_keys(config.NAME)
        email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email'].form-control[name='email']")
        email_field.send_keys(config.EMAIL)
        mobile_field = driver.find_element(By.CSS_SELECTOR, "input[type='tel'].form-control[name='mobile']")
        mobile_field.send_keys(config.MOBILE)
        logging.info("Filled in personal details")

        # Checkbox for terms and conditions
        checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        checkbox.click()
        logging.info("Accepted terms and conditions")

        # Proceed to payment
        wait_and_click(driver, By.XPATH, f"//button[.='{config.PROCEED_TO_PAYMENT}']")
        logging.info("Clicked proceed to payment button")

        logging.info("Booking process completed successfully")
        pdb.set_trace()

    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()