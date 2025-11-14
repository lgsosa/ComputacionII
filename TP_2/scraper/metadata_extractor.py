from bs4 import BeautifulSoup

def extract_meta(html):
    soup = BeautifulSoup(html, "lxml")
    meta = {}

    d = soup.find("meta", {"name": "description"})
    if d and d.get("content"):
        meta["description"] = d["content"]

    k = soup.find("meta", {"name": "keywords"})
    if k and k.get("content"):
        meta["keywords"] = k["content"]

    for tag in soup.find_all("meta", property=True):
        p = tag.get("property")
        if p and p.startswith("og:") and tag.get("content"):
            meta[p] = tag["content"]

    return meta
