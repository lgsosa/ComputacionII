from bs4 import BeautifulSoup

def parse_structure(html):
    soup = BeautifulSoup(html, "lxml")
    data = {}
    for i in range(1, 7):
        tag = f"h{i}"
        data[tag] = len(soup.find_all(tag))
    return data

def extract_title_and_links(html):
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    links = [a["href"] for a in soup.find_all("a", href=True)]
    imgs = [img.get("src") for img in soup.find_all("img") if img.get("src")]
    return {
        "title": title,
        "links": links,
        "images": imgs,
        "images_count": len(imgs)
    }
