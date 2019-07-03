from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import re
import time

driver = webdriver.Chrome()

driver.get("https://www.grailed.com/categories/short-sleeve-t-shirts")

total_items_raw = driver.find_element_by_xpath('//h3[@class="-summary"]').text
temp = re.search("\d+", total_items_raw)
total_items = int(temp.group())
total_pages = total_items // 98 + 1
print(total_pages)

csv_file = open('hypebeast.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

index = 1
while True:
	try:
		print("Scraping Page number " + str(index))
		index = index + 1
		driver.execute_script("window.scrollTo(0,1000)")
		# Find all the listings on the page
		time.sleep(30)
		listings = driver.find_elements_by_xpath('//div[@class="feed-item"]')
		print(listings[30:32])
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

			listing_dict['designer'] = designer
			listing_dict['description'] = description
			listing_dict['size'] = size

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

		# move to the next page after we get all the information we need.
		new_page = "https://www.grailed.com/categories/short-sleeve-t-shirts" + "?page=" + str(index)
		driver.get(new_page)

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break

csv_file.close()
driver.close()
