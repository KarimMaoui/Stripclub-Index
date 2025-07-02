import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

LOCATION = "Rosewood Theater New York"
OUTPUT_CSV = "rosewood_populartimes.csv"
FETCH_INTERVAL = 3600  # secondes (1 heure)

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(executable_path="./chromedriver", options=options)

def fetch_popular_times():
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Récupération de l'affluence pour : {LOCATION}")

   # URL directe vers le Rosewood Theater sur Google Maps
maps_url = "https://www.google.com/maps/place/Rosewood+Theater/@40.7542054,-73.9943727,17z"
driver.get(maps_url)
time.sleep(5)


    try:
        link = driver.find_element(By.XPATH, "//a[contains(@href,'/maps/place')]")
        link.click()
        time.sleep(5)
    except Exception as e:
        print("❌ Lien Google Maps non trouvé :", e)
        return None

    try:
        blocks = driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'Popular times') or contains(@aria-label, 'graph showing popular times')]")
        entries = []
        for block in blocks:
            text = block.get_attribute("aria-label")
            entries.append(text)
            print(text)
        return {"timestamp": timestamp, "data": entries}
    except Exception as e:
        print("❌ Aucun bloc d'affluence trouvé :", e)
        return None

def save_to_csv(record):
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for entry in record["data"]:
            writer.writerow([record["timestamp"], entry])

if __name__ == "__main__":
    # En-tête CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "popular_times_label"])

    record = fetch_popular_times()
    if record:
        save_to_csv(record)

    while True:
        time.sleep(FETCH_INTERVAL)
        record = fetch_popular_times()
        if record:
            save_to_csv(record)
