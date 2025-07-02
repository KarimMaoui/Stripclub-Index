from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_popular_times(place_query):
    # Préparation navigateur headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    # Étape 1 : Recherche sur Google
    search_url = f"https://www.google.com/search?q={place_query}+site:google.com/maps"
    driver.get(search_url)
    time.sleep(5)

    try:
        # Étape 2 : Cliquer sur le lien Google Maps (souvent le premier)
        maps_link = driver.find_element(By.XPATH, "//a[contains(@href,'/maps/place')]")
        maps_url = maps_link.get_attribute("href")
        driver.get(maps_url)
        time.sleep(5)

        # Étape 3 : Extraire les blocs de popularité
        blocks = driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'graph showing popular times')]")
        if not blocks:
            print("Aucune donnée d’affluence trouvée.")
            return

        print(f"Données d'affluence pour : {place_query}")
        for block in blocks:
            print(block.get_attribute("aria-label"))

    except Exception as e:
        print("Erreur :", e)

    driver.quit()


# Exemple d’utilisation
get_popular_times("Rick's Cabaret New York")
