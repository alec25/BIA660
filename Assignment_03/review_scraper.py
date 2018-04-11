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
from datetime import datetime
# import numpy as np
import pandas as pd
# Accessing the URL
url = "https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM"
driver = webdriver.Chrome(executable_path="chromedriver.exe")# "Assignment_03/chromedriver.exe"
# driver = webdriver.Chrome(executable_path="Assignment_03/chromedriver.exe") #for running in console
driver.get(url=url)
print("Loading page....")
sleep(0.75) # WAIT WAIT WAIT
# Apply filters and sort
reviewer_filter = driver.find_element_by_class_name("reviewer-type-select")
reviewer_filter.click()
sleep(0.05 + random())
reviewer_filter = driver.find_element_by_id("reviewer-type-dropdown")
Select(reviewer_filter).select_by_value("avp_only_reviews")
sleep(0.05 + random())
rated_filter = driver.find_element_by_class_name("cr-sort-dropdown")
rated_filter.click()
sleep(0.05 + random())
rated_filter = driver.find_element_by_id("sort-order-dropdown")
Select(rated_filter).select_by_value("recent")
sleep(0.05 + random())
# Harvest Reviews
# review_section = driver.find_element_by_id("cm_cr-review_list").find_elements_by_class_name("review") #"a-section review"
df = pd.DataFrame(columns=["stars", "title", "author", "date", "body", "style", "helpful"])
day_limit = datetime(2017, 1, 1).toordinal()
done = False
page_num = 1
review_count = 0
while (done==False & page_num <= 4):
    print("page num: " + str(page_num))

    review_section = driver.find_element_by_id("cm_cr-review_list").find_elements_by_class_name("review")  # "a-section review"
    for review in review_section:
        review_count += 1
        # stars = int(review.find_element_by_class_name("a-link-normal").get_attribute("title")[0]) # first char is the #stars
        # stars = review.find_element_by_css_selector("i[data-hook='review-star-rating'").find_element_by_class_name("a-icon-alt").text[0]
        stars = review.find_element_by_css_selector("a[class='a-link-normal'").get_attribute("title")[0]
        title = review.find_element_by_class_name("review-title").text
        author = review.find_element_by_css_selector("a[data-hook='review-author'").text
        # author = review.find_element_by_class_name("author").text
        raw_date = review.find_element_by_class_name("review-date").text[
                   3:]  # 3: is to remove the "on " part of the date #TEST THIS TO SEE IF IN RANGE
        ordinal = datetime.strptime(raw_date, "%B %d, %Y").toordinal()
        if ordinal < day_limit:
            done = True
            break #FINISHED!!!!!!!!!
        # date = date.fromordinal(ordinal)
        # date = datetime.date(datetime.strptime(raw_date, "%B %d, %Y"))#%-d #careful for the day of month
        body = review.find_element_by_class_name("review-text").text
        style = review.find_element_by_css_selector("a[data-hook='format-strip'").text.replace("Pattern: ", "") # replace "Pattern: " w/ ""
        raw_count = review.find_element_by_css_selector("span[data-hook='review-voting-widget'").find_element_by_class_name("a-color-secondary").text
        # raw_count = review.find_element_by_class_name("cr-vote-component").find_element_by_class_name("a-color-secondary").text
        if "One person" in raw_count:  # raw_count == "Was this review helpful to you?"
            count = 1
        elif "people found" in raw_count:
            count = int(raw_count.split()[0])
        else:
            count = 0
        df = df.append({"stars": stars, "title": title, "author": author, "date": ordinal,  # raw_date
                        "body": body, "style": style, "helpful": count}, ignore_index=True)
        print("review count: " + str(review_count))
    if done: break
    next_button = driver.find_element_by_class_name("a-last") #.find_element_by_class_name("a-form-actions")
    sleep(0.05 + random())
    next_button.click()
    page_num += 1
print("Done")
print(df.shape)
df.to_json("reviews.json")
print(df)

driver.close()