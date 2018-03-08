# driver.find_elements_by_tag_name
"""
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
# ok great 2a done
# inning_selector = driver.find_element_by_id('widgets').find_element_by_class_name('onscreen').find_element_by_class_name('season_select')
# Select(year_selector).select_by_value('2015')
game_type_selector = driver.find_element_by_id('widgets').find_element_by_class_name('onscreen').find_element_by_name('st_hitting_hitting_splits')
game_type_selector.click()
sleep(random()+0.5) # WAIT WAIT WAIT
Select(game_type_selector).select_by_visible_text('First Inning')#.select_by_value('i01')
team_table_ = driver.find_element_by_id('datagrid').find_element_by_tag_name('table')
table_two_b = get_table(team_table)




# print(eee)
# for team in table_path.find_elements_by_tag_name('tr'):
#     [eh.text for eh in team.find_elements_by_tag_name('td')]


# data = pd.[[e.text for e in team.find_elements_by_tag_name('td')] for team in team_table.find_elements_by_tag_name('tr')]
#
# [team for team in team_table.find_elements_by_tag_name('tr')]
# team = team_table.find_elements_by_tag_name('tr')[0]
# [''.join([eh.text for eh in team.find_elements_by_tag_name('td')]) for team in team_table.find_elements_by_tag_name('tr')]
# driver.close()





# stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
# sleep(random())
# stats_line_items[0].click()
# sleep(random())
# hitting_season_element = driver.find_element_by_id('sp_hitting_season')
# season_select = Select(hitting_season_element)


# Last thing, close driver
# driver.close()
driver.close()
print('Question 1: The team is "{}"'.format(answer_one))
print('Question 2a: The league is {} (avg home runs: {})'.format(answer_two_a_name, answer_two_a_avg))
