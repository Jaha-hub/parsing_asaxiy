import json
import requests
from bs4 import BeautifulSoup

URL = 'https://asaxiy.uz'
HOST = 'https://asaxiy.uz'
def get_soup(link):
    response = requests.get(link)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_categories():
    soup = get_soup(URL)
    nav = soup.find('nav', class_='header__nav')
    categories = nav.find_all("a", class_="header__nav__link")
    data = []
    for category in categories:
        title = category.text.strip()

        data.append({
            "title" : title,
            "link" : HOST + category.get("href")
        })
    return data


def get_product(link):
    soup = get_soup(link)
    products = soup.find_all("div", class_="col-6 col-xl-3 col-md-4")
    data = []
    for product in products:
        title = product.find("span", class_="product__item__info-title").text.strip()
        price = product.find("span", class_="product__item-price").text.strip()
        old_price = product.find("span", class_="product__item-old--price").text.strip() if product.find("span", class_="product__item-old--price") else None
        img = product.find("img", class_="img-fluid lazyload").get("data-src")
        col_vo_otzivov = product.find("div", class_="product__item-info--comments").text.strip()
        link = HOST + product.select_one('a[onclick="selectItemGtag()"]').get("href")
        linka = HOST + link
        description_tag = product.find("div", class_="short-desc")
        get_description = description_tag.text.strip() if description_tag else linka
        print(get_description)
        data.append({
            "title": title,
            "price": price,
            "old_price": old_price,
            "image": img,
            "col_vo_otzivov": col_vo_otzivov,
            "link": link,
            "description" : get_description,
        })
    return data
def main():
    data = get_categories()
    for category in data:
        category ["products"] = get_product(category["link"])
    print(data)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
if __name__ == "__main__":
    main()
