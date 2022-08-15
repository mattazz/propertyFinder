import requests
from bs4 import BeautifulSoup
import pandas
from pathlib import Path

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

path = Path('output.csv')
userInput = 'y'
if path.is_file():
    print('=' * 80)
    userInput = input("File already exists, are you sure you want to overwrite? (y/n)")
if userInput == 'y':
    print("Overwriting old output.csv file...")
    df.to_csv(path)
    print("Output saved")
    print("Exiting...")
else:
    print("Exiting...")
