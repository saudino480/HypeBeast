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
import os.path

time.sleep(5)

driver = webdriver.Chrome(r"C:/chromedriver/chromedriver.exe")
#driver = webdriver.Chrome()

driver.get("https://www.grailed.com/categories/short-sleeve-t-shirts")

#scroll down to get the page to load listings
driver.execute_script("window.scrollTo(0,1000)")

time.sleep(2)

#move designers into view
ActionChains(driver).move_to_element(driver.find_element_by_xpath('//div[@class="show-only-wrapper"]')).perform()

#close the footer
footer_begone = driver.find_element_by_xpath('//div[@class="TrustStickyFooter"]')
footer_close = footer_begone.find_element_by_xpath('.//a[@class="--close"]')
footer_close.click()

time.sleep(1)

#see helper.py
temp = click_to_designers(driver)

time.sleep(1)


#scroll_to_last_csv(driver, "C:\\Docker\\webscrapping")


#designers_list = temp.find_elements_by_xpath('.//div[@class="active-indicator"]')

time.sleep(1)
last_designer = ""

#list of CSVs to attempt to string scrolls together
files = os.listdir("C:\\Docker\\webscrapping")
files_csv = [x for x in files if x[-3:] == "csv"]
designers_csv_list = []
for dirs in files_csv:
	designers_csv_list.append(dirs.replace("hypebeast_", "").replace(".csv", "").replace("_", " "))

#last_designer_list = []

#print(designers_csv_list)

last_designer_name = ""

while True:
	try:

		#temp = driver.find_element_by_xpath('.//div[@class="content"]')
		print("")
		time.sleep(1)
		try:
			print("base loop, 1")
			designers_list = temp.find_elements_by_xpath('.//div[@class="active-indicator"]')
		except:
			print("base loop, 2")
			dummy = click_designers_menu(driver)
			time.sleep(2)
			#designers_list = temp.find_elements_by_xpath('.//div[@class="active-indicator"]')
			while not find_elem:
				sleep(1)
				designers_list = dummy.find_elements_by_xpath('.//div[@class="active-indicator"]')
				#driver.execute_script("window.scrollTo(%d, %d);" %(scroll_from, scroll_from+scroll_limit))
				driver.execute_script("arguments[0].scrollIntoView();", designers_list[-1])
				try:
					find_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text()," + name + "')]")))
				except TimeoutException:
					pass

			designers_list = temp.find_elements_by_xpath('.//div[@class="active-indicator"]')
		#print(len(designers_list))
		if (last_designer != ""):
			driver.execute_script("arguments[0].scrollIntoView();", last_designer)

		#print(last_designer)
		time.sleep(0.5)
		designers_list, last_designer = listing_cleaner(designers_list, last_designer)



		designers_list_text = []
		#print("before the for loop")
		for design_temp in designers_list:
			designers_list_text.append(design_temp.find_element_by_xpath('.//h3[@class="sub-title middle"]/span').text)
		#print(designers_list_text[0], "we made a list")
		last_designer_list = []
		last_designer_test = list(set(designers_list_text).intersection(designers_csv_list))

		try:
			last_designer_test = last_designer_test[-1]
		except:
			pass

		#print("before if")
		if ((last_designer_test != []) & (last_designer_test != designers_list_text[-1])):
			#print("in if")
			last_designer = designers_list[designers_list_text.index(last_designer_test)]

			continue

		idx = 1

		#designers_list, last_designer = listing_cleaner(designers_list, last_designer)


		print(last_designer.find_element_by_xpath('.//h3[@class="sub-title middle"]/span').text)
		last_designer_name = last_designer.find_element_by_xpath('.//h3[@class="sub-title middle"]/span').text

		for designer in designers_list:
			print("\n ***DESIGNER LOOP*** \n")
			try:
				print("DESIGNER," + " 2")
				time.sleep(0.1)
				url_smartclick(driver, designer)

			except:
				try:
					temp_url = temp.find_elements_by_xpath('.//div[@class="active-indicator active"]')
					for des in temp_url:
						driver.execute_script("arguments[0].scrollIntoView();", des)
						print("DESIGNER," + " 1.1")
						url_smartclick(driver, des)
					print("DESIGNER," + " 1")
					time.sleep(0.1)
					url_smartclick(driver, designer)

				except:
					try:
						driver.execute_script("arguments[0].scrollIntoView();", last_designer)
						#last_designer_list.append(last_designer.find_element_by_xpath('.//h3[@class="sub-title middle"]/span').text)
						time.sleep(0.1)
						print("DESIGNER," + " 3")
						url_smartclick(driver, designer)

					except:
						try:
							dummy = click_designers_menu(driver)
							time.sleep(1)
							print("DESIGNER," + " 4")
							url_smartclick(driver, designer)

						except:
							dummy = click_designers_menu(driver)
							time.sleep(1)
							driver.execute_script("arguments[0].scrollIntoView();", last_designer)
							#last_designer_list.append(last_designer.find_element_by_xpath('.//h3[@class="sub-title middle"]/span').text)
							time.sleep(0.5)
							print("DESIGNER," + " 5")
							url_smartclick(driver, designer)


			#delay = 3
			#temp_url = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="active-indicator active"]')))



			time.sleep(1)

			#catch the selected designer not rendering.
			try:
				temp_url = temp.find_element_by_xpath('.//div[@class="active-indicator active"]')
				print("TEMP URL," + " 1")
			except:
				print("TEMP URL," + " 2")
				continue
			#if morethanFifty(driver):
			#print(idx)
			idx += 1

			#check if the designer has more than 30 listings
			#if there is an existing CSV file, skip the entry.
			#otherwise, make a new CSV file with filename.
			if morethanN(driver, 29):
				print("MORE THAN N," + " 1")
				brand = temp_url.find_element_by_xpath('.//h3[@class="sub-title middle"]/span').text
				filename = 'hypebeast' + '_' + brand.replace(" ", "_").replace("/", "@@@") + '.csv'
				if (os.path.exists(filename)):
					print("MORE THAN N," + " 2")
					url_smartclick(driver, temp_url)
					continue
				else:
					print("MORE THAN N," + " 3")
					csv_file = open(filename, 'w', encoding='utf-8', newline='')
					writer = csv.writer(csv_file)
					last_scrapped = ""

				index = 1
				while True:
					try:
						print("I've scrolled " + str(index) +" times!")
						index = index + 1
						# Find all the listings on the page

						#actual timer for implementation
						time.sleep(random.randint(2, 4))

						#grab all the items, move to the end of the list to load
						#the new items
						listings = driver.find_elements_by_xpath('//div[@class="feed-item"]')
						print("Listings has: ", len(listings))
						driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('.//div[@class="feed-item empty-item"]'))

						#see helper.py
						listings, last_scrapped = listing_cleaner(listings, last_scrapped)

						listing_processing(listings, writer)


					except Exception as e:
						print(e)
						print("inner")
						csv_file.close()
						url_smartclick(driver, temp_url)
						break


			else:
				print("More than N," + " 4")
				temp_url = temp.find_element_by_xpath('.//div[@class="active-indicator active"]')
				try:
					url_smartclick(driver, temp_url)
					print("else try, " + "1")
				except:
					print("else try, " + "2")
					driver.execute_script("arguments[0].scrollIntoView();", last_designer)
					url_smartclick(driver, temp_url)

	except Exception as e:
		print(e)
		print("outter")
		#csv_file.close()
		driver.close()
		break
