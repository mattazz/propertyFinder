import requests
from bs4 import BeautifulSoup
import pandas

userSearch = input("Input property search: ")
link = "https://www.lamudi.com.ph/buy/?q={}".format(userSearch)

soup = BeautifulSoup(requests.get(link).content, "html.parser")

listTitle = []
listLink = []
listPrice = []
listDesc = []

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
    listTitle.append(title)
    listLink.append(link)
    listPrice.append(price)
    listDesc.append(desc)
    # Store results in separate lists
    print(listTitle)
    print(listLink)
    print(listPrice)
    print(listDesc)

# Create dictionary file for pandas
output = {'Title': listTitle,
          'Link': listLink,
          'Price': listPrice,
          'Desc': listDesc}
# Create pandas DataFrame
df = pandas.DataFrame(output)

df.to_csv('output.csv')
