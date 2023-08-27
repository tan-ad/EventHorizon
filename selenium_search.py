from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Replace with the path to your ChromeDriver executable
chrome_driver_path = '/path/to/chromedriver'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode

# Start the Chrome driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def fetch_events_from_google(query):
    try:
        google_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
        driver.get(google_url)

        # Find relevant elements that contain event information
        event_elements = driver.find_elements(By.CSS_SELECTOR, '.event-result')

        events = []
        for element in event_elements:
            events.append(element.text)

        return events
    except Exception as e:
        print("Error fetching events:", e)
        return None
    finally:
        driver.quit()

# Replace 'concerts near me' with your desired search query
events = fetch_events_from_google('concerts near me')

if events:
    for idx, event in enumerate(events, start=1):
        print(f"Event {idx}:\n{event}\n{'='*30}")
