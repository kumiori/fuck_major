from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json

def initialize_driver(chrome_driver_path):
    """Initializes the Selenium WebDriver."""
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    return driver

def extract_journal_data_springer(driver, url):
    """Extracts journal information from a Springer journal webpage."""
    # Load the page
    driver.get(url)
    # Let the page load completely
    driver.implicitly_wait(2)
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize the dictionary to store all the extracted data
    journal_data = {}

    # Extract the journal title
    title_element = soup.find('h1', class_='app-journal-masthead__title')
    journal_data['title'] = title_element.get_text(strip=True) if title_element else None

    # Extract the Editor's name
    editor_name = soup.find('dl', class_='app-journal-overview__editor').find('li')
    journal_data['editor'] = editor_name.get_text(strip=True) if editor_name else None

    # Extract the Impact Factor and other metrics
    metrics = soup.find_all('div', class_='app-journal-overview__metric')
    for metric in metrics:
        label = metric.find('dt').get_text(strip=True)
        value = metric.find('dd').get_text(strip=True)
        if "Journal Impact Factor" in label:
            journal_data['impact_factor'] = value
        elif "5-year Journal Impact Factor" in label:
            journal_data['five_year_impact_factor'] = value
        elif "Submission to first decision" in label:
            journal_data['submission_to_first_decision'] = value
        elif "Downloads" in label:
            journal_data['downloads'] = value

    # Extract the "About the journal" section
    about_section = soup.find('div', class_='app-journal-overview__promo-text')
    journal_data['about_the_journal'] = about_section.get_text(strip=True) if about_section else None

    # Extract the Calls for Papers section
    calls_for_papers_section = soup.find('section', {'data-test': 'homepage-updates'})
    calls_for_papers_list = []
    if calls_for_papers_section:
        calls_for_papers = calls_for_papers_section.find_all('li', class_='c-list-bullets')
        for call in calls_for_papers:
            call_data = {
                'title': call.find('h3').get_text(strip=True),
                'guest_editors': call.find('p').find('strong').get_text(strip=True) if call.find('p') else None,
                'description': call.find('p').get_text(strip=True),
                # 'submission_deadline': call.find('strong').next_sibling.strip() if call.find('strong') else None
            }
            calls_for_papers_list.append(call_data)
    journal_data['calls_for_papers'] = calls_for_papers_list if calls_for_papers_list else None

    return journal_data

def extract_editorial_board_springer(driver, url):
    """Extracts editorial board information from a Springer journal editorial board page."""
    # Load the page
    driver.get(url)
    # Let the page load completely
    driver.implicitly_wait(2)
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize the list to store editorial board information
    editorial_board = []

    # Extract the Editorial Board information
    editorial_board_section = soup.find('div', class_='app-page-layout__main')
    if editorial_board_section:
        editor_groups = editorial_board_section.find_all('div', class_='c-list-bullets__item')
        for group in editor_groups:
            role_element = group.find('h3')
            role = role_element.get_text(strip=True) if role_element else 'Unknown Role'
            for editor in group.find_all('li'):
                name = editor.get_text(strip=True)
                editorial_board.append({
                    'role': role,
                    'name': name,
                })

    return editorial_board


def extract_springer_editors(url, driver):
    # Load the editors' page
    driver.get(url)
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Initialize the dictionary to store the editor data
    editorial_board = []
    
    # Extract the main editor details
    editor_section = soup.find('div', class_='placeholder-editorialBoard')
    founding_editor = ""
    regional_editors = []
    editor_data = {}

    # Start a flag to track when we are in the "Regional Editors" section
    in_regional_editors_section = False
    for s in editor_section.find_all('strong'):
        text = s.get_text(strip=True)
        print(text)
        if "Editor-in-Chief" in text:
            name = s.find('br').next_sibling.strip()
            role = "Editor-in-Chief"
            affiliation = s.find_next_sibling(string=True).strip()
        # Check if we are dealing with the Founding Editor
        if "Founding Editor" in text:
            name = s.find_next_sibling(string=True).strip()
            role = "Founding Editor"
            affiliation = s.find_next_sibling(string=True).strip()

        # Check if we are entering the Regional Editors section
        if "Regional Editors" in text:
            in_regional_editors_section = True
            role = "Regional Editor"
            continue  # Skip to next iteration to avoid adding the header itself

        # Collect all Regional Editors
        if in_regional_editors_section:
            name = text.strip().strip(',')
            affiliation = s.find_next_sibling(string=True).strip()
            # regional_editors.append(f"{name}, {affiliation}")
            
        # Stop collecting if we hit an empty string or another section
        if in_regional_editors_section and not s.find_next_sibling(string=True).strip():
            role = None
            in_regional_editors_section = False

        image = None
        
        editorial_board.append({
            'role': role,
            'name': name,
            'affiliation': affiliation,
            'image': image if image else 'No image found',
        })

    print(editorial_board)
    __import__('pdb').set_trace()
    # if editor_section:

    #     # Extracting the Editor-in-Chief
    #     editor_in_chief = editor_section.find('strong').find('br').next_sibling.strip()
        
    #     if editor_in_chief:
    #         editor_data['Editor-in-Chief'] = editor_in_chief.strip()

    #     # Extracting the Founding Editor
    #     founding_editor = editor_section.find('strong', string="Founding Editor:").find_next_sibling().find_next_sibling(text=True)
    #     if founding_editor:
    #         editor_data['Founding Editor'] = founding_editor.strip()

    #     __import__('pdb').set_trace()

    return editor_data

# Example usage
chrome_driver_path = "/usr/local/bin/chromedriver"  # Update this path if necessary
driver = initialize_driver(chrome_driver_path)

# URL for Springer journal's main page
journal_url = 'https://link.springer.com/journal/10704'

# Extract journal data from the main page
journal_data = extract_journal_data_springer(driver, journal_url)

# URL for Springer journal's editorial board page
editorial_board_url = journal_url + '/editors'

# Extract editorial board data from the editorial board page
editorial_board = extract_editorial_board_springer(driver, editorial_board_url)
editorial_board = extract_springer_editors(editorial_board_url, driver)

# Combine journal data with editorial board data
journal_data['editorial_board'] = editorial_board

# Close the WebDriver
driver.quit()
__import__('pdb').set_trace()
# The `journal_data` dictionary now contains all the extracted information
print(journal_data)