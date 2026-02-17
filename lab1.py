import requests
from bs4 import BeautifulSoup
import re
import json
import os
from links import get_links

headers = {"User-Agent": "Mozilla/5.0"}

OUTPUT_JSON = "images_info.json"
IMAGES_DIR = "images"


def extract_image_url(style):
    if not style:
        return None
    match = re.search(r"url\((['\"]?)(.*?)\1\)", style)
    return match.group(2) if match else None


def download_image(url, filename):
    if not url:
        return None

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    path = os.path.join(IMAGES_DIR, filename)
    with open(path, "wb") as f:
        f.write(response.content)

    return path


def get_image_links():
    links = get_links()
    os.makedirs(IMAGES_DIR, exist_ok=True)

    all_data = []
    image_counter = 1

    for topic, base_url in links.items():
        for page in range(1, 3):  # 🔹 doar 2 pagini
            url = base_url if page == 1 else f"{base_url}/page/{page}"

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")

            slides = soup.find("div", id="masonry-grid")
            if not slides:
                continue

            images = slides.find_all("div", class_="slide")

            for img in images:
                image_style = img.get("data-lazy-style")
                image_url = extract_image_url(image_style)

                date = img.find("span", class_="date meta-item tie-icon")
                desc = img.find("div", class_="thumb-desc")

                image_name = f"{topic.lower().replace(' ', '_')}_{image_counter}.jpg"
                local_image_path = download_image(image_url, image_name)

                item = {
                    "descriere_imagine": " ".join(desc.text.split()) if desc else None,
                    "autor_sursa": "Timpul.md",
                    "data_ora": date.text.strip() if date else None,
                    "tematica": topic,
                    "image_file": local_image_path
                }

                all_data.append(item)
                image_counter += 1

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_data)} records")
    print(f"Images stored in ./{IMAGES_DIR}/")


if __name__ == "__main__":
    get_image_links()