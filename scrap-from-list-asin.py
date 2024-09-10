from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import requests
import random
import time

@dataclass
class Item:
    asin: str
    title: str
    price: str
    image_url: str

def get_html(page, asin):
    url = f"https://www.amazon.fr/dp/{asin}"
    page.goto(url)
    page.wait_for_timeout(3000)  # Attendre un peu pour s'assurer que tout est chargé
    html = page.content()  # Obtenir le HTML complet de la page
    return HTMLParser(html)

def download_image(image_url, filename):
    # Télécharger l'image
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image téléchargée et sauvegardée sous le nom : {filename}")
    else:
        print(f"Impossible de télécharger l'image, status code : {response.status_code}")

def parse_html(html, asin):
    # Extraire le titre du produit
    title_node = html.css_first('span#productTitle')  
    if title_node:
        product_title = title_node.text(strip=True)
    else:
        product_title = "Title not found"
    
    # Extraire le prix du produit
    price_symbol_node = html.css_first('span.a-price-symbol')  # Symbole du prix (€, $)
    price_whole_node = html.css_first('span.a-price-whole')    # Partie entière du prix
    price_fraction_node = html.css_first('span.a-price-fraction')  # Fraction du prix (cents)
    
    if price_symbol_node and price_whole_node and price_fraction_node:
        price = f"{price_symbol_node.text(strip=True)}{price_whole_node.text(strip=True)}.{price_fraction_node.text(strip=True)}"
    else:
        price = "Price not found"

    # Extraire l'URL de l'image
    image_node = html.css_first('div.imgTagWrapper img')  # Sélectionner l'image
    if image_node:
        image_url = image_node.attrs.get("src")
    else:
        image_url = "Image not found"
    
    # Créer l'objet Item
    item = Item(
        asin=asin,
        title=product_title,
        price=price,
        image_url=image_url
    )

    return item

def run(proxy, asin_list):
    with sync_playwright() as pw:
        # Extraire l'adresse IP, le port, l'utilisateur et le mot de passe du proxy
        proxy_parts = proxy.split(":")
        proxy_server = f"http://{proxy_parts[0]}:{proxy_parts[1]}"
        proxy_username = proxy_parts[2]
        proxy_password = proxy_parts[3]
        
        # Lancer le navigateur avec le proxy
        browser = pw.chromium.launch(headless=True, proxy={
            "server": proxy_server,
            "username": proxy_username,
            "password": proxy_password
        })

        page = browser.new_page()
        
        for asin in asin_list:
            # Extraire le HTML pour l'ASIN en cours
            html = get_html(page, asin)
            item = parse_html(html, asin)
            print(item)

            # Télécharger l'image si l'URL est trouvée
            if item.image_url != "Image not found":
                download_image(item.image_url, f"produit_image_{asin}.jpg")

            # Attendre un délai aléatoire entre 2 et 5 secondes
            wait_time = random.uniform(2, 5)
            print(f"Attente de {wait_time:.2f} secondes avant de continuer...")
            time.sleep(wait_time)
        
        browser.close()

def main():
    # Liste des ASINs à parcourir
    asin_list = ['B07PZR3PVB', 'B0BDJ6QBTL', 'B0CHWZ9TZS', 'B0CHYBZ8L8', 'B0BXSH4WGB', 'B0D52ZVRTZ', 
                 'B0BYD8F9W7', 'B0D1G3D31G', 'B09LCVHCVX', 'B0CBJSLDDB', 'B09HGGV5R5', 'B0D7MNX9Y5', 
                 'B0C6QP1LWY', 'B0BTYCRJSS', 'B08Q2CYLTQ', 'B0BHTJLFVP', 'B0CDLFK7JN', 'B0B5GP9FXN', 
                 'B0CKWZ3N1P', 'B0BHDS3HQS', 'B0BWN2718H', 'B0CDPKSL27', 'B0D452MJV5', 'B09CHJDZYL', 
                 'B0DB8619DZ', 'B0CQKD5N9X', 'B0BL668ZYM', 'B09HGW9V7D', 'B0CXPRHTNB', 'B0D2H4J4KZ', 
                 'B0979QRKMW', 'B08TJ2LGB8', 'B0BZV6SYXQ', 'B0BXM3ZFKC', 'B0BCZZXDS9', 'B07W7VNSC7', 
                 'B0C95J98LV', 'B0CB6DZX79', 'B0BTM6L3HQ', 'B0CB6DTXSH', 'B0CPFVB5VN', 'B0CD2F4B1G', 
                 'B09D7PXZV7', 'B09Q78MP7W', 'B086LKXYMD', 'B09QSZB5RY', 'B0CTHY1JNJ', 'B0C4TLFZSZ']

    # Exemple de proxy à utiliser
    proxy = "216.173.72.174:6793:ejyhouxi:tv90c5w28qxj"
    
    # Lancer avec un proxy
    run(proxy, asin_list)

if __name__ == "__main__":
    main()
