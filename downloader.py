import os
import requests
from bs4 import BeautifulSoup
import json 
# page : https://honkai-star-rail.fandom.com/wiki/Category:Stickers

url = "https://honkai-star-rail.fandom.com/wiki/Category:Stickers"
base = "https://honkai-star-rail.fandom.com"

page = requests.get(url)
characters = [
    "Seele",
    "Pom",
    "March",
    "Stelle",
    "Caelus",
    "Bronya",
    "Arlan",
    "Clara",
    "Asta",
    "Gepard",
    "Herta",
    "Hook",
    "Himeko",
    "Kafka",
    "Pela",
    "Sampo",
    "Welt",
    "Luocha",
    "Qingque",
    "Sushang",
    "Dan",
    "Tingyun",
    "Yanqing",
    "Wolf",
    "Jing",
    "Wubbaboo",
    "Blade",
    "Luka",
    "Natasha",
    "Serval",
    "Bailu",
    "Xuan",
    "Lynx",
    "Gui",
    "Jingliu",
    "Topaz",
    "Hanya",
    "Argenti",
    "Huohuo",
    "Ratio",
    "Peppy",
    "Mei",
    "Screwllum",
    "Swan",
    "Xueyi",
    "Misha",
    "Clockie",
    "Other",
    "Sparkle",
    "Acheron",
    "Aventurine",
    "Gallagher",
    "Firefly",
    "Robin",
    "Boothill",
    "Jade",
    "Sunday",
    "Jiaoqiu",
    "Yunli",
    "Yukong",
    "Feixiao",
    "Moze",
    "Lingsha",
    "Reca",
    "Rappa",
    "Monkey",
    "Fugue"
]
soup = BeautifulSoup(page.text, "html.parser")
# check if star_rail folder exists
if not os.path.exists("star_rail"):
    os.makedirs("star_rail")


def download_image(parent: BeautifulSoup, title: str):
    img = parent.find("img")
    src = img["src"]
    # this is low res, https://static.wikia.nocookie.net/houkai-star-rail/images/9/9f/HonkaixHonkai_Sticker_1.png/revision/latest/smart/width/40/height/30?cb=20241203132203
    # remove part after /revision/latest/
    src = src.split("/revision/latest/")[0]
    # find the folder to put the image
    for char in characters:
        if char.lower() in title.lower():
            folder = char
            # create folder if not exist
            if not os.path.exists("star_rail/" + folder):
                os.makedirs("star_rail/" + folder)
            break
    else:
        folder = "other"
        if not os.path.exists("star_rail/other"):
            os.makedirs("star_rail/other")
    # add folder to title
    title = folder + "/" + title
    title = title.replace(" ", "_").lower()

    # download image
    img = requests.get(src)
    with open("star_rail/" + title, "wb") as f:
        f.write(img.content)

current = []
if os.path.exists("current.json"):
    with open ("current.json", "r") as f:
        current = json.load(f)

# get by class name category-page__member-sticker
stickers = soup.find_all("a", class_="category-page__member-link")
links = []
flag = True
for sticker in stickers:
    sticker: BeautifulSoup
    # get parent div
    parent = sticker.find_parent("li")
    links.append(base + sticker["href"])
    if base + sticker["href"] in current:
        # skip if already downloaded
        print("Skipping", sticker["title"])
        continue
    title: str = sticker["title"]
    if (title.startswith("File:") and flag):
        title = title[5:]
        print("Downloading", title)
        download_image(parent, title)
