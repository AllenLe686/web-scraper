import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incognito")

def create_webdriver():
    return webdriver.Chrome(options=driver_option)

def get_project_list():
    """Step 2: collect project names and URLs from the collection page."""
    browser = create_webdriver()
    try:
        browser.get("https://github.com/collections/machine-learning")
        projects = browser.find_elements(By.XPATH, "//h1[contains(@class, 'lh-condensed')]")
        project_list = {}
        for proj in projects:
            links = proj.find_elements(By.XPATH, ".//a")
            if not links:
                continue
            project_list[proj.text] = links[0].get_attribute("href")
        return project_list
    finally:
        browser.quit()

def scrape_url(url):
    """Visit one project page and return data from it."""
    browser = create_webdriver()
    try:
        browser.get(url)
        return {"project_url": url, "page_title": browser.title}
    finally:
        browser.quit()

if __name__ == "__main__":
    start = time.time()

    project_list = get_project_list()
    urlarray = list(project_list.values())
    print(f"Scraping {len(urlarray)} project pages...")

    results = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(scrape_url, url) for url in urlarray]
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"A page failed: {e}")

    project_df = pd.DataFrame(results)
    project_df.to_csv("project_details.csv", index=False)
    print(project_df.head())
    print(f"Done in {time.time() - start:.1f} seconds")