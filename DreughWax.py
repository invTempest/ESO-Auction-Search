import re
import sys
import os
from time import time, sleep
from termcolor import colored, cprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

## Search Settings
isCraftingMat = True   # Set to True if item is a crafting mat
showOnlyTrait = False    # Set to False to allow all traits to appear
searchTrait = "Decisive"    # Weapon Traits: "Charged" "Defending" "Infused" "Nirnhoned" "Powered" "Precise" "Sharpened" "Training" "Decisive"
                            # Armor Traits: "Divines" "Invigorating" "Impenetrable" "Infused" "Nirnhoned" "Reinforced" "Sturdy" "Training" "Well-Fitted" 
                            # Jewelry Traits: "Arcane" "Bloodthirsty" "Harmony" "Healthy" "Infused" "Protective" "Robust" "Swift" "Triune"
maxAmountLegend = 7000  #130000
maxAmountEpic = 75000   #75000
maxAmountSuperior = 65000   #65000
maxAmountFine = 65000   #65000
maxAmountNormal = 65000 #65000
maxLastSeen = 30
searchURL = 'https://us.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=211&SortBy=Price&Order=asc'
##

while True:
    os.system('color')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome('C:\Windows\ChromeDriver.exe', options=options)
    driver.get(searchURL);
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    print(chr(27) + "[2J")

    for TRcount, TRItem in enumerate(soup.find('table', {'class': "trade-list-table max-width"}).find_all('tr', {'class': "cursor-pointer"}), start=1):
        for TDcount, TDItem in enumerate(TRItem.find_all('td'), start=1):
            if TDcount == 1:
                if TDItem.find('div', {'class': "item-quality-legendary"}):
                    itemType = "Legendary"
                elif TDItem.find('div', {'class': "item-quality-epic"}):
                    itemType = "Epic"
                elif TDItem.find('div', {'class': "item-quality-superior"}):
                    itemType = "Superior"
                elif TDItem.find('div', {'class': "item-quality-fine"}):
                    itemType = "Fine"
                else:
                    itemType = "Normal"
                
                if isCraftingMat:
                    itemTrait = "Crafting Mat"
                else:
                    itemTrait = TDItem.find('img').get('data-trait')
                
                NameLevel = re.split(r"\s{2,}", TDItem.get_text().replace("\n", "").strip())
                itemName = NameLevel[0]
                itemLevel = NameLevel[2]
            
            elif TDcount == 3:
                itemLocation = re.split(r"\s{2,}", TDItem.get_text().replace("\n", "").strip())
                
            elif TDcount == 4:
                itemPrice = re.split(r"\s{2,}", TDItem.get_text().replace("\n", "").strip())
                
            elif TDcount == 5:
                itemSeen = TDItem.get('data-mins-elapsed')
                
        print_legendary = lambda x: cprint(x, 'grey', 'on_yellow', attrs=['blink'])
        print_epic = lambda x: cprint(x, 'white', 'on_magenta')
        print_superior = lambda x: cprint(x, 'grey', 'on_blue')
        print_fine = lambda x: cprint(x, 'grey', 'on_green')
        print_normal = lambda x: cprint(x, 'grey', 'on_white')
        output = str(TRcount) + " " + itemType + ", " + itemTrait + ", " + itemName + ", " + itemLevel + ", " + itemLocation[0] + " " + itemLocation[1] + ", " + itemPrice[0] + ", " + itemPrice[2] + ", " + itemPrice[4] + ", " + itemSeen + " Mins ago"
        
        if showOnlyTrait:
            if itemType == "Legendary" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountLegend and int(itemSeen) <= maxLastSeen and searchTrait == itemTrait:
                print_legendary(output)
            elif itemType == "Epic" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountEpic and int(itemSeen) <= maxLastSeen and searchTrait == itemTrait:
                print_epic(output)
            elif itemType == "Superior" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountSuperior and int(itemSeen) <= maxLastSeen and searchTrait == itemTrait:
                print_superior(output)
            elif itemType == "Fine" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountFine and int(itemSeen) <= maxLastSeen and searchTrait == itemTrait:
                print_fine(output)
            elif itemType == "Normal" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountNormal and int(itemSeen) <= maxLastSeen and searchTrait == itemTrait:
                print_normal(output)
        else:
            if itemType == "Legendary" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountLegend and int(itemSeen) <= maxLastSeen:
                print_legendary(output)
            elif itemType == "Epic" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountEpic and int(itemSeen) <= maxLastSeen:
                print_epic(output)
            elif itemType == "Superior" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountSuperior and int(itemSeen) <= maxLastSeen:
                print_superior(output)
            elif itemType == "Fine" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountFine and int(itemSeen) <= maxLastSeen:
                print_fine(output)
            elif itemType == "Normal" and int(float(itemPrice[0].replace(',', ""))) <= maxAmountNormal and int(itemSeen) <= maxLastSeen:
                print_normal(output)
    sleep(5)
    driver.quit()
    sleep(55)