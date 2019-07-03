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

ActionChains(driver).move_to_element(driver.find_element_by_xpath('//div[@class="designers-wrapper _collapsed"]')).perform()

designer_menu = driver.find_element_by_xpath('//div[@class="designers-wrapper _collapsed"]')
designer_menu_button = test.find_element_by_xpath('.//div[@class="-collapsible-target"]')
designer_menu_button.click()

desisgner_cat_button = driver.find_element_by_xpath('//button[@title="View all designers"]')
desisgner_cat_button.click()

temp = designer_cat.find_element_by_xpath('.//div[@class="content"]')
designers_list = temp.find_elements_by_xpath('.//div[@class="active-indicator"]')


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
