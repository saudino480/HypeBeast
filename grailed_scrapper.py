from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from helper import *
import csv
import re
import time
import random

#driver = webdriver.Chrome(r"C:/chromedriver/chromedriver.exe")
driver = webdriver.Chrome()

driver.get("https://www.grailed.com/categories/short-sleeve-t-shirts")

driver.execute_script("window.scrollTo(0,1000)")

time.sleep(2)

ActionChains(driver).move_to_element(driver.find_element_by_xpath('//div[@class="show-only-wrapper"]')).perform()

designer_menu = driver.find_element_by_xpath('//div[@class="designers-wrapper _collapsed"]')
designer_menu_button = designer_menu.find_element_by_xpath('.//div[@class="-collapsible-target"]')
designer_menu_button.click()

designer_cat_button = driver.find_element_by_xpath('//button[@title="View all designers"]')
designer_cat_button.click()

temp = designer_cat_button.find_element_by_xpath('.//div[@class="content"]')
designers_list = temp.find_elements_by_xpath('.//div[@class="active-indicator"]')

while True:
	try:

		temp = designer_cat.find_element_by_xpath('.//div[@class="content"]')
		designers_list = temp.find_elements_by_xpath('.//div[@class="active-indicator"]')
		last_designer = ""

		designers_list, last_designer = listing_cleaner(designers_list, last_designer)
		if(last_designer != ""):
			ActionChains(driver).move_to_element(last_designer).perform()


		for designer in designers_list:
			designer.click()
			temp_url = temp.find_element_by_xpath('.//div[@class="active-indicator -active"]')
			if morethanFifty(driver):
				brand = temp_url.find_element_by_xpath('.//h3[@class="sub-title middle"]/span').text
				filename = 'hypebeast' + '_' + brand + '.csv'
				csv_file = open(filename, 'w', encoding='utf-8', newline='')
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

							listings, last_scrapped = listing_cleaner(listings, last_scrapped)

							listing_processing(listings, writer)


					except Exception as e:
						print(e)
						csv_file.close()
						temp_url.click()
						break


			else:
				temp_url.click()

	except:
		print(e)
		csv_file.close()
		driver.close()
		break

''' LEGACY
total_scrolls = how_many_scrolls(driver)
print(total_scrolls)


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

		listings, last_scrapped = listing_cleaner(listings, last_scrapped)

		listing_processing(listings, writer)

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
'''
