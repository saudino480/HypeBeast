from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import re

def listing_cleaner(listings, last_scrapped):
    if (last_scrapped in listings):
        idx = listings.index(last_scrapped) + 1
        listings = listings[idx:]
        print("I trimmed my list of ", str(idx), " entries!")
    else:
        print("I did not trim my list :(")
    last_scrapped = listings[-1]
    return listings, last_scrapped


def how_many_scrolls(webdriver):
    total_items_raw = webdriver.find_element_by_xpath('//h3[@class="-summary"]').text
    temp = re.search("\d+", total_items_raw)
    total_items = int(temp.group())
    print(total_items)

    listings = webdriver.find_elements_by_xpath('//div[@class="feed-item"]')
    items_on_page = len(listings)
    print(items_on_page)

    return((total_items // items_on_page) + 1)




def listing_processing(listings, writer):
    for listing in listings:
        listing_dict = {}
        designer = listing.find_element_by_xpath('.//h3[@class="listing-designer truncate"]').text
        description = listing.find_element_by_xpath('.//h3[@class="sub-title listing-title"]/div').text
        size = listing.find_element_by_xpath('.//h3[@class="listing-size sub-title"]').text

        #price is listed two ways, and the first will fail if it has been
        #listed before.
        try:
            price = listing.find_element_by_xpath('.//h3[@class="sub-title original-price"]/span').text
        except:
            original_price = listing.find_element_by_xpath('.//h3[@class="sub-title original-price strike-through"]/span').text
            price = listing.find_element_by_xpath('.//h3[@class="sub-title new-price"]/span').text

        #dates are sorted two ways, we want to make sure that we can get
        #the repost data as well.
        try:
            date = listing.find_element_by_xpath('.//span[@class="date-ago"]').text
            old_date = listing.find_element_by_xpath('.//span[@class="strike-through"]').text
        except:
            date = listing.find_element_by_xpath('.//span[@class="date-ago"]').text


        url = listing.find_element_by_xpath('.//a').get_attribute('href')

        listing_dict['designer'] = designer
        listing_dict['description'] = description
        listing_dict['size'] = size
        listing_dict['url'] = url

        #fill the dictionary options based on what happened above
        try:
            listing_dict['original_price'] = original_price
            listing_dict['price'] = price
        except:
            listing_dict['original_price'] = ""
            listing_dict['price'] = price


        try:
            listing_dict['date'] = date
            listing_dict['old_date'] = old_date
        except:
            listing_dict['date'] = date
            listing_dict['old_date'] = ""

        writer.writerow(listing_dict.values())
