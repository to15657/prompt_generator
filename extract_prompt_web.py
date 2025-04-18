import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import requests
import urllib.request
from urllib.error import HTTPError, URLError
from http.cookiejar import CookieJar
from urllib.parse import urlencode
from http.cookiejar import Cookie, CookieJar
from pprint import pprint

# Chrome debugging port
DEBUGGING_PORT = 9222
chrome_profile_path="/Users/gillestost/Library/Application Support/Google/Chrome/Profile 2"

# Configure WebDriver
driver_path = '/opt/homebrew/bin/chromedriver'  # Replace with your actual chromedriver path
service = Service(executable_path=driver_path)
options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--remote-debugging-port=9222')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUGGING_PORT}")
options.add_argument(f"--user-data-dir={chrome_profile_path}")
options.add_argument("--start-maximized")  # Start Chrome maximized
driver = webdriver.Chrome(service=service, options=options)

# Download the 134 chromedriver version
# --------------------------------------
# unzip ~/Downloads/mac-arm64.zip
#
# Move it to the bin:
# ------------------
# sudo mv ~/Downloads/chromedriver-mac-arm64/chromedriver /usr/local/bin/

# Pre-requise to launch the Browser
# ---------------------------------
# "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/Users/gillestost/Library/Application\ Support/Google/Chrome/Profile\ 2"

# Launch the script
# python3.11 ./extract_web_data.py

import re

def reduce_zoom(driver, zoom_level=80):
    """
    Reduce the browser's zoom level.
    For example, setting zoom_level=80 will simulate pressing Ctrl "-" until the page is 80% zoomed.
    """
    print(f"reduce_zoom() - Reduce the zoom to zoom_level = {zoom_level}")
    driver.execute_script("document.body.style.zoom='{}%'".format(zoom_level))
    # Allow time for the page to re-render at the new zoom level
    time.sleep(4)

    # Scroll back up to the top
    driver.execute_script("window.scrollTo(0, 0);")

def scroll_down_and_back_up(driver, scroll_pixels=200, scroll_times=10, pause_time=10):
    """
    Scrolls down the page a specified number of times, waiting between each scroll,
    and then scrolls back up to the top of the page.
    
    Args:
        driver: The Selenium WebDriver instance.
        scroll_times (int): Number of times to scroll down.
        pause_time (int or float): Seconds to wait after each scroll.
    """
    # Scroll down repeatedly
    index_scroll_time = 1
    for _ in range(scroll_times):
        print(f"scroll_down_and_back_up() - Scroll time #{index_scroll_time} / {scroll_times}")
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_pixels)
        time.sleep(pause_time)
        index_scroll_time += 1
    
    # Scroll back up to the top
    driver.execute_script("window.scrollTo(0, 0);")

