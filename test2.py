import pandas as pd
import selenium
import requests
from bs4 import BeautifulSoup
import time
#
def checkForStock(page):

  soup = BeautifulSoup(page.content, features="html.parser")
  items = soup.find("div", {"class": "item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell"})

  #find number of items
  print(len(items.find_all("div", {"class": "item-cell"})))

  rowsProcessed =[]

  for item in items.find_all("div", {"class": "item-cell"}):
    itemTitle = item.find("a", {"class": "item-title"})
    itemPromo = item.find("p", {"class": "item-promo"})
    itemPrice = item.find("li", {"class": "price-current"})
    row = []

    row.append(itemTitle.text)
    if (itemPromo):
      row.append("Sold Out")
    else:
      row.append("Available")
    row.append(itemPrice.strong)

    rowsProcessed.append(row)

  df = pd.DataFrame.from_records(rowsProcessed, columns=["Item Title", "Status", "Price"])

  return df


if __name__ == '__main__':

  print("Main line start")

  #URLS for various cards
  """RTX 3060ti"""
  URL_NVIDIA_RTX_3060TI_P1 = "https://www.newegg.com/p/pl?N=100007709%20601359415&LeftPriceRange=300+600"
  #URL_NVIDIA_RTX_3060TI_P2 = "https://www.newegg.com/p/pl?d=graphics+card&N=100007709%20600030348%20601359415&isdeptsrh=1&page=2"
  """RTX 3070"""
  URL_NVIDIA_RTX_3070_P1 = "https://www.newegg.com/p/pl?d=graphics+card&N=100007709%20600030348%20601357250&isdeptsrh=1"
  URL_NVIDIA_RTX_3070_P2 = "https://www.newegg.com/p/pl?d=graphics+card&N=100007709%20600030348%20601357250&isdeptsrh=1&page=2"
  """RTX 3070ti"""
  URL_NVIDIA_RTX_3070TI_P1 = "https://www.newegg.com/p/pl?d=graphics+card&N=100007709%20600030348%20601386504&isdeptsrh=1"

  #Lists of URLS for each GPU type RTX 30-series
  STOCK_URLS_3060TI=[URL_NVIDIA_RTX_3060TI_P1]
  STOCK_URLS_3070=[URL_NVIDIA_RTX_3070_P1, URL_NVIDIA_RTX_3070_P2]
  STOCK_URLS_3070TI=[URL_NVIDIA_RTX_3070TI_P1]

  #Check each page for each GPU
  for url in STOCK_URLS_3060TI:
    page = requests.get(url)
    stock_df = checkForStock(page)
    print(stock_df)

    if "Available" in stock_df.Status.values:
      print("LOW PRICES STOCK Available!")
      #Start Checkout 
    else:
      print("LOW PRICES out of stock")
    time.sleep(5)
  print("Main line end")
