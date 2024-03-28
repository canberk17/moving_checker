from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException

chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get('https://www.bbb.org/')

try:
    # Wait for the search input to be present
    search_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, ":Rjalal4pa:"))
    )
    
    # Clear the input field and type the search query
    search_input.clear()
    search_input.send_keys("Trans Canada Movers")
    
    # Simulate pressing Enter
    search_input.send_keys(Keys.ENTER)
    
    # Wait for the search results to be visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "yourSearchResultsSelector"))  # Update this selector based on actual search results
    )

except TimeoutException:
    print("Timed out waiting for search results to load.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
