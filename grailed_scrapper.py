from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import csv
import re
import time
import random

driver = webdriver.Chrome(r"C:/chromedriver/chromedriver.exe")

driver.get("https://www.grailed.com/categories/short-sleeve-t-shirts")

driver.execute_script("window.scrollTo(0,1000)")

total_items_raw = driver.find_element_by_xpath('//h3[@class="-summary"]').text
temp = re.search("\d+", total_items_raw)
total_items = int(temp.group())
total_pages = total_items // 98 + 1
print(total_pages)

csv_file = open('hypebeast.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
last_scrapped = ""


index = 1
while True:
	try:
		if index > 2:
			break
		print("I've scrolled " + str(index) +" times!")
		index = index + 1
		# Find all the listings on the page

		#actual timer for implementation
		time.sleep(random.randint(4, 8))


		listings = driver.find_elements_by_xpath('//div[@class="feed-item"]')
		print("Listings has: ", len(listings))
		ActionChains(driver).move_to_element(driver.find_element_by_xpath('.//div[@class="feed-item empty-item"]')).perform()

		if (last_scrapped in listings):
			idx = listings.index(last_scrapped) + 1
			#listings = listings[idx:]
			print("I trimmed my list of ", str(idx), " entries!")
		else:
			print("I did not trim my list :(")
		last_scrapped = listings[-1]

		#print(listings[30:32])
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


		# move to the next page after we get all the information we need. (LEGACY)
		#new_page = "https://www.grailed.com/categories/short-sleeve-t-shirts" + "?page=" + str(index)
		#driver.get(new_page)

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break

csv_file.close()
driver.close()
