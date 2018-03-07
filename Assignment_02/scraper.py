"""
BIA-660A: Assignment 02
Alec Kulakowski
I pledge my honor that I have abided by the Stevens honor system.
"""
# Import Statements
from selenium import webdriver
from selenium.webdriver.support.select import Select
# Base URL Declaration
mlb_url = "https://www.mlb.com/" #'Assignment_01/assignment_01.data'
# driver = webdriver.Chrome(executable_path="Assignment_02/chromedriver.exe")#executable_path=r'/Users/zacharywentzell/Downloads/chromedriver'
def get_stuff(earl):
    driver = webdriver.Chrome(executable_path="Assignment_02/chromedriver.exe")
    driver.close()
get_stuff(mlb_url)




get_url = requests.get(mlb_url)
soup = bs4.BeautifulSoup(get_url.text, 'html5lib')
url = """https://www.stevens.edu/schaefer-school-engineering-science/departments/computer-science/faculty-staff"""
get_url = requests.get(url)
# get_url.text
soup = bs4.BeautifulSoup(get_url.text, 'html5lib')
big_box = soup.find('div', attrs={'class': 'view-content'})
print(big_box.prettify())

#faculty exercise
faculty_divs = big_box.find_all('div', attrs={'class': 'views-row'})
[s.find('div', attrs={'class':'views-field-title'}).text.strip() for s in faculty_divs]
faculty_divs[0].find('span', attrs={'class':'views-field-field-personnel-phone'}).text
def faculty_div_process(soup_div):
    name = soup_div.find('div', attrs='views-field-title')
    position = soup_div.find('div', attrs='views-field-field-personnel-position')
    office = soup_div.find('div', attrs='views-field-field-personnel-building-room')
    phone = soup_div.find('span', attrs='views-field-field-personnel-phone')

    return (name.text if name else 'Name Unknown',
            position.text if position else 'Position Unknown',
            office.text if office else 'Office Location Unknown',
            phone.text if phone else 'Phone Number Unknown'
            )
[faculty_div_process(f) for f in faculty_divs]


