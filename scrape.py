import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from openai import OpenAI
import os
from dotenv import load_dotenv
import cohere

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
cohere_api_key = os.getenv('COHERE_API_KEY')

# Initialize OpenAI and Cohere clients
openai_client = OpenAI(api_key=openai_api_key)
cohere_client = cohere.Client(api_key=cohere_api_key)

def scrape_website(url):
    # Initialize Chrome options for Selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Set default values for variables
    cameleon_text = "Not found"
    footer_text = "Not found"
    page_title = "Not found"

    # Open the website
    driver.get(url)
    driver.implicitly_wait(10)

    try:
        page_title = driver.title
        
        try:
            cameleon_p = driver.find_element(By.CSS_SELECTOR, '#cameleon > p')
            cameleon_text = cameleon_p.text.strip()
        except NoSuchElementException:
            cameleon_text = "Not found"

        try:
            footer = driver.find_element(By.TAG_NAME, 'footer')
            footer_text = footer.text.strip()
        except NoSuchElementException:
            footer_text = "Not found"
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        driver.quit()

    return page_title, cameleon_text, footer_text

def query_openai(comp_name, cameleon_text, footer_text, page_title):
    content_to_analyze = f"{cameleon_text} \n{footer_text} \n{page_title}"
    response = openai_client.chat.completions.create(
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
    return comp_name

def query_cohere(comp_name, url):
    response = cohere_client.chat(
        message=f"What is the address of the following moving company use the following link only {url}  here is the company name {comp_name}. If you cannot find the address in the provided website, look up {comp_name} in https://bbb.org/ .",
        connectors=[{"id": "web-search"}],
        temperature=0.1
    )
    return response.text

# Streamlit app
def main():
    st.title("Website Information Extractor")
    
    # Input from user
    user_url = st.text_input("Enter the URL of the website:")

    if st.button("Extract Information"):
        if user_url:
            page_title, cameleon_text, footer_text = scrape_website(user_url)
            comp_name = query_openai(page_title, cameleon_text, footer_text, user_url)
            cohere_response = query_cohere(comp_name, user_url)
            
            # Display extracted information
            # st.write("### Extracted Information")
            # st.write(f"**Page Title:** {page_title}")
            # st.write(f"**Cameleon Text:** {cameleon_text}")
            # st.write(f"**Footer Text:** {footer_text}")
            st.write(f"**Company Name:** {comp_name}")
            
            # st.write("### Cohere Response")
            st.write(cohere_response)
        else:
            st.error("Please enter a URL to extract information.")

if __name__ == "__main__":
    main()
