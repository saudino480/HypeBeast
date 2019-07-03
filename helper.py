from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import re

def page_scroll():

  while True:

    # Get scroll height
    ### This is the difference. Moving this *inside* the loop
    ### means that it checks if scrollTo is still scrolling
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:

        # try again (can be removed)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # check if the page height has remained the same
        if new_height == last_height:
            # if so, you are done
            break
        # if not, move on to the next loop
        else:
            last_height = new_height
            continue
