from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import requests

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
    print(html)  # Imprimer le HTML pour débogage
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

def run(proxy):
    asin = "B084P1H86P"  # Exemple d'ASIN pour les Apple AirPods Pro - 2e génération
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
        html = get_html(page, asin)
        item = parse_html(html, asin)
        print(item)

        # Télécharger l'image si l'URL est trouvée
        if item.image_url != "Image not found":
            download_image(item.image_url, "produit_image.jpg")
        
        browser.close()

def main():
    # Exemple de proxy à utiliser
    proxy = "216.173.72.174:6793:ejyhouxi:tv90c5w28qxj"
    
    # Lancer avec un proxy
    run(proxy)

if __name__ == "__main__":
    main()
