import cohere
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables from .env file
load_dotenv()

# Now you can access the COHERE_API_KEY environment variable
cohere_api_key = os.getenv('COHERE_API_KEY')  # Ensure this is 'COHERE_API_KEY'

# Initialize the Cohere client with the API key
co = cohere.Client(api_key=cohere_api_key)

# Define the URL you want to inquire about
url = 'https://www.atlantisvanlines.com/'




# Use the client to make a request
response = co.chat(
    message=f"Go to this {url} and return the company name on their website. Exactly as it is printed. Do not change the company name - do note remove chracters from the name.",
    connectors=[{"id": "web-search"}],
    temperature=0.9
)


print(response.text)
# # Use the client to make a request
# response = co.chat(
#     message=f"What is the address of the following moving company use the following link only {url} for your search and provide the company name and provide the corresponding url in the contact information. If you cannot find the address in the provided website, look up the company name you fetched from the website in https://bbb.org/ .",
#     connectors=[{"id": "web-search"}],
#     temperature=0.1
# )


# # Use the client to make a request
# comp_name = co.chat(
#     message=f"Select the company name and information  here {response.text} for the url that matches the following {url}.",
#     temperature=0.1
# )
# print(comp_name.text)

# # comp_name=co.chat(
# #     message=f"What is the company name here for the given url: {response.text}, only return the company name that matches for the given domain{url}",
# #     temperature=0.1
# # )

# # # print(comp_name.text)
# # # Extract the text from the response
# # company_name = f"{comp_name.text}"  # Placeholder, you'll need to extract the actual company name from the response

# # # Setup Selenium WebDriver
# # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # # Navigate to BBB.org
# # driver.get("https://www.bbb.org/")

# # # Wait for the page to load and for the search input to be clickable
# # driver.implicitly_wait(10)

# # # Find the search input field and enter the company name
# # # Note: The selector might need an update based on the current website structure
# # search_input_selector = "#:Rlalal5a:"  # This looks like a dynamically generated ID and might change
# # search_input = driver.find_element(By.CSS_SELECTOR, search_input_selector)
# # search_input.send_keys(company_name)

# # # Find and click the search button
# # # The selector provided seems to be very specific and might need updating if the website's structure has changed
# # search_button_selector = "#root > div > header > div.css-fj90qq.ed7lj9y0 > div:nth-child(2) > dialog > div > form > div > div.repel > button.bds-button"
# # search_button = driver.find_element(By.CSS_SELECTOR, search_button_selector)
# # search_button.click()

# # # At this point, Selenium has entered the company name and clicked the search button on BBB.org
# # # You can continue to use Selenium to scrape the required information from the search results

# # # Don't forget to close the browser when done
# # # driver.quit()
