from selenium import webdriver

def create_firefox_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    return webdriver.Firefox(options=options)