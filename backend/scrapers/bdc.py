import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
from .utility import create_chrome_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from models.models import DanceClass

'''

<div id='classSchedule-mainTable'>
    <div class="header" id="an5"><b><span class="headText">Thu </span>December 4, 2025</b></div> - > scan for this current day
    keep going to the end of the table
    <div class='evenRow'>
        <div class='col-1'> -> getText for time, 9:00 am EST
        <div class='col-2'>
            <div class='col'> -> getText for class title
            <div class='col'> -> getText for instructor
            <div class='col'> -> getText for room
            <div class='col'> -> getText for class duration
    <div class='oddRow'>
        ...same structure as even row
    skip class='header'
'''

def get_start_end_time(class_date: datetime, bdc_time: str, duration: str) -> tuple[datetime, datetime]:
    # bdc formats time as '9:00 am EST'
    time = bdc_time.split(' EST')[0]
    time_datetime = datetime.strptime(time, "%I:%M %p").time()
    start_time = datetime.combine(class_date, time_datetime)
    # lmao use reg ex to get the hours and minutes, ty claude
    hours = re.search(r'(\d+)\s*hour', duration)
    minutes = re.search(r'(\d+)\s*minute', duration)
    
    hours_value = int(hours.group(1)) if hours else 0
    minutes_value = int(minutes.group(1)) if minutes else 0
    end_time = start_time + timedelta(hours=hours_value, minutes=minutes_value)
    return (start_time, end_time)

def scrape_bdc_classes(url: str) -> list[DanceClass]:
    dance_class_data = []
    driver = create_chrome_driver()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, timeout=5)
        # Convert to correct format, ex: December 03, 2025
        start_date = datetime.now().strftime("%B %-d, %Y") 
        html = driver.page_source
        print(html)
        soup = BeautifulSoup(html, 'html.parser')
        start_row = soup.find('div', text=re.compile(start_date))
        class_date = datetime.now()
        if start_row:
            for row in start_row.find_next_siblings('div'):
                if row.find('span', class_='headText'):
                    class_date = class_date + timedelta(days=1)
                    break
                class_data = {
                    'title': '',
                    'instructor': '',
                    'studio': 'BDC',
                    'style': '',  
                    'date': class_date,
                    'start_time': class_date,
                    'end_time': class_date,
                    'difficulty': '',
                    'cancelled': False 
                }
                time_div = row.find('div', class_='col-1')
                inner_div = row.find('div', class_='col-2')
                if inner_div:
                    information_divs = inner_div.find_all('div', class_='col')
                    class_data['title'] = information_divs[0].getText()
                    instructor = information_divs[1].getText()
                    if instructor == 'Canceled Today':
                        class_data['cancelled'] = True
                    else:
                        class_data['instructor'] = instructor
                    # class_data['room'] = information_divs[2].getText()
                    duration = information_divs[3].getText()
                    if time_div:
                        bdc_time = time_div.getText()
                        converted_times = get_start_end_time(class_date, bdc_time, duration)
                        class_data['start_time'] = converted_times[0]
                        class_data['end_time'] = converted_times[1]
                dance_class = DanceClass(**class_data)
                dance_class_data.append(dance_class)      
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return dance_class_data

def get_bdc_classes() -> list[DanceClass]:
    url = 'https://clients.mindbodyonline.com/classic/ws?studioid=28329&stype=-103&sView=week&sLoc=0'
    return scrape_bdc_classes(url)