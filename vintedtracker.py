# -*- coding: utf-8 -*-

"""
Vinted Notifiche Bot
"""

import requests
import time
from prefect import flow, task
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# print(dir(prefect))
# Configurazione Telegram
TELEGRAM_TOKEN = '7247285493:AAFDjrLcO3gzMxOW54ZLp38sigavM45hPoo'  # Sostituisci con il token del bot
CHAT_ID = '23791879'  # Sostituisci con il tuo Chat ID

# Funzione per inviare un messaggio su Telegram
@task
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Messaggio inviato con successo!")
    else:
        print(f"Errore nell'invio: {response.status_code}, {response.text}")


# Funzione di ricerca con Selenium
@task
def search_vinted(search_query, max_price):
    # Configura le opzioni di Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Avvia il browser a schermo intero
    # Usa il servizio per specificare il percorso del ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.vinted.it/catalog")

    # 1. Attendere e fare clic sul pulsante "Accetta tutti" i cookie
    try:
        consent_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Accetta tutti")]'))
        )
        consent_button.click()
        print("Consenso ai cookie accettato.")
    except Exception as e:
        print("Errore nel cliccare sul pulsante per accettare i cookie:", e)
    
    # 2. Trova il campo di ricerca e inserisci il testo
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_text"))
        )
        
        search_box.clear()
        search_box.send_keys(search_query)
        print(f"Ricerca per '{search_query}' inserita.")
        # 3. Simula il tasto "Invio" per avviare la ricerca
        search_box.send_keys(Keys.RETURN)
        print("Ricerca avviata con Invio.")
    except Exception as e:
        print("Errore nel trovare il campo di ricerca:", e)

    # 4. Debug: Verifica se il filtro del prezzo è presente sulla pagina
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#content > div > div > section > div:nth-child(6) > div:nth-child(6) > div > div > button > div.web_ui__Chip__text > span"))
        )
        price_filter = driver.find_element(By.CSS_SELECTOR, "#content > div > div > section > div:nth-child(6) > div:nth-child(6) > div > div > button > div.web_ui__Chip__text > span")
        time.sleep(1)
        price_filter.click()
        
        price_to =  WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "price_to"))
        )
        
        
        price_to.clear()
        price_to.send_keys(str(max_price))
        print(f"Filtro del prezzo impostato a massimo {max_price} euro.")
        # Applica il filtro
        time.sleep(1)
        price_to.send_keys(Keys.ENTER)
        print(f"Filtro prezzo applicato.")
    except Exception as e:
        print("Errore nel trovare il filtro del prezzo:", e)

    # 5. Attendere che i risultati vengano caricati
    time.sleep(5)

    # 6. Estrai i risultati
    try:
        items = driver.find_element(By.CSS_SELECTOR, "#content > div > div > section > div.u-ui-padding-vertical-medium.u-flexbox.u-justify-content-between.u-align-items-center > span")
        print(f"Numero di articoli trovati: {items.text}")
        # results = []
        # for item in items:
        #     title = item.find_element(By.CSS_SELECTOR, ".catalog-item-title").text
        #     price = item.find_element(By.CSS_SELECTOR, ".catalog-item-price").text
        #     link = item.find_element(By.CSS_SELECTOR, "a.catalog-item-link").get_attribute("href")
        #     results.append({"title": title, "price": price, "link": link})
        # driver.quit()
        # return results
    except Exception as e:
        print("Errore nell'estrarre i risultati:", e)
        driver.quit()
        return []

@flow
def main():
    
    send_telegram_message("Ciao! Questo è un messaggio di prova dal tuo bot Telegram.")
    search_query = "Mario Kart 8 Nintendo Switch"
    max_price = 25
    items = search_vinted(search_query, max_price)

    # Mostra i risultati trovati
    if items:
        for item in items:
            print(f"- {item['title']} | {item['price']} | {item['link']}")
    else:
        print("Nessun articolo trovato.")
            
if __name__ == "__main__":
    main()
