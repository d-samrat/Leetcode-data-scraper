import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def leetcode_scraper(username, driver):
    url = f"https://leetcode.com/u/{username}/"
    print(f"Scraping data for Username: {username}")

    driver.get(url)
    driver.implicitly_wait(10)

    # Initialize data dictionary
    data = {"Username": username, "Rank": "N/A", "Problems Solved": "N/A", "Badges": "N/A"}

    try:
        # Rank
        try:
            rank_element = driver.find_element(By.CSS_SELECTOR, ".ttext-label-1.dark\\:text-dark-label-1.font-medium")
            data["Rank"] = rank_element.text
        except Exception as e:
            print("Error fetching rank: ", e)

        # Problems Solved
        try:
            prob_sol_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='text-[30px] font-semibold leading-[32px]']"))
            )
            data["Problems Solved"] = prob_sol_element.text
        except Exception as e:
            print("Error fetching problems solved: ", e)

        # Badges
        try:
            badges_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH,
                    "//div[contains(@class, 'bg-layer-1') and contains(@class, 'dark:bg-dark-layer-1')]"
                    "//div[contains(@class, 'text-label-1') and contains(@class, 'dark:text-dark-label-1') and contains(@class, 'mt-1.5') and contains(@class, 'text-2xl')]"
                ))
            )
            data["Badges"] = badges_element.text
        except Exception as e:
            print("Error fetching badges: ", e)

    except Exception as e:
        print("General error: ", e)

    return data

def main():
    # Read usernames from JSON file
    with open("usernames.json", "r") as json_file:
        data = json.load(json_file)
        usernames = data.get("usernames", [])

    # Prepare CSV file
    csv_file = "leetcode_data.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Username", "Rank", "Problems Solved", "Badges"])
        writer.writeheader()

        # Start WebDriver
        driver = webdriver.Chrome()

        # Scrape data for each username
        for username in usernames:
            user_data = leetcode_scraper(username, driver)
            writer.writerow(user_data)

        # Close WebDriver
        driver.quit()

    print(f"Data saved to {csv_file}")

if __name__ == "__main__":
    main()
