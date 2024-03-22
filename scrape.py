from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
driver.get('https://www.atlanntisvanlines.com/')

# Wait for the page to load
driver.implicitly_wait(10)

try:
    # Extract the title of the webpage
    page_title = driver.title
    print("Page Title:", page_title)
    
    # Find the footer element
    # This step might need adjustment based on the website's structure
    footer = driver.find_element(By.TAG_NAME, 'footer')
    
    # Extract text from the footer
    # This simple approach might need refinement based on the website's layout
    footer_text = footer.text
    print("Footer Content:", footer_text)
    
    # Additional logic here for more refined extraction from the footer if needed
    
except Exception as e:
    print("An error occurred:", e)

# It's a good practice to close the browser after scraping
driver.quit()
