from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import csv
import re
import time
import os


def url_smartclick(webdriver, url):
	try:
		url.find_element_by_xpath(".//div[@class='indicator']").click()
		print("url_smartclick," " 1")
	except:
		print("url_smartclick," " 2")
		temp = webdriver.find_element_by_xpath('//div[@class="designers-popover"]')
		temp = temp.find_element_by_xpath('.//div[@class="content"]')
		temp_designers = temp.find_elements_by_xpath('.//div[@class="active-indicator"]')
		webdriver.execute_script("arguments[0].scrollIntoView();", temp_desingers[-1])
		#ActionChains(webdriver).move_to_element(temp_designers[-1])
		url.find_element_by_xpath(".//div[@class='indicator']").click()


def click_to_designers(webdriver):
	designer_menu = webdriver.find_element_by_xpath('//div[@class="designers-wrapper _collapsed"]')
	designer_menu_button = designer_menu.find_element_by_xpath('.//div[@class="-collapsible-target"]')
	designer_menu_button.click()

	time.sleep(1)

	designer_cat_button = webdriver.find_element_by_xpath('//button[@title="View all designers"]')
	designer_cat_button.click()

	time.sleep(1)

	temp = webdriver.find_element_by_xpath('//div[@class="designers-popover"]')
	button = temp.find_element_by_xpath('.//div[@class="tabs"]/span')
	button.click()

	time.sleep(1)

	return(temp.find_element_by_xpath('.//div[@class="content"]'))


def click_designers_menu(webdriver):
	designer_cat_button = webdriver.find_element_by_xpath('//button[@title="View all designers"]')
	designer_cat_button.click()

	time.sleep(1)

	temp = webdriver.find_element_by_xpath('//div[@class="designers-popover"]')
	button = temp.find_element_by_xpath('.//div[@class="tabs"]/span')
	button.click()

	time.sleep(1)

	return(temp.find_element_by_xpath('.//div[@class="content"]'))

def how_many_scrolls(webdriver):
	total_items_raw = webdriver.find_element_by_xpath('//h3[@class="-summary"]').text
	temp = re.search("\d+", total_items_raw)
	total_items = int(temp.group())
	print(total_items)

	listings = webdriver.find_elements_by_xpath('//div[@class="feed-item"]')
	items_on_page = len(listings)
	print(items_on_page)

	return((total_items // items_on_page) + 1)


def morethanN(webdriver, n):
	total_items_raw = webdriver.find_element_by_xpath('//h3[@class="-summary"]').text
	temp = re.search("\d+", total_items_raw)
	total_items = int(temp.group())

	if total_items > n:
		return(True)
	else:
		return(False)

def smartclick(designer, last_designer, webdriver):
	try:
		designer.click()
	except:
		try:
			ActionChains(driver).move_to_element(last_designer).perform()
			designer.click()
		except:
			try:
				dummy = click_to_designers(driver)
				time.sleep(1)
				designer.click()
			except:
				dummy = click_to_designers(driver)
				time.sleep(1)
				ActionChains(driver).move_to_element(last_designer).perform()
				time.sleep(0.5)
				designer.click()


def listing_cleaner(listings, last_scrapped):
	if (last_scrapped in listings):
		idx = listings.index(last_scrapped) + 1
		listings = listings[idx:]
		print("I trimmed my list of ", str(idx), " entries!")
	else:
		print("I did not trim my list :(")
	last_scrapped = listings[-1]
	return listings, last_scrapped

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
