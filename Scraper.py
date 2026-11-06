from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incognito")

def create_webdriver():
    return webdriver.Chrome(options=driver_option)


if __name__ == "__main__":
    driver = create_webdriver()
    driver.get("https://www.example.com")
    print(driver.title)
    driver.quit()