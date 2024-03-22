from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from openai import OpenAI
import os
from dotenv import load_dotenv
import cohere
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")



# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
# Now you can access the COHERE_API_KEY environment variable
cohere_api_key = os.getenv('COHERE_API_KEY')  # Ensure this is 'COHERE_API_KEY'

# Initialize the Cohere client with the API key
co = cohere.Client(api_key=cohere_api_key)




# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))#, options=chrome_options)

# Default values for variables
cameleon_text = "Not found"
footer_text = "Not found"
page_title = "Not found"

url = 'https://www.atlanntisvanlines.com/'

# Open the website
driver.get(f'{url}')
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


# Use the client to make a request
cohere_response = co.chat(
    message=f"What is the address of the following moving company use the following link only {url}  here is the company name {comp_name}. If you cannot find the address in the provided website, look up {comp_name} in  https://bbb.org/ .",
    connectors=[{"id": "web-search"}],
    temperature=0.1
)

print(cohere_response.text)



driver.get('https://www.bbb.org/')

# Wait for the page to fully load
driver.implicitly_wait(10)

try:
    # Since the CSS selector contains special characters, use double backslashes to escape them in Python string
    search_bar_css_selector = '#\\:Rlalal5a\\:'  # Update this if the selector changes
    search_button_css_selector = '#root > div > header > div.css-fj90qq.ed7lj9y0 > div:nth-child(2) > dialog > div > form > div > div.repel > button.bds-button'  # Update this if the selector changes

    # Find the search bar and input the company name
    search_bar = driver.find_element(By.CSS_SELECTOR, search_bar_css_selector)
    search_bar.clear()
    search_bar.send_keys(comp_name)

    # Find the search button and click it
    search_button = driver.find_element(By.CSS_SELECTOR, search_button_css_selector)
    search_button.click()

except NoSuchElementException as e:
    print(f"Element not found: {e}")
except ElementClickInterceptedException as e:
    print(f"Element not clickable: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

# Close the browser
driver.quit()