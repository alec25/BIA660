"""# driver.find_elements_by_tag_name

BIA-660A: Assignment 02
Alec Kulakowski
I pledge my honor that I have abided by the Stevens honor system.
"""
# Import Statements
from selenium import webdriver
from selenium.webdriver.support.select import Select
from random import random
from time import sleep
import numpy as np
import pandas as pd
# Base URL Declaration
mlb_url = "https://www.mlb.com/"
# Initialize Selenium Chrome webdriver
driver = webdriver.Chrome(executable_path="chromedriver.exe")# "Assignment_02/chromedriver.exe"
driver.get(mlb_url)
sleep(random()) # WAIT WAIT WAIT
# Webpage Processing
stats_header_bar = driver.find_element_by_class_name('megamenu-static-navbar__menu-button-label')
stats_header_bar.click()
sleep(random())
stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item--stats')
stats_header_bar.click()
sleep(random()) # WAIT WAIT WAIT
team_button = driver.find_element_by_id('content_wrapper').find_element_by_link_text("Team")
team_button.click()
year_selector = driver.find_element_by_id('widgets').find_element_by_class_name('onscreen').find_element_by_class_name('season_select')
Select(year_selector).select_by_value('2015')
sleep(random()) # WAIT WAIT WAIT
game_type_selector = driver.find_element_by_id('widgets').find_element_by_class_name('onscreen').find_element_by_name('st_hitting_game_type')
game_type_selector.click()
sleep(random()+0.5) # WAIT WAIT WAIT
Select(game_type_selector).select_by_visible_text('Regular Season')
sleep(random()+0.5) # WAIT WAIT WAIT #stats_table
# home_run_sorter = driver.find_element_by_id('datagrid').find_element_by_tag_name('thead').find_element_by_class_name('dg-hr')
# home_run_sorter.click() #this works but it's uncessesary
sleep(random()) # WAIT WAIT WAIT
# team_table = driver.find_element_by_id('datagrid').find_element_by_tag_name('tbody')
team_table = driver.find_element_by_id('datagrid').find_element_by_tag_name('table')
# sorted_team_data = [team.text for team in sorted_teams]
# print(sorted_team_data)
def get_table(table_path):
    table_head = table_path.find_element_by_tag_name('thead').find_element_by_tag_name('tr')
    table_body = table_path.find_element_by_tag_name('tbody')
    head_data = np.array([e.text for e in table_head.find_elements_by_tag_name('th')])
    data = np.array([[e.text for e in team.find_elements_by_tag_name('td')] for team in table_body.find_elements_by_tag_name('tr')])
    # while(len(head_data) > len(data[:,1:])+1): head_data = head_data[:-1] #???
    data_frame = pd.DataFrame(data = data[:,1:], columns = head_data[1:], index = data[:,0])
    data_frame.replace('', np.nan, inplace=True)
    data_frame.dropna(axis=1, how='all', inplace=True)
    return data_frame
    # n_rows = len(table_path.find_elements_by_tag_name('tr'))
    # n_cols = len(table_path.find_element_by_tag_name('tr').find_elements_by_tag_name('td'))
    # for i in range(n_rows):
    #     for j in range(n_cols):
    #         element = table_path
table_one = get_table(team_table)
table_one.sort_values(by='HR', ascending=False, inplace=True)
table_one.to_csv("Assignment_02/Question_1.csv")
answer_one = table_one.iloc[0,:].loc["Team"]
#ok, whew, done with that. 90% of the effort went into that one question,
#but i guess it's only going to account for 1/5 of the grade for some reason...
table_two = table_one.sort_values(by='League', inplace=False)
table_two.to_csv("Assignment_02/Question_2a.csv")
# [eh for eh in table_two if eh.loc["League"]=="AL"]
# [print(eh) for eh in table_two.iterrows()]
al_homeruns = []
nl_homeruns = []
for team_data in table_two.iterrows():
    if team_data[1]["League"]=="AL":
        al_homeruns = al_homeruns + [int(team_data[1]["HR"])]
    else:
        nl_homeruns = nl_homeruns + [int(team_data[1]["HR"])]
if(np.mean(al_homeruns) > np.mean(nl_homeruns)):
    answer_two_a_name = "AL"
    answer_two_a_avg = np.mean(al_homeruns)
else:
    answer_two_a_name = "NL"
    answer_two_a_avg = np.mean(nl_homeruns)
