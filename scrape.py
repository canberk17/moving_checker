from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Default values for variables
cameleon_text = "Not found"
footer_text = "Not found"
page_title = "Not found"

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
        cameleon_text = cameleon_p.text.strip()
    except NoSuchElementException:
        print("Cameleon Content: Not found")

    # Try to find the footer element, handling cases where a traditional footer tag might not exist
    try:
        footer = driver.find_element(By.TAG_NAME, 'footer')
        footer_text = footer.text.strip()
    except NoSuchElementException:
        print("Footer Content: Not found")
    
except Exception as e:
    print("An error occurred:", e)

# Always a good practice to close the browser after scraping
driver.quit()

# Concatenate the strings, handling potential "Not found" values gracefully
content_to_analyze = f"{cameleon_text} \n{footer_text} \n{page_title}"

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Your job is to extract only the asked information from the given text, nothing more. Make sure to provide your answers as concise as possible."},
        {"role": "user", "content": f"What is the company name here, please only return the company name from the given text exactly as it is spelled: \n{content_to_analyze}"}
    ],
    top_p=0.5,
    temperature=0.2,
    max_tokens=150,
)

comp_name = response.choices[0].message.content.strip()

print("Company Name:", comp_name)
