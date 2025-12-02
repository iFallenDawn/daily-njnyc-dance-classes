from selenium import webdriver

def create_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage"); 
    options.add_argument("--no-sandbox"); 
    return webdriver.Chrome(options=options)