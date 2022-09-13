import requests
from bs4 import BeautifulSoup
import pandas
from pathlib import Path

userSearch = input("Input property search: ")
link = f'https://rentpad.com.ph/q/{userSearch}'

soup = BeautifulSoup(requests.get(link).content, "html.parser")

listTitle = []
listLink = []
listPrice = []
listDec = []

for row in soup.select(".listing-holder"):
    title = row.find("span", {"itemprop": "name"})
    if title != None:
        title = title.get_text()
        listTitle.append(title)
    print(listTitle)