import pdb

from selenium import webdriver
from selenium.webdriver.common.by import By

import config

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# Open the URL with window height 1440p
driver.set_window_size(1800, 2000)
driver.get(config.URL)
driver.implicitly_wait(5)


# Find and select date
date = driver.find_element(By.CSS_SELECTOR, f"[aria-label='{config.DATE}']")
date.click()

# Select table??

# Find all ook buttons and click the second one
book_buttons = driver.find_elements(By.XPATH, f"//button[.='{config.BOOK_BUTTON_TEXT}']")
book_buttons[1].click()
# # Click book(by span)
# book_button = driver.find_element(By.XPATH, f"//button[.='{config.BOOK_BUTTON_TEXT}']")
# book_button.click()

# Select time by span
# Time might take a while to load
# Wait with FluntWait
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, f"//span[.='{config.TIME_1}']"))

time = driver.find_element(By.XPATH, f"//span[.='{config.TIME_1}']")



# time = driver.find_element(By.XPATH, f"//span[.='{config.TIME_1}']")
time.click()

# Add guests
guests_inc = driver.find_element(By.CSS_SELECTOR, f"[aria-label='{config.PLUS_ICON}']")
for i in range(config.NUM_GUESTS): guests_inc.click()

# pdb.set_trace()
# Click continue
continue_button = driver.find_element(By.XPATH, f"//button[.='{config.CONTINUE_BUTTON_TEXT}']")
continue_button.click()

# Fill name, email (class contains name="name")
name_field = driver.find_element(By.CSS_SELECTOR, "input[type='text'].form-control[name='name']")
name_field.send_keys(config.NAME)

email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email'].form-control[name='email']")
email_field.send_keys(config.EMAIL)

mobile_field = driver.find_element(By.CSS_SELECTOR, "input[type='tel'].form-control[name='mobile']")
mobile_field.send_keys(config.MOBILE)

# Checkbox for terms and conditions
checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
checkbox.click()

# Prpceed to payment
continue_button = driver.find_element(By.XPATH, f"//button[.='{config.PROCEED_TO_PAYMENT}']")
continue_button.click()

pdb.set_trace()

# Close the browser
driver.quit()