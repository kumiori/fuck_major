from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json

"""

   ▄████████ ███    █▄   ▄████████    ▄█   ▄█▄         ▄████████    ▄███████▄    ▄████████  ▄█  ███▄▄▄▄      ▄██████▄     ▄████████    ▄████████ 
  ███    ███ ███    ███ ███    ███   ███ ▄███▀        ███    ███   ███    ███   ███    ███ ███  ███▀▀▀██▄   ███    ███   ███    ███   ███    ███ 
  ███    █▀  ███    ███ ███    █▀    ███▐██▀          ███    █▀    ███    ███   ███    ███ ███▌ ███   ███   ███    █▀    ███    █▀    ███    ███ 
 ▄███▄▄▄     ███    ███ ███         ▄█████▀           ███          ███    ███  ▄███▄▄▄▄██▀ ███▌ ███   ███  ▄███         ▄███▄▄▄      ▄███▄▄▄▄██▀ 
▀▀███▀▀▀     ███    ███ ███        ▀▀█████▄         ▀███████████ ▀█████████▀  ▀▀███▀▀▀▀▀   ███▌ ███   ███ ▀▀███ ████▄  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
  ███        ███    ███ ███    █▄    ███▐██▄                 ███   ███        ▀███████████ ███  ███   ███   ███    ███   ███    █▄  ▀███████████ 
  ███        ███    ███ ███    ███   ███ ▀███▄         ▄█    ███   ███          ███    ███ ███  ███   ███   ███    ███   ███    ███   ███    ███ 
  ███        ████████▀  ████████▀    ███   ▀█▀       ▄████████▀   ▄████▀        ███    ███ █▀    ▀█   █▀    ████████▀    ██████████   ███    ███ 
                                     ▀                                          ███    ███                                            ███    ███ 
                                     
                                                                                    
                                                    ____ ____  ___           __  ___         
                                                    /    |    \|   \         /  ]/   \        
                                                    Y  o  |  _  |    \       /  /Y     Y       
                                                    |     |  |  |  D  Y     /  / |  O  |       
                                                    |  _  |  |  |     |    /   \_|     |__     
                                                    |  |  |  |  |     |    \     l     |  T    
                                                    l__j__l__j__l_____j     \____j\___/l__j    
                                                                                        

"""


# Specify the path to your ChromeDriver
chrome_driver_path = "/usr/local/bin/chromedriver"  # Update this path if necessary

# Set up the WebDriver service
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Load the main journal page
base_url = 'https://www.sciencedirect.com/journal/journal-of-the-mechanics-and-physics-of-solids'
driver.get(base_url)

# Let the page load completely
# driver.implicitly_wait(1)

# Parse the main page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Initialize the dictionary to store all the extracted data
journal_data = {}

# Extract the journal title
title_element = soup.find('h1', {'class': 'js-title-text'})
journal_data['title'] = title_element.get_text(strip=True) if title_element else None

# Extract the Editor's name
editor_name = soup.find('h3', class_='js-editor-name')
journal_data['editor'] = editor_name.get_text(strip=True) if editor_name else None

# Extract the Article Publishing Charge (APC) for Open Access
apc_element = soup.find('div', class_='article-publishing-charge')
journal_data['apc'] = apc_element.find('span', class_='list-price u-h2').get_text(strip=True) if apc_element else None

# Extract the Time to First Decision, Review Time, and Submission to Acceptance Time
metrics = soup.find_all('div', class_='metric u-padding-s-left')
journal_data['time_to_first_decision'] = metrics[0].find('div', class_='value u-h2').get_text(strip=True) if len(metrics) > 0 else None
journal_data['review_time'] = metrics[1].find('div', class_='value u-h2').get_text(strip=True) if len(metrics) > 1 else None
journal_data['submission_to_acceptance'] = metrics[2].find('div', class_='value u-h2').get_text(strip=True) if len(metrics) > 2 else None

# Extract the Impact Factor
impact_factor = soup.find('div', class_='js-impact-factor')
journal_data['impact_factor'] = impact_factor.find('span', class_='text-l u-display-block').get_text(strip=True) if impact_factor else None

# Extract the CiteScore
citescore_element = soup.find('div', class_='js-cite-score')
journal_data['citescore'] = citescore_element.find('span', class_='text-l u-display-block').get_text(strip=True) if citescore_element else None

# Extract the "About the journal" section
about_section = soup.find('div', class_='about-container')
journal_data['about_the_journal'] = " ".join(about_section.find_all(string=True)).strip() if about_section else None

# Extract the Calls for Papers section
calls_for_papers_section = soup.find('section', class_='calls-for-papers-section')
calls_for_papers_list = []
if calls_for_papers_section:
    calls_for_papers = calls_for_papers_section.find_all('div', class_='item')
    for call in calls_for_papers:
        call_data = {
            'title': call.find('h3', class_='title').get_text(strip=True),
            'guest_editors': call.find('div', class_='text-xs u-margin-xs-top u-clr-grey8').get_text(strip=True),
            'description': call.find('div', class_='u-margin-xs-top text-s').get_text(strip=True),
            'submission_deadline': call.find('div', class_='text-xs u-padding-xs-top').get_text(strip=True).replace('Submission deadline:', '').strip()
        }
        calls_for_papers_list.append(call_data)
journal_data['calls_for_papers'] = calls_for_papers_list if calls_for_papers_list else None

# Load the editorial board page
driver.get(base_url + '/about/editorial-board')

# Let the page load completely
# driver.implicitly_wait(1)

# Parse the editorial board page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract the Editorial Board information
editorial_board_section = soup.find('div', class_='right-pane')
editorial_board = []

if editorial_board_section:
    editor_groups = editorial_board_section.find_all('div', class_='u-margin-xl-bottom')

    for section in editor_groups:
        role = section.find('h3', class_='js-editor-group-role').get_text(strip=True)
        for editor_group in section.find_all('div', class_='editor-group'):
            name = editor_group.find('h4', class_='js-editor-name').get_text(strip=True)
            affiliation = editor_group.find('p', class_='js-affiliation').get_text(strip=True)
            img_tag = editor_group.find('img', class_='editor-img')
            image = img_tag['src'] if img_tag else None

            editorial_board.append({
                'role': role,
                'name': name,
                'affiliation': affiliation,
                'image': image if image else 'No image found',
            })

journal_data['editorial_board'] = editorial_board if editorial_board else None

# Close the WebDriver
driver.quit()

# Now 'journal_data' contains all the extracted information including the editorial board
print(json.dumps(journal_data, indent=4))