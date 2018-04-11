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
