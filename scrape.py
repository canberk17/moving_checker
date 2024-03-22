from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
driver.get('https://www.tcvl.ca/')
# Wait for the page to load
driver.implicitly_wait(10)

try:
    # Extract the title of the webpage
    page_title = driver.title
    print("Page Title:", page_title)
    
    # Attempt to find the custom footer element within divs or the #cameleon > p
    try:
        cameleon_p = driver.find_element(By.CSS_SELECTOR, '#cameleon > p')
        cameleon_text = cameleon_p.text
        print("Cameleon Content:", cameleon_text)
    except NoSuchElementException:
        print("Cameleon Content: Not found")

    # Try to find the footer element, handling cases where a traditional footer tag might not exist
    try:
        footer = driver.find_element(By.TAG_NAME, 'footer')
        footer_text = footer.text
        print("Footer Content:", footer_text)
    except NoSuchElementException:
        # If a standard footer is not found, look for alternative divs acting as a footer or other indications
        print("Footer Content: Not found or replaced by custom content above")
    
    # Additional logic here for more refined extraction if needed
    
except Exception as e:
    print("An error occurred:", e)

# It's a good practice to close the browser after scraping
driver.quit()
