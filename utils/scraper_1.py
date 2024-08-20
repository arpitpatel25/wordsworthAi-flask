import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def scrape_images(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    images = []

    for img in soup.find_all("img"):
        img_url = img.get("src")
        if not img_url:
            continue

        # Skip SVG files
        if img_url.lower().endswith(".svg"):
            continue

        # Ensure the image URL is complete
        if img_url.startswith("//"):
            img_url = "https:" + img_url

        images.append({"url": img_url})

    return images


def scrape_and_store_images(db, page_type, pages_list):
    for page in pages_list:
        images = scrape_images(page['url'])
        for image in images:
            image_data = {
                "source_url": page['url'],
                "source_type": page_type,
                "url": image['url'],
                "aspect_ratio": None,
                "file_size": None,
                "type": "https",
                "height": None,
                "width": None,
                "product_tag": page.get('handle') if page_type == "product" else None,
                "collection_tag": page.get('handle') if page_type == "collection" else None,
                "product_tags_using_a_tags_body": [],
                "collection_tags_using_a_tags_body": [],
                "product_tags_using_text_body": [],
                "product_tags_using_a_tags_scroll": [],
                "collection_tags_using_a_tags_scroll": [],
                "product_tags_using_text_scroll": []
            }
            db.image_tags.insert_one(image_data)
