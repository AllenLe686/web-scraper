from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Driver options for Chrome
driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incognito")

def create_webdriver():
    return webdriver.Chrome(options=driver_option)

# Main script for scraping GitHub machine learning projects
browser = create_webdriver()
browser.get("https://github.com/collections/machine-learning")

# Extract all projects
projects = browser.find_elements(By.XPATH, "//h1[contains(@class, 'lh-condensed')]")
print(f"Found {len(projects)} projects")

# Extract name and URL for each project
project_list = {}
for proj in projects:
    proj_name = proj.text
    links = proj.find_elements(By.XPATH, ".//a")
    if not links:
        print(f"Skipping heading with no link: {proj_name!r}")
        continue
    proj_url = links[0].get_attribute("href")
    project_list[proj_name] = proj_url

print(f"Collected {len(project_list)} projects")
print(project_list)

browser.quit()