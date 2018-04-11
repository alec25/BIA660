"""
BIA-660A: Assignment 03
Alec Kulakowski
I pledge my honor that I have abided by the Stevens honor system.
"""
# Import Statements
from selenium import webdriver
from selenium.webdriver.support.select import Select
from random import random
from time import sleep
# import numpy as np
import pandas as pd
# Accessing the URL
url = "https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM"
driver = webdriver.Chrome(executable_path="chromedriver.exe")# "Assignment_03/chromedriver.exe"
driver.get(url=url)
sleep(1.5) # WAIT WAIT WAIT
# Apply filters and sort
filter_section = driver.find_element_by_id("cm_cr-view_opt_sort_filter")
reviewer_filter = filter_section.find_element_by_id("a-autoid-12") #-announce
reviewer_filter.click()
sleep(random())
Select(reviewer_filter).select_by_visible_text('Verified purchase only')
sleep(random())