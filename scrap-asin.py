from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

def get_html(page, url):
    page.goto(url)
    page.wait_for_timeout(3000)  # Attendre que la page se charge
    html = page.content()  # Récupérer le contenu HTML
    return HTMLParser(html)

def extract_asins(html):
    asins = []
    
    # Récupérer toutes les balises contenant des liens vers les produits (balise <div> avec data-asin)
    product_nodes = html.css('div[data-asin]')
    
    for product in product_nodes:
        asin = product.attrs.get('data-asin')
        if asin:
            asins.append(asin)
    
    return asins

def run(proxy):
    search_url = "https://www.amazon.fr/s?k=airpods"  # URL de recherche sur Amazon pour AirPods
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
        html = get_html(page, search_url)
        
        # Extraire les ASINs des produits sur la page de résultats de recherche
        asins = extract_asins(html)
        print(f"ASINs extraits : {asins}")
        
        browser.close()

def main():
    # Exemple de proxy à utiliser
    proxy = "216.173.72.174:6793:ejyhouxi:tv90c5w28qxj"
    
    # Lancer avec un proxy
    run(proxy)

if __name__ == "__main__":
    main()
