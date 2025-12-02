import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from models.models import DanceClass

'''
Example of html
<div class="bw-widget__sessions bw-widget__sessions--hide-empty-days" data-start_date="2025-12-01"> -> overall div with all ays
    <div class="bw-widget__day"> -> each day
        <div class="bw-session"> -> each class
            ...
            <time class="hc_starttime" datetime="2025-12-01T18:00"> -> start time
            <time class="hc_endtime" datetime="2025-12-01T19:20"> -> end time
            ...
            <div class="bw-session__name"> -> take text for class name
            <div class="bw-session__staff"> -> take text for teacher
            <div class="bw-session__description"> -> take text for location
        <div class="bw-session">
        ...
    <div class="bw-widget__day">
    ...
</div>
'''

def get_ilovedancenj_classes(url: str) -> list[DanceClass]:
    driver = create_firefox_driver()
    driver.get(url)
    wait = WebDriverWait(driver, timeout=10)
    # time.sleep(3)
    date = f'{datetime.today().strftime('%Y-%m-%d')}'
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-start_date]')))
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    dance_class_data = []
    week_div = soup.find(attrs={'data-start_date': date})
    if week_div:
        days_divs = week_div.find_all('div', class_='bw-widget__day')
        for day_div in days_divs:
            session_divs = day_div.find_all('div', class_='bw-session')
            date_element = day_div.find('div', class_='bw-widget__date')
            #ex : 'bw-widget__date date-2025-12-01', need to get the year in the event the schedule goes over another year
            class_date = datetime.now()
            if date_element:
                element_classes = date_element.get('class') or []
                if isinstance(element_classes, str):
                    element_classes = [element_classes]
                if element_classes:
                    date = list(filter(lambda c: c.startswith('date-'), element_classes))[0]
                    class_date = date.split('-', 1)[1]
                    class_date = datetime.strptime(class_date, '%Y-%m-%d')
            for session_div in session_divs:
                class_data = {
                    'title': '',
                    'instructor': '',
                    'studio': 'ILoveDance',  
                    'style': '',  
                    'date': class_date,
                    'start_time': class_date,
                    'end_time': class_date,
                    'difficulty': '' 
                }  
                    
                start_time_element = session_div.find('time', class_='hc_starttime')
                if start_time_element:
                    start_time = str(start_time_element.get('datetime'))
                    # time is in standard iso 1861 format 2025-12-01T18:00
                    class_data['start_time'] = datetime.fromisoformat(start_time)
                else:
                    continue
                end_time_element = session_div.find('time', class_='hc_endtime')
                if end_time_element:
                    end_time = str(end_time_element.get('datetime'))
                    # time is in standard iso 1861 format 2025-12-01T18:00
                    class_data['end_time'] = datetime.fromisoformat(end_time)
                    
                title_element = session_div.find('div', class_='bw-session__name')
                if title_element:
                    class_data['title'] = title_element.getText(strip=True)
                    
                instructor_element = session_div.find('div', class_='bw-session__staff')
                if instructor_element:
                    class_data['instructor'] = instructor_element.getText(strip=True)
                    
                dance_class = DanceClass(**class_data)
                dance_class_data.append(dance_class)
    return dance_class_data


def create_firefox_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    return webdriver.Firefox(options=options)

def main():
    print("Hello from daily-nynyc-dance-classes!")
    get_ilovedancenj_classes("https://www.ilovedancenyc.com/instudio-classesnewjersey")


if __name__ == "__main__":
    main()
