from re import search
import requests
from bs4 import BeautifulSoup
import pandas
from pathlib import Path

print("LAMUDI SEARCH")
userSearch = input("Input property search: ")
rentOrBuy = input("Rent or buy? (type in 'rent' or 'buy') ")

withPrice = input("Do you want to limit the price? (y/n) ")

if withPrice == 'n':
    link = f"https://www.lamudi.com.ph/{rentOrBuy}/?q={userSearch}"
else:
    priceRange = input("Give price range (ex. 10000-20000) ")
    link = f"https://www.lamudi.com.ph/{rentOrBuy}/price:{priceRange}/?q={userSearch}"

searchLink = link # For debugging purposes
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
print(f'Searched this link - {searchLink}')
userInput = 'y'
if path.is_file():
    print('=' * 80)
    userInput = input("File already exists, are you sure you want to overwrite? (y/n)")
if userInput == 'y':
    print("Overwriting old output.csv file...")
    df.to_csv(path)
    print("Output saved")
else:
    pass

# Additional feature
def nextPages(searchLink, soup):
    userNextPage = input("Do you want to get the next pages? (y/n)")
    
    maxPages = soup.select(".nativeDropdown")
    pageList = []
    for row in maxPages:
        parse = row.find('option').get_text(strip=True)
        pageList.append(parse)
    parsedMaxPage = pageList[1]
    converted = ''.join(parsedMaxPage[-3:])

    print(f'Max pages for this search is: {converted}')
    if userNextPage == 'y':
        userPageRange = input("How many pages? ")
        pageStart = 2
        pageEnd = int(userPageRange)
        
        while pageStart < pageEnd:
            link = searchLink + f"&page={str(pageStart)}"
            print(link)
            pageStart += 1            
            
            soup = BeautifulSoup(requests.get(link).content, "html.parser")

            # listTitle = []
            # listLink = []
            # listPrice = []
            # listDesc = []

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

        # path = Path(f'output_{pageStart}.csv')
        path = Path(f'output.csv')
        print(f'Searched this link - {searchLink}')
        if path.is_file():
            print('=' * 80)
            userInput = input("File already exists, are you sure you want to overwrite? (y/n)")
            if userInput == 'y':
                print("Overwriting old output.csv file...")
                df.to_csv(path)
                print("Output saved")
                print("Exiting...")
        else:
            print("Overwriting old output.csv file...")
            df.to_csv(path)
            print("Exiting...")


nextPages(searchLink, soup)
