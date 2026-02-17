import requests
from bs4 import BeautifulSoup
import re

def get_links():
    url = "https://timpul.md"
    IMAGES_DIR = "images"
    OUTPUT_JSON = "images_info.json"

    headers = {"User-Agent": "Mozilla/5.0"}    

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    lists = soup.find("ul")

    elements = lists.find_all("li",class_=re.compile(r"menu-item-type-taxonomy"))

    with open("codulhtml.html", "w") as f:
        for e in elements:
            f.write(str(e))
            f.write("\n")

    links = {}
    for el in elements:
        # print(el.text)
        # print(el.find("a").get("href"))
        links[el.text] = el.find("a").get("href")

    return links

if __name__ == "__main__":
    links = get_links()
    for l in links:
        print(l, links[l])
