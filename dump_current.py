import os
import requests
from bs4 import BeautifulSoup

urls = [
    "https://honkai-star-rail.fandom.com/wiki/Category:Stickers",
    "https://honkai-star-rail.fandom.com/wiki/Category:Stickers?from=Sticker+PPG+12+Black+Swan+02.png",
]
base = "https://honkai-star-rail.fandom.com"

links = []
for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    stickers = soup.find_all("a", class_="category-page__member-link")
    for sticker in stickers:
        links.append(base + sticker["href"])
    
# dump current to current.json
import json
with open("current.json", "w") as f:
    json.dump(links, f, indent=4)