# ok great 2a done ###################################################################################
# inning_selector = driver.find_element_by_id('widgets').find_element_by_class_name('onscreen').find_element_by_class_name('season_select')
# Select(year_selector).select_by_value('2015')
game_type_selector = driver.find_element_by_id('widgets').find_element_by_class_name('onscreen').find_element_by_name('st_hitting_hitting_splits')
game_type_selector.click()
sleep(random()+0.5) # WAIT WAIT WAIT
Select(game_type_selector).select_by_visible_text('First Inning')#.select_by_value('i01')
sleep(random()+0.1)
team_table_2 = driver.find_element_by_id('datagrid').find_element_by_tag_name('table')
table_two_b = get_table(team_table_2)
table_two_b.sort_values(by='League', inplace=True)
table_two_b.to_csv("Assignment_02/Question_2b.csv")
al_homeruns_b = []
nl_homeruns_b = []
for team_data in table_two_b.iterrows():
    if team_data[1]["League"]=="AL":
        al_homeruns_b = al_homeruns_b + [int(team_data[1]["HR"])]
    else:
        nl_homeruns_b = nl_homeruns_b + [int(team_data[1]["HR"])]
if(np.mean(al_homeruns_b) > np.mean(nl_homeruns_b)):
    answer_two_b_name = "AL"
    answer_two_b_avg = np.mean(al_homeruns_b)
else:
    answer_two_b_name = "NL"
    answer_two_b_avg = np.mean(nl_homeruns_b)
#ok whew, 2b done too #####################################################################################
# stats_header_bar = driver.find_element_by_class_name('megamenu-static-navbar__menu-button-label')
# stats_header_bar.click()
# sleep(random())
# stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item--stats')
# stats_header_bar.click()
team_button = driver.find_element_by_id('content_wrapper').find_element_by_link_text("Player")
team_button.click()
sleep(random()) # WAIT WAIT WAIT
year_selector = driver.find_element_by_id('widgets').find_element_by_class_name('onscreen').find_element_by_class_name('season_select')
Select(year_selector).select_by_value('2017')
sleep(random()) # WAIT WAIT WAIT
game_type_selector = driver.find_element_by_id('widgets').find_element_by_class_name('onscreen').find_element_by_name('sp_hitting_game_type') #st?
game_type_selector.click()
sleep(random()+0.5) # WAIT WAIT WAIT
Select(game_type_selector).select_by_visible_text('Regular Season')
sleep(random()+0.5) # WAIT WAIT WAIT #stats_table
team_selector = driver.find_element_by_id('sp_hitting-1').find_element_by_class_name('team_id')
team_selector.click()
sleep(random()+0.5) # WAIT WAIT WAIT
Select(team_selector).select_by_visible_text('New York Yankees')
sleep(random()+0.5) # WAIT WAIT WAIT
game_type_selector = driver.find_element_by_id('widgets').find_element_by_class_name('onscreen').find_element_by_name('sp_hitting_hitting_splits') #st
game_type_selector.click()
sleep(random()+0.5) # WAIT WAIT WAIT
Select(game_type_selector).select_by_visible_text('Select Split')#.select_by_value('i01')
sleep(random()+0.1)
home_run_sorter = driver.find_element_by_id('datagrid').find_element_by_tag_name('thead').find_element_by_class_name('dg-ops')
home_run_sorter.click() #this works but it's uncessesary
#
question_3_a_table = driver.find_element_by_id('datagrid').find_element_by_tag_name('table')
q3_table = get_table(question_3_a_table)
q3_table_min30 = pd.DataFrame(q3_table.loc[[int(i)>=30 for i in q3_table["AB"]]])
q3_table_min30.sort_values(by='AVG', ascending=False, inplace=True)
q3_table_min30.to_csv("Assignment_02/Question_3a.csv")
q3a_name = q3_table_min30.iloc[0].loc["Player"]
q3a_pos = q3_table_min30.iloc[0].loc["Pos"]







# Last thing, close driver
# driver.close()
driver.close()
print('Question 1: The team is "{}"'.format(answer_one))
print('Question 2a: The league is {} (avg home runs: {})'.format(answer_two_a_name, answer_two_a_avg))
print('Question 2b: The league is {} (avg home runs: {})'.format(answer_two_b_name, answer_two_b_avg))
print('Question 3a: The player is {} (position: {})'.format(q3a_name, q3a_pos))
