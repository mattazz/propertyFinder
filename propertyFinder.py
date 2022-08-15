import requests
from bs4 import BeautifulSoup

userSearch = input("Input property search: ")
link = "https://www.lamudi.com.ph/buy/?q={}".format(userSearch)

soup = BeautifulSoup(requests.get(link).content, "html.parser")


for row in soup.select(".ListingCell-row"):
    title = row.h2.get_text(strip=True)
    link = row.a["href"]
    price = row.select_one(
        ".PriceSection-FirstPrice, .PriceSection-NoPrice"
    ).get_text(strip=True)
    desc = row.select_one(".ListingCell-shortDescription").get_text(strip=True)
    print(title)
    print(link)
    print(price)
    print(desc)
    print("=" * 80)