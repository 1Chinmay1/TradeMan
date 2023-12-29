from dhanhq import dhanhq
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

def login_to_dhan(client_id, mobile_number, password):
    user_number = mobile_number
    user_pwd = password
    user_id = client_id

    global dhan_access_token
    #chromedriver_autoinstaller.install(path="C:\\Program Files\\Google\\Chrome\\Application")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    print(driver)
    try:
        # Open Dhan login page
        driver.get("https://login.dhan.co/")

        # Wait for the elements to load
        mobile_input = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(By.NAME, 'phone_number')
        )
        password_input = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(By.NAME, 'password')
        )
        submit_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(By.XPATH, '//button[contains(text(), "Login")]')
        )

        # Input mobile number and password
        mobile_input.send_keys(user_number)
        password_input.send_keys(user_pwd)

        # Click login button
        submit_button.click()

        sleep(10)  # Wait for login process to complete (adjust the time as needed)

        # After successful login, extract the access token or perform any other necessary steps
        # Here, you may need to extract the access token from the session, if available

        # Example: Extracting the access token from cookies (this may vary based on how Dhan handles sessions)
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'access_token':
                dhan_access_token = cookie['value']
                print(f"Dhan Access Token: {dhan_access_token}")
                break

    finally:
        driver.quit()  # Close the browser window after completion

    return dhan_access_token

# Usage
client_id = os.getenv("client_id")
mobile_number = os.getenv("mobile_number")
password = os.getenv("password")
access_token = os.getenv("access_token")
#dhan_access_token = login_to_dhan(client_id,mobile_number, password)
