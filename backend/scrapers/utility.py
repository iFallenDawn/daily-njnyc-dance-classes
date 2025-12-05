from selenium import webdriver
from datetime import datetime

def create_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage"); 
    options.add_argument("--no-sandbox"); 
    return webdriver.Chrome(options=options)

# assuming format is something like Wednesday, Dec 10
def parse_date(date: str) -> datetime:
    date_without_year = datetime.strptime(date, "%A, %b %d")
    current_date = datetime.now()
    new_date = date_without_year.replace(year=current_date.year)
    
    days_diff = (new_date - current_date).days
    
    # If date is more than X days in the past, it's probably next year
    if days_diff < -60:  # More than 60 days in the past
        new_date = new_date.replace(year=current_date.year + 1)
    
    return new_date