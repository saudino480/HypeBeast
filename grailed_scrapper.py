from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import re
import time

driver = webdriver.Chrome(r"C:/chromedriver/chromedriver.exe"))

driver.get("https://www.grailed.com/categories/short-sleeve-t-shirts")

SCROLL_PAUSE_TIME = 1

total_items_raw = driver.find_element_by_xpath('//h3[@class="-summary"]').text

temp = re.search("\d+", total_items_raw)
total_items = int(temp.group())
total_pages = total_items // len(listings) + 1
print(total_pages)

index = 1
while index True:
	try:
		print("Scraping Page number " + str(index))
		index = index + 1
		# Find all the listings on the page
		wait_listing = WebDriverWait(driver, 10)
		listings = wait_listing.until(EC.presence_of_all_elements_located((By.XPATH,
									'//h3[@class="-summary"]')))
		for listing in listings:

            listing_dict = {}

			designer = listing.find_element_by_xpath('.//h3[@class="listing-designer truncate"]').text
			description = listing.find_element_by_xpath('.//h3[@class="sub-title listing-title"]/div').text

			try:
                price = listing.find_element_by_xpath('.//h3[@class="sub-title original-price"]/span').text
            except:
                original_price = listing.find_element_by_xpath('.//h3[@class="sub-title original-price strike-through"]/span').text
                price = listing.find_element_by_xpath('.//h3[@class="sub-title new-price"]/span').text

            size = listing.find_element_by_xpath('.//h3[@class="listing-size sub-title"]').text

            try:
                date = listing.find_element_by_xpath('.//span[@class="date-ago"]').text
                old_date = listing.find_element_by_xpath('.//span[@class="strike-through"]').text
            except:
                date = listing.find_element_by_xpath('.//span[@class="date-ago"]').text

			# create a listing object that correponds to one row of our table.
			cur_listing = listing(designer=designer,
							description=description,
                            price=price,
                            original_price=original_price
							date_published=date_published,
							rating=rating)
			cur_listing.save()

		# Locate the next button on the page.
		#wait_button = WebDriverWait(driver, 10)
		#next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//li[@class="nextClick displayInlineBlock padLeft5 "]')))
		#next_button.click()
	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break
