import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import time
from tqdm import tqdm

def download_image(url, folder, name=None):
    os.makedirs(folder, exist_ok=True)
    if not name:
        name = os.path.basename(urlparse(url).path)
    path = os.path.join(folder, name)
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(path, "wb") as f:
            f.write(resp.content)
        # Suppression du message de téléchargement image
    else:
        print(f"✘ Erreur téléchargement image {url}")
    return path

def get_product_id_from_url(url):
    return url.split("/")[-1]

def parse_price(price_text):
    mapping_currency = {'£': 'GBP', '$': 'USD', '€': 'EUR'}
    price_text = price_text.replace('\xa0', ' ').strip()
    value_match = re.search(r'[\d.,]+', price_text)
    if not value_match:
        return None, "UNKNOWN"
    raw_value = value_match.group().replace(',', '.')
    try:
        value = float(raw_value)
    except ValueError:
        return None, "UNKNOWN"
    symbol_match = re.search(r'[£€$]', price_text)
    symbol = symbol_match.group() if symbol_match else ''
    currency = mapping_currency.get(symbol, symbol or "UNKNOWN")
    return value, currency

def format_name(name):
    name = name.upper()
    if name.startswith("NIKE "):
        name = name[5:]
    if name.endswith(" MEN'S SHOES"):
        name = name[:-12]
    name = name.replace(" ", "+")
    return name

def get_image_urls(r, product_name):
    urls = []
    soup = BeautifulSoup(r.text, "html.parser")
    container = soup.find("div", attrs={"data-testid": "ThumbnailListContainer"})
    if not container:
        print("⚠️ Conteneur 'ThumbnailListContainer' non trouvé.")
        return urls
    inputs = container.find_all("input", {"type": "radio"})
    formatted_name = format_name(product_name)
    for input_tag in inputs:
        image_id = input_tag.get("id")
        if image_id:
            url = f"https://static.nike.com/a/images/t_default/{image_id}/{formatted_name}.png"
            urls.append(url)
    return urls

def scrape_nike_product(url, brand="nike", country="uk", section="womens", category="clothes"):
    print(f"\n🔍 Traitement du produit : {url}")
    product_id = get_product_id_from_url(url)
    print(f"🆔 Product ID détecté : {product_id}")

    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"❌ Erreur chargement page {url} (status {resp.status_code})")
        return

    soup = BeautifulSoup(resp.text, "html.parser")

    h1 = soup.find("h1", id="pdp_product_title")
    title = h1.text.strip() if h1 else "Titre non trouvé"
    print(f"📛 Titre : {title}")

    price_span = soup.find("span", {"data-testid": "currentPrice-container"})
    price_text = price_span.text.strip() if price_span else ""
    price_value, currency_code = parse_price(price_text)
    print(f"💰 Prix : {price_value} {currency_code}")

    images_urls = get_image_urls(resp, title)
    if not images_urls:
        print("⚠️ Aucune image trouvée.")

    images_info = []
    image_folder = f"nike_products/images/{product_id}"
    os.makedirs(image_folder, exist_ok=True)

    # Téléchargement des images sans message ni barre de progression
    for i, img_url in enumerate(images_urls):
        ext = os.path.splitext(urlparse(img_url).path)[1]
        img_type = "main" if i == 0 else f"hover{i}"
        img_name = f"{img_type}{ext}"
        local_path = download_image(img_url, image_folder, img_name)
        images_info.append({
            "type": img_type,
            "url": img_url,
            "local_path": local_path.replace("\\", "/")
        })

    product_json = {
        "id": product_id,
        "name": title,
        "brand": brand,
        "color": "",
        "category": category,
        "section": section,
        "country": country,
        "price": {
            "value_original": price_value,
            "current_price": price_value,
            "is_Discount": False,
            "currency": currency_code
        },
        "url": url,
        "product_code": product_id,
        "images": images_info
    }

    json_folder = f"nike_products/{country}/{section}/{category}"
    os.makedirs(json_folder, exist_ok=True)
    json_path = os.path.join(json_folder, f"{product_id}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(product_json, f, indent=4, ensure_ascii=False)

    print(f"💾 JSON sauvegardé : {json_path}")
    return product_json

def process_all_links(base_dir="nike_links"):
    countries = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    print(f"📂 Pays détectés : {', '.join(countries)}")
    for country in countries:
        country_path = os.path.join(base_dir, country)
        sections = [d for d in os.listdir(country_path) if os.path.isdir(os.path.join(country_path, d))]
        print(f"\n🌍 Traitement pays : {country} ({len(sections)} sections)")
        for section in sections:
            section_path = os.path.join(country_path, section)
            files = [f for f in os.listdir(section_path) if f.endswith(".txt")]
            print(f"➡️ Section : {section} ({len(files)} fichiers)")

            for filename in files:
                category = filename.replace(".txt", "")
                filepath = os.path.join(section_path, filename)
                print(f"\n📄 Traitement fichier : {filepath}")
                with open(filepath, "r") as f:
                    urls = [line.strip() for line in f if line.strip()]

                # Barre de progression pour les URLs seulement
                for url in tqdm(urls, desc=f"Scraping URLs ({category})", unit="produit"):
                    try:
                        scrape_nike_product(
                            url,
                            brand="nike",
                            country=country,
                            section=section,
                            category=category
                        )
                        time.sleep(1)  # éviter trop de requêtes simultanées
                    except Exception as e:
                        print(f"❗ Erreur avec l'URL {url} : {e}")

if __name__ == "__main__":
    print("🚀 Lancement du scraping Nike...")
    process_all_links()
    print("\n✅ Scraping terminé.")
