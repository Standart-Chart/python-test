import requests
import sys
import json
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
page = 1
list_of_items = []

while True:
    response = requests.get("https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/?PAGEN_1="+ str(page),headers=headers, timeout=5, allow_redirects = True )
    html = BS(response.content, "html.parser")
    items = html.find_all(class_="bx_catalog_item_container gtm-impression-product")

    for item in items:
        product = {}
        data_product = json.loads(item.get("data-product"))
        product["name"] = data_product["item_name"].replace("Смартфон ", "")
        product["articul"] = f'{data_product["product_id"]}'
        product["price"] = f'{data_product["price"]}'

        item_articuls = item.find(class_="bx_catalog_item_articul").findChildren()

        found = False
        for item_articul in item_articuls:
            if found:
                product["memory_size"] = item_articul.text
                break
            if item_articul.get("data-prop-title") == '386':
                found = True

        list_of_items.append(product)

    last_page = html.find(class_="bx-pagination-container row").find_all("span")
    if int(last_page[-2].text) == page:
        break

    page += 1


jsonString = json.dumps(list_of_items)
jsonFile = open("smartphones.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

