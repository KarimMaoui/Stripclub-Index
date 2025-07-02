import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

LOCATION = "Rick's Cabaret New York"
OUTPUT_CSV = "rosewood_populartimes.csv"
FETCH_INTERVAL = 3600  # secondes (1 heure)

# Initialisation du driver
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
service = Service("./chromedriver")
driver = webdriver.Chrome(service=service, options=options)

def fetch_popular_times():
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Récupération de l'affluence pour : {LOCATION}")

    # Aller directement sur la page Maps du Rosewood Theater
    maps_url = "https://www.google.com/maps/place/Rick's+Cabaret+New+York/@40.751251,-73.9904733,17z"
    driver.get(maps_url)
    time.sleep(5)

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
    # En-tête CSV (création initiale)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "popular_times_label"])

    record = fetch_popular_times()
    if record:
        save_to_csv(record)

    # Boucle continue toutes les heures
    while True:
        time.sleep(FETCH_INTERVAL)
        record = fetch_popular_times()
        if record:
            save_to_csv(record)

