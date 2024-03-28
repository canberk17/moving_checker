from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import urllib.parse

chrome_options = Options()xs
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Define the company name
company_name = "Atlanntis Van Lines"  # Replace this with the actual company name you're searching for
encoded_company_name = urllib.parse.quote(company_name)
search_url = f"https://www.bbb.org/search?find_country=CAN&find_text={encoded_company_name}&page=1&sort=Relevance"

# Navigate directly to the search URL
driver.get(search_url)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.bds-h4 > a.text-blue-medium"))
    )
    
    company_links = driver.find_elements(By.CSS_SELECTOR, "h3.bds-h4 > a.text-blue-medium")
    
    for link in company_links:
        if company_name.lower() in link.text.lower():
            link.click()  # Click on the link if the company name matches
            break  # Exit the loop after clicking the matching link

    # Wait for the company profile page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    
    # Extract the average customer review text
    try:
        customer_reviews_text = driver.find_element(By.CSS_SELECTOR, "p.bds-body.text-size-5").text
        print(customer_reviews_text)
    except NoSuchElementException:
        print("Customer review information is not available.")

    # Attempt to extract the numeric rating regardless of accreditation status
    try:
        rating_numeric = driver.find_element(By.CSS_SELECTOR, ".bds-body.text-size-70").text.split('/')[0].strip()
        print(f"Rating (Numeric): {rating_numeric} / 5")
    except NoSuchElementException:
        print("Numeric rating information is not available.")

    # Check for "Accredited Since" and accreditation status
    try:
        accredited_since = driver.find_element(By.XPATH, "//p[contains(., 'Accredited Since:')]").text
        print(f"Accredited Since: {accredited_since.split(': ')[1]}")
        # try:
        #     rating_letter = driver.find_element(By.CSS_SELECTOR, "span.dtm-rating > span > span.font-bold").text
        #     print(f"Rating (Letter): {rating_letter}")
        # except NoSuchElementException:
        #     print("Letter rating information is not available.")
    except NoSuchElementException:
        # Check for non-accreditation notice
        non_accredited_notice = driver.find_element(By.XPATH, "//a[contains(text(), 'This business is not BBB Accredited')]").text
        print(non_accredited_notice)

    # Extract "Years in Business" if available
    try:
        years_in_business = driver.find_element(By.XPATH, "//p[contains(., 'Years in Business:')]").text
        print(f"Years in Business: {years_in_business.split(': ')[1]}")
    except NoSuchElementException:
        print("Years in Business information is not available.")

except TimeoutException:
    print("Timed out waiting for page elements to load.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
