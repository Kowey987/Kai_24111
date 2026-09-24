# садыков искандер 24111

import csv
import json
import time

import requests
from bs4 import BeautifulSoup


BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
DELAY = 1


def parse_book(book):
    title = book.select_one("h3 a")["title"].strip()
    price = book.select_one("p.price_color").get_text(strip=True)
    availability = book.select_one("p.instock.availability").get_text(strip=True)
    return {"title": title, "price": price, "availability": availability}


def scrape_all(max_pages=5):
    all_books = []
    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        print(f"Страница {page}: {url}")

        response = requests.get(url, timeout=10)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.select("article.product_pod")
        if not books:
            break

        for book in books:
            all_books.append(parse_book(book))

        if not soup.select_one("li.next a"):
            break

        time.sleep(DELAY)

    return all_books


def save_csv(books, path="books.csv"):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)
    print(f"CSV: {path} ({len(books)} записей)")


def save_json(books, path="books.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    print(f"JSON: {path} ({len(books)} записей)")


def main():
    books = scrape_all(max_pages=5)
    print(f"Всего собрано: {len(books)}")
    save_csv(books)
    save_json(books)


if __name__ == "__main__":
    main()