import re
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

xml = ET.parse("../data/signs/sitemap.xml")
nsmp = {
    "doc": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "image": "http://www.google.com/schemas/sitemap-image/1.1",
}


count = 0
urls = []
for url in xml.findall("doc:url", namespaces=nsmp):
    loc = url.find("doc:loc", namespaces=nsmp).text

    if "/word/" not in loc:
        continue

    x = loc.split("/")
    if x[-2].isdigit():
        count += 1
        urls.append(loc)

all_words = []
bar = tqdm(total=len(urls))
for url in urls:

    try:
        bar.update(1)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        raw = (
            soup.findAll("h1")[0]
            .text.lower()
            .replace("signs for", "")
            .replace("in sign language", "")
            .replace('"', "")
            .replace('"', "")
            .strip()
        )

        raw_words = []
        if "," in raw:
            x = raw.split(",")
            for w in x:
                raw_words.append(w.strip())
        else:
            raw_words.append(raw)

        words = []
        for w in raw_words:
            cleaned = re.sub("[\(\[].*?[\)\]]", "", w).strip()

            if cleaned in all_words:
                continue

            if " " in cleaned:
                continue

            words.append(cleaned)

        if not words:
            print(f"failed: ", raw)
            continue

        video = "https://www.handspeak.com" + soup.findAll("video")[0]["src"]

        if "-fs" in video:
            print(f"fingerspell: ", raw)
            continue

        response = requests.get(video)
        for word in words:
            with open(f"../data/signs/videos/{word}.mp4", "wb") as f:
                f.write(response.content)

        all_words += words
    except Exception as e:
        print(e)
