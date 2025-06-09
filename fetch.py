import csv
import re
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

def extract_coords_from_search(url):
    match = re.search(r'/maps/search/([0-9.-]+),([0-9.-]+)', url)
    if match:
        lat, lng = match.groups()
        print(f"Extracted from /maps/search/: {lat}, {lng}")
        return lat, lng
    return "", ""

def extract_coords_from_place(url, driver):
    print(f"Looking up coordinates for: {url}")
    try:
        driver.get(url)
        time.sleep(5)  # wait for JS to load; adjust if needed

        page_source = driver.page_source

        match = re.search(r'@([0-9.-]+),([0-9.-]+),', page_source)
        if match:
            lat, lng = match.group(1), match.group(2)
            print(f"Extracted from /maps/place/: {lat}, {lng}")
            return lat, lng

        print("Coordinates not found on page.")
        return "", ""

    except WebDriverException as e:
        print(f"WebDriver error: {e}")
        return "", ""

def process_csv(input_file):
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_with_coords.csv"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    cache = {}

    with open(input_file, newline='', encoding='utf-8') as csv_in, \
         open(output_file, 'w', newline='', encoding='utf-8') as csv_out:

        reader = csv.DictReader(csv_in)
        fieldnames = reader.fieldnames + ["Latitude", "Longitude"]
        writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            url = row.get("URL", "")
            lat, lng = "", ""

            if url in cache:
                lat, lng = cache[url]
            elif "/maps/search/" in url:
                lat, lng = extract_coords_from_search(url)
            elif "/maps/place/" in url:
                lat, lng = extract_coords_from_place(url, driver)

            cache[url] = (lat, lng)
            row["Latitude"] = lat
            row["Longitude"] = lng
            writer.writerow(row)

    driver.quit()
    print(f"\n✅ Finished. Output saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch.py <input_csv_file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    process_csv(input_filename)