def renumber_prompts_generic(md_file_path):
    """
    Renumbers lines containing `- Prompt` in the given Markdown file sequentially.

    Args:
        md_file_path (str): Path to the Markdown file.
    """
    if os.path.exists(output_file):

        # Read the content of the file
        with open(md_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        # Pattern to match `- Prompt <number>`
        prompt_pattern = re.compile(r"(.*Prompt )(\d+)")
        
        new_lines = []
        prompt_counter = 1  # Start numbering from 1

        for line in lines:
            # Check if the line matches the `- Prompt` pattern
            match = prompt_pattern.match(line)
            if match: 
                # Replace the number with the updated `prompt_counter`
                before_prompt = match.group(1)  # Part before the number
                line = f"{before_prompt}{prompt_counter}\n"
                prompt_counter += 1
            
            # Append the (possibly updated) line to the new lines
            new_lines.append(line)
        
        # Write the updated content back to the file
        with open(md_file_path, "w", encoding="utf-8") as file:
            file.writelines(new_lines)

        print(f"renumber_prompts_generic() - Prompts have been renumbered in {md_file_path} up to {prompt_counter} prompts")
    else:
        print(f"renumber_prompts_generic() - {md_file_path} does not exist !")

def download_image_with_referer(image_url, referer_url, output_path):
    """
    Download an image using a specific 'referer' header.
    Args:
        image_url: The URL of the image to download.
        referer_url: The URL to set as the 'referer' header.
        output_path: The file path where the image will be saved.
    """
    try:
        # Create a session
        with requests.Session() as session:
            # Set the headers
            headers = {
                "referer": referer_url,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "authority": "www.google.com",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            }

            # Make the GET request
            response = session.get(image_url, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP status codes 4xx or 5xx

            # Save the image content
            with open(output_path, "wb") as file:
                file.write(response.content)
        
        print(f"Image successfully downloaded to: {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {image_url}: {e}")

# Scroll and load all thumbnails
def scroll_once_and_load_thumbnails(driver, max_scroll_attempts=10):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0
    nb_scroll = 0
    max_nb_scroll = 1

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for new content to load

    # Get the new scroll height
    # new_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollBy(0, arguments[0]);", 400)

    print(f"scroll_and_load_thumbnails() = last_height = {last_height}")
    #print(f"scroll_and_load_thumbnails() = new_height = {new_height}")

    nb_scroll += 1 # increase scroll counter

    # Check if new content has been loaded
    # if new_height == last_height:
    #     scroll_attempts += 1  # Increment if no new content is loaded
    # else:
    #     scroll_attempts = 0  # Reset attempts if new content is found
    #     last_height = new_height

    print(f"scroll_and_load_thumbnails() = scroll_attempts = {scroll_attempts}")
    print(f"scroll_and_load_thumbnails() = nb_scroll = {nb_scroll}")

    # Collect all thumbnails after scrolling is complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img"))
    )
    return driver.find_elements(By.CSS_SELECTOR, "img")

import re

def load_existing_prompts(output_file):
    """
    Load existing prompts from the markdown file.
    Args:
        output_file: Path to the markdown file.
    Returns:
        A list of existing prompts and a set of processed links.
    """
    processed_links = set()
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as file:
            content = file.readlines()
            # Reconstruct prompts and extract links
            for line in content:
                if line.lstrip().startswith(("- Page Link: ","* Page Link: ")):
                    link = line.split(": ", 1)[1].strip()
                    processed_links.add(link)
            print(f"Loaded {len(processed_links)} links from {output_file}.")
    else:
        print(f"No existing output file found at {output_file}. Starting fresh.")
    return processed_links

# ----------------------------------------------------------------------------------------
#                                          MAIN
# ----------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Set the base URL and output file paths
    # username = "best_all_time"
    # username = "pancholi"
    # username = "yaisroman"
    username = "openAI"
    base_url = "https://sora.com/explore/images"
    url = f"{base_url}"   #/generated
    # url = f"{base_url}/t/explore?f=all_time"   #/generated
    output_file = f"ChatGPT_prompts_{username}.md"

    # Example usage
    renumber_prompts_generic(output_file)

    # exit(1)

    # Load existing prompts and processed links
    previous_file_processed_links = load_existing_prompts(output_file)

    # DEBUG - Pretty print the processed_links set
    # print("Processed Links:")
    # pprint(processed_links)

    try:
        driver.get(url)
        # Add random delay before clicking
        time.sleep(random.uniform(4, 8))

        # Scroll and load all thumbnails
        # thumbnails = scroll_and_load_thumbnails(driver)

        print(f"Try to find img tags - WebDriverWait()")

        # Wait for the thumbnails to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img'))
        )

        # Reduce the zoom (simulate Ctrl "-" action)
        # reduce_zoom(driver, zoom_level=25) 

        # scroll_down_and_back_up(driver, scroll_pixels=250, scroll_times=100, pause_time=0.2)

        thumbnails = driver.find_elements(By.CSS_SELECTOR, 'img')

        # print(f"thumbnails found = {thumbnails}")
        num_thumbnails = len(thumbnails)
        print(f"Number of Thumbnail found = {num_thumbnails}\n")

        # exit(1)

        prompts = []
        global_index = len(previous_file_processed_links) + 1 # Start global index from the number of processed links
        print(f"Number of previous Thumbnail found in {output_file} = {global_index}\n")

        # Keep track of processed links
        max_scroll_attempts = 160  # Define the maximum number of scroll attempts (5 = 100)

        for scroll_attempt in range(1, max_scroll_attempts + 1):
            print(f"Current scroll status: {scroll_attempt + 1}/{max_scroll_attempts}")

            index = 0  # Initialize index

            while index < len(thumbnails):
                try:
                    # Refresh thumbnail list to avoid stale element issues
                    # thumbnails = driver.find_elements(By.CSS_SELECTOR, 'img')
                    img = driver.find_elements(By.TAG_NAME, "img")
                    
                    print(f"Image Index = {index} / {len(thumbnails)} for scroll #{scroll_attempt}")

                    # Check if the current index is within the bounds of the refreshed image list
                    if index >= len(img):
                        print(f"Index {index} out of range for current img list (length: {len(img)}). Breaking the loop.")
                        break

                    anchor_elements = img[index].find_elements(By.XPATH, "./ancestor::a")
                    if not anchor_elements:
                        print(f"No anchor element found for image at index {index}. Skipping.")
                        index += 1
                        continue
                    thumbnail = anchor_elements[0]
                    #print(f"Thumbnail path = {thumbnail}\n")
                    link = thumbnail.get_attribute("href")
                    #rint(f"Thumbnail link = {link}\n")

                    # Skip already processed thumbnails
                    if link in previous_file_processed_links:
                        print(f"Thumbnail already processed: {link}. Skipping.")
                        index += 1
                        continue

                    # Save the thumbnail image
                    img_tag = thumbnail.find_element(By.CSS_SELECTOR, "img")
                    img_src = img_tag.get_attribute("src")
                    #print(f"Thumbnail picture URL = {img_src} for tag ={img_tag} \n")

                    if not link.startswith("http"):
                        link = base_url + link


                    # Wait up to 10 seconds for the element to appear
                    driver.get(link)
                    prompt_element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[div[normalize-space()='Prompt']]/button | //div[div[normalize-space()='Remix']]/button")
                        )
                    )
                    prompt_text = prompt_element.text
                    # print(prompt_text)

                    print(f"Global Index = {global_index+1} / Extracted prompt: {prompt_text}\n")
                    prompt = f"# {username} * Prompt {global_index+1}\n * Page Link: {link}\n * Prompt:{prompt_text}\n![Image Link: {img_src}]({img_src})\n\n"
                    # prompts.append(f"# {username} * Prompt {global_index+1}\n * Page Link: {link}\n * Prompt:{prompt_text}\n![Image Link: {img_src}]({img_src})\n\n")

                    # Mark the thumbnail as processeds
                    previous_file_processed_links.add(link)

                    # Update the file dynamically
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.writelines(prompt)

                except (StaleElementReferenceException, TimeoutException) as e:
                    print(f"Error processing thumbnail at {link}: {e}")
                    if index < len(thumbnails):
                        index += 1  # Increment index only when valid
                    global_index += 1
                    continue  # Skip to the next thumbnail

                # Move to the next thumbnail
                if index < len(thumbnails):
                    index += 1
                global_index += 1
                time.sleep(1)  # Small delay to mimic human browsing

                # Navigate back to the main page
                # ------------------------------
                driver.get(url)
                time.sleep(5)

            # Refresh thumbnails after scrolling
            print(f"\n>>>>>>>>>>> Scrolling {scroll_attempt}/{max_scroll_attempts}\n")
            new_thumbnails = scroll_once_and_load_thumbnails(driver)
            # print(f"new_thumbnails {new_thumbnails} VS {thumbnails}")
            # if len(new_thumbnails) <= len(thumbnails):
            #     print("No new thumbnails loaded. Ending scrolling attempts.")
            #     break
            thumbnails = new_thumbnails

        print(f"Prompts saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()