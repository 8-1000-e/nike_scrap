import os
import requests
import time

HEADERS = {
 "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.nike.com/",
    "anonymousId": "A433038E909913B03488E8507C9D9D6B",
    "nike-api-caller-id": "nike:dotcom:browse:wall.client:2.0",
    "Origin": "https://www.nike.com",
    "Connection": "keep-alive",
    "Cookie": (
        "ni_d=176EF3A2-E1D7-4EBC-a90B-BAF061608E7C; "
        "anonymousId=A433038E909913B03488E8507C9D9D6B; "
        "ni_c=1PA=0|BEAD=0|PERF=0|PERS=0; "
        "mbox=PC#04f4ab10d33aa326bf44c8a68f1942b9.37_0#1810551015|session#9899771847d34d2bb1b83705bfccebc9#1747324938; "
        "NIKE_COMMERCE_COUNTRY=US; "
        "NIKE_COMMERCE_LANG_LOCALE=en_US; "
        "CONSUMERCHOICE=us/en_us; "
        "CONSUMERCHOICE_SESSION=t; "
        "AnalysisUserId=6d2c6b95-d23d-4e6e-9df4-522bcbda51ec; "
        "forterToken=4d4e19719f5a4405b97b3204c357643f_1747311288532_7086_UAL9_11ck; "
        "KP_UIDz-ssn=02dP3ChCADuxFypLVe2NcrIlG1FcZhSDiGnYR4OKnEQPmHbYKFGu8D8neDtxsUERQnal8hUlVbzzWCEZ8AOdnWctaE4W4hatMfcCwkFJzfDvwwvJ941GDFztFDqT8umfktU6FZM4Ym5rkonndJIfOCdTZP8xFM1vbPzVCr; "
        "KP_UIDz=02dP3ChCADuxFypLVe2NcrIlG1FcZhSDiGnYR4OKnEQPmHbYKFGu8D8neDtxsUERQnal8hUlVbzzWCEZ8AOdnWctaE4W4hatMfcCwkFJzfDvwwvJ941GDFztFDqT8umfktU6FZM4Ym5rkonndJIfOCdTZP8xFM1vbPzVCr; "
        "sq=0; "
        "ak_bmsc=3B3CDF94504DDAEBEB7CA55433E7D592~000000000000000000000000000000~YAAQzeJIF8cjeM2WAQAAjYUX6RtrnngK2/JaryjPS6wRo4G9Ai1MpJz35nnohhrp5qQjpJTc7no0IQpgvt5LUIOsNdtzTH47g3K270IMOExdwQM5qMn9LihlB+4Z51AsjlxNrJwH5vhawTM0YYOPTmZBEYAdYLDd5L04hEj57PUDUP9fkpilCLXgIfifQ78Qw6xp2N0di8OUg9yDOi07NmXBWh5/c8ZnHFF0aBJLTNoQ5Swlah+bX1pkk1fU7rMRxRvjq08p7f4/Pa7akdxlvsSb3x4Q7Ja0jJ6cLIhmWkrTd59g5WiBl+erm+yviGSJrHmgL9RHWukQZTTa82cK9oySE2Csr9KKSwasGzW8dGF4CQAyMNS1MWKbM9U17lReuM7YoYXVzg==; "
        "bm_sv=E21A60521130DF17A3AE3692AA590F24~YAAQvv4WAjJV2MWWAQAAPclo6RvBqSbMt1ItywFBEDE8sU0mviYlqkcj8E5XmeI1QvXjZkORX5SdD9KZq/5b1d2h8vjoFQHvdbVCTBtNEf9zHMv5MITvUAs1Slo+5KC/NrsuIMweyORfs48rm1jf3TEwAPSDqscrqOg4K0d5HrvgpvZSgv1xdH2zSXGaLrwspCKf+ipgFNGbJEyT9poLrd3f4OL0+a6XHfIghdE0/ucmo/rr8Q0+appZmHG7JlE=~1; "
        "geoloc=cc=FR,rc=IDF,tp=vhigh,tz=GMT+1,la=48.87,lo=2.33; "
        "nike_locale=us/en_us; "
        "AKA_A2=A"
    ),
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=4",
    "TE": "trailers"
}

# URL de base par pays
BASE_URLS = {
    "fr": "https://api.nike.com/discover/product_wall/v1/marketplace/FR/language/fr/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647",
    "gb": "https://api.nike.com/discover/product_wall/v1/marketplace/GB/language/en-GB/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647",
    "us": "https://api.nike.com/discover/product_wall/v1/marketplace/US/language/en/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647",
}

# Dictionnaire des paths par pays, catégorie et genre
PATHS = {
    "fr": {
        "shoes": {
            "mens": "/fr/w/hommes-chaussures-nik1zy7ok",
            "womens": "/fr/w/femmes-chaussures-5e1x6zy7ok",
            "kids" : "/fr/w/kids-chaussures-v4dhzy7ok",
        },
        "clothes": {
            "mens": "/fr/w/hommes-vetements-6ymx6znik1",
            "womens": "/fr/w/femmes-vetements-5e1x6z6ymx6",
            "kids" : "/fr/w/kids-vetements-6ymx6zv4dh",

        },
        "accessories": {
            "mens": "/fr/w/hommes-accessoires-et-equipement-awwpwznik1",
            "womens": "/fr/w/femmes-accessoires-et-equipement-5e1x6zawwpw",
            "kids" : "/fr/w/kids-accessoires-et-equipement-awwpwzv4dh",
        }
    },
    "gb": {
        "shoes": {
            "mens": "/gb/w/mens-shoes-nik1zy7ok",
            "womens": "/gb/w/womens-shoes-5e1x6zy7ok",
            "kids" : "/gb/w/kids-shoes-v4dhzy7ok",

        },
        "clothes": {
            "mens": "/gb/w/mens-clothing-6ymx6znik1",
            "womens": "/gb/w/womens-clothing-5e1x6z6ymx6",
            "kids" : "/gb/w/kids-clothing-6ymx6zv4dh",

        },
        "accessories": {
            "mens": "/gb/w/mens-accessories-equipment-awwpwznik1",
            "womens": "/gb/w/womens-accessories-equipment-5e1x6zawwpw",
            "kids" : "/gb/w/kids-accessories-equipment-awwpwzv4dh",

        }
    },
    "us": {
        "shoes": {
            "mens": "/w/mens-shoes-nik1zy7ok",
            "womens": "/w/womens-shoes-5e1x6zy7ok",
            "kids" : "/w/kids-shoes-v4dhzy7ok",

        },
        "clothes": {
            "mens": "/w/mens-clothing-6ymx6znik1",
            "womens": "/w/womens-clothing-5e1x6z6ymx6",
            "kids" : "/w/kids-clothing-6ymx6zv4dh",

        },
        "accessories": {
            "mens": "/w/mens-accessories-equipment-awwpwznik1",
            "womens": "/w/womens-accessories-equipment-5e1x6zawwpw",
            "kids" : "/w/kids-accessories-equipment-awwpwzv4dh",

        }
    },

}

def extract_pdp_urls(obj):
    urls = []
    try:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "pdpUrl" and isinstance(v, dict):
                    url = v.get("url")
                    if url and "/t/" in url:
                        urls.append(url)
                else:
                    urls.extend(extract_pdp_urls(v))
        elif isinstance(obj, list):
            for item in obj:
                urls.extend(extract_pdp_urls(item))
    except Exception as e:
        print(f"⚠️ Erreur lors de l'extraction des URLs : {e}")
    return urls

def get_max(text):
    try:
        text = text.replace("}", ",")
        parts = text.split(",")
        candidate = parts[-3]
        key_value = candidate.split(":")
        max_value = key_value[-1].strip()
        return int(max_value)
    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération du max : {e}")
        return 0

def fetch_urls_for_combination(base_url, path):
    params = {
        "path": path,
        "attributeIds": "0f64ecc7-d624-4e91-b171-b83a03dd8550,16633190-45e5-4830-a068-232ac7aea82c",
        "queryType": "PRODUCTS",
        "anchor": 0,
        "count": 100,
    }

    try:
        response = requests.get(base_url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        print(f"❌ Erreur HTTP initiale pour {path} : {e}")
        return []

    max_resources = get_max(response.text)
    print(f"max anchor = {max_resources}")
    anchor = 0
    urls_collected = []

    while anchor <= max_resources:
        params["anchor"] = anchor
        try:
            response = requests.get(base_url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
        except RequestException as e:
            print(f"❌ Erreur HTTP à anchor={anchor} : {e}")
            break

        try:
            data = response.json()
            urls = extract_pdp_urls(data)
            print(f"[{path}] anchor {anchor} : {len(urls)} URLs récupérées")
            urls_collected.extend(urls)
        except Exception as e:
            print(f"❌ Erreur de parsing JSON à anchor={anchor} : {e}")
            break

        anchor += 50
        time.sleep(1)

    return sorted(set(urls_collected))

def main():
    url_collections = {}
    for country, cat_data in PATHS.items():
        url_collections[country] = {}
        for category, genders in cat_data.items():
            url_collections[country][category] = {}
            for gender, path in genders.items():
                base_url = BASE_URLS[country]
                print(f"\n=== Récupération {category} - {gender} - {country} ===")
                try:
                    urls = fetch_urls_for_combination(base_url, path)
                except Exception as e:
                    print(f"❌ Erreur lors de la récupération des URLs pour {path} : {e}")
                    urls = []

                url_collections[country][category][gender] = urls

    OUTPUT_DIR = "nike_links"
    for country, cat_data in url_collections.items():
        for category, genders in cat_data.items():
            for gender, urls in genders.items():
                if not urls:
                    continue  # Ne crée pas de fichier vide

                folder_path = os.path.join(OUTPUT_DIR, country, gender)
                try:
                    os.makedirs(folder_path, exist_ok=True)
                except Exception as e:
                    print(f"❌ Erreur création dossier {folder_path} : {e}")
                    continue

                file_path = os.path.join(folder_path, f"{category}.txt")
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        for url in urls:
                            f.write(url + "\n")
                    print(f"✅ {file_path} ({len(urls)} liens)")
                except Exception as e:
                    print(f"❌ Erreur écriture fichier {file_path} : {e}")

if __name__ == "__main__":
    main()
