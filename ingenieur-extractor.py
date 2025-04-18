# ------------------------------------------------------------------------------
# Update with the command: 
# ------------------------
#     brew install --cask chromedriver
#     xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
# ------------------------------------------------------------------------------
import sys
import logging
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Configure logging to display timestamps, log levels, and messages.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def perform_search(driver, url, placeholder_text, search_query):
    """
    Perform a search on the specified URL using the given search query.
    Returns a dictionary with the button text (if any) and the table body content.
    """
    result = {}
    try:
        # Navigate to the homepage.
        #logging.info("Navigating to %s for search query: '%s'", url, search_query)
        driver.get(url)
        
        # Wait for the search input field to be present.
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//input[@placeholder='{placeholder_text}']"))
        )
        #logging.info("Search field found (placeholder: '%s').", placeholder_text)
        
        # Clear any pre-existing text and send the search query.
        input_field.clear()
        input_field.send_keys(search_query)
        #logging.info("Entering search query: '%s'", search_query)
        input_field.send_keys(Keys.RETURN)  # Submit the search.
        
        # Attempt to capture the button text (e.g., "Aucun résultat").
        try:
            button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='ui icon buttons']/button[@class='ui basic button']")
                )
            )
            result['button_text'] = button.text.strip()
            #logging.info("Button text found: '%s'", result['button_text'])
        except Exception as e:
            logging.warning("No button found or error occurred when searching for button: %s", e)
            result['button_text'] = None
        
        # Attempt to capture the table body content if available.
        try:
            tbody_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//ui-list-table//div//table//tbody"))
            )
            
            rows = tbody_element.find_elements(By.TAG_NAME, "tr")
            if rows:

                # Regex explanation:
                #   ^          : Start of string
                #   (.*?)      : Capture group 1 - lazily matches any characters (name part)
                #   \s+        : One or more whitespace characters
                #   (\d+)      : Capture group 2 - matches one or more digits
                #   \s+        : One or more whitespace characters
                #   (.*)       : Capture group 3 - matches the rest of the string (institution and year)
                #   $          : End of string
                pattern = r"^(.*?)\s+(\d+)\s+(.*)$"

                # Use re.sub to reformat the string with semicolons
                result['table_text'] = re.sub(pattern, r"\1;\2;\3", rows[0].text.strip()).strip()

            # result['table_text'] = tbody_element.text.strip()
            #logging.info("Table content extracted.")
        except Exception as e:
            logging.warning("No table content found or error occurred when searching for table body: %s", e)
            result['table_text'] = None
        
        return result
    except Exception as e:
        logging.error("Error during search for '%s': %s", search_query, e)
        return None

def display_result(search_query, result):
    """
    Display the search result in a formatted (pretty) manner.
    """
    print("\n" + "=" * 60)
    print(f"Search result for: {search_query}")
    print("-" * 60)
    if result is None:
        print("An error occurred during the search.")
    else:
        if result.get('button_text'):
            print(f"Button Text: {result.get('button_text')}")
        if result.get('table_text'):
            print("Table Content:")
            print(result.get('table_text'))
        if not result.get('button_text') and not result.get('table_text'):
            print("No results found.")
    print("=" * 60 + "\n")


def display_result_lite(search_query, result):
    """
    Display the search result in a formatted (pretty) manner.
    """
    if result is None:
        school = "An error occurred during the search."
    else:
        if result.get('table_text'):
            school = result.get('table_text')
        if not result.get('button_text') and not result.get('table_text'):
            school = "No results found."

    print(f"{school} ")

def main():
    # ------------------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------------------
    # Path to your Chrome driver; adjust if necessary.
    driver_path = '/opt/homebrew/bin/chromedriver'  # Update with your chromedriver path
    
    # URL to be loaded.
    url = "https://repertoire.iesf.fr"
    
    # Expected placeholder text of the search input.
    placeholder_text = "Recherche"
    
    # List of names to search.
    names_to_search = [
        "Rémy Lazzerini",
        "Gilles TOST",
        "Frederic TOST"
    ]
    
    # ------------------------------------------------------------------------------
    # WebDriver Initialization
    # ------------------------------------------------------------------------------
    try:
        # Initialize the Chrome service with the specified driver path.
        service = Service(executable_path=driver_path)
        
        # Set up Chrome options.
        options = webdriver.ChromeOptions()
        # Set browser language preferences.
        options.add_experimental_option("prefs", {"intl.accept_languages": "fr,fr-FR"})
        # Uncomment the following line to run Chrome in headless mode.
        # options.add_argument('--headless')
        
        # Initialize the Chrome WebDriver with the specified service and options.
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Chrome browser initialized successfully.")
    except Exception as e:
        logging.error("Error initializing Chrome browser: %s", e)
        sys.exit(1)
    
    # ------------------------------------------------------------------------------
    # Process each search query in the list
    # ------------------------------------------------------------------------------
    try:
        print("\n" + "=" * 60)
        for name in names_to_search:
            result = perform_search(driver, url, placeholder_text, name)
            display_result_lite(name, result)
        print("=" * 60 + "\n")
    except Exception as e:
        logging.error("An error occurred during the search loop: %s", e)
    finally:
        # ------------------------------------------------------------------------------
        # Clean-up: Close the browser
        # ------------------------------------------------------------------------------
        driver.quit()
        logging.info("Browser closed.")

if __name__ == '__main__':
    main()