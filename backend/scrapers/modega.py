from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
from .driver import create_chrome_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from models.models import DanceClass

'''
<div class="card-list__card-group"> -> each of these is a day
    <div class="class-list__day border-bottom"> -> take text for day
    <div class="class-list__card"> -> each of these is a class
        <p class="dateTimeText"> -> take text for time
        <div class="card-title"> -> take text for class title
        <div class="d-flex flex-row justify-content-between align-items-center"> -> have to narrow this down for more class info
            <p class="m-0 p-0 font-weight-bold card-text"> -> first p tag has instructor name
            <p class="m-0 p-0 mb-2 card-text"> -> second p tag has location but we don't really need that
</div>

<button type="button" class="m-auto primaryColor btn btn-link">Show More</button> -> paginates 10 at a time. probably click this 5 times
'''

def parse_date(date: str) -> datetime:
    date_without_year = datetime.strptime(date, "%A, %b %d")
    current_date = datetime.now()
    new_date = date_without_year.replace(year=current_date.year)
    
    days_diff = (new_date - current_date).days
    
    # If date is more than X days in the past, it's probably next year
    if days_diff < -60:  # More than 60 days in the past
        new_date = new_date.replace(year=current_date.year + 1)
    
    return new_date

def get_start_end_time(class_date: datetime, modega_time: str):
    # modega formats time in this 05:00 PM EST • (85 min) 
    storage = modega_time.split(' EST • ')
    length = storage[1]
    length = length.split(' ')[0].replace('(', '')
    length = int(length)
    time = storage[0].split(' EST')[0]
    time_datetime = datetime.strptime(time, "%I:%M %p").time()
    start_time = datetime.combine(class_date.date(), time_datetime)
    end_time = start_time + timedelta(minutes=85)
    return (start_time, end_time)

def get_cancelled(class_tag: Tag) -> bool:
    cancelled_tag = class_tag.find('div', class_='ml-2')
    if cancelled_tag:
        if cancelled_tag.getText() == 'Canceled':
            return True
    return False

def scrape_modega_classes(url: str):
    dance_class_data = []
    driver = create_chrome_driver()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, timeout=5)
        # show 50 results, each time you click it adds 10
        for i in range(0, 5):
            show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Show More']")))
            show_more_button.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        days_divs = soup.find_all(class_='card-list__card-group')
        for day_div in days_divs:
            class_date = day_div.find('div', class_='class-list__day border-bottom')
            # Ex: Wednesday, Dec 3
            if class_date:
                class_date = parse_date(class_date.getText())
            else:
                # can't find day
                continue
            dance_class_divs = day_div.find_all('div', class_='class-list__card')
            for dance_class in dance_class_divs:
                class_data = {
                    'title': '',
                    'instructor': '',
                    'studio': 'Modega',
                    'style': '',  
                    'date': class_date,
                    'start_time': class_date,
                    'end_time': class_date,
                    'difficulty': '',
                    'cancelled': False 
                }
                time_text = dance_class.find('p', class_='dateTimeText')
                if time_text:
                    converted_times = get_start_end_time(class_date, time_text.getText())
                    class_data['start_time'] = converted_times[0]
                    class_data['end_time'] = converted_times[1]
                title = dance_class.find('div', class_='card-title')
                if title:
                    class_data['title'] = title.getText()
                inner_card_div = dance_class.find('div', class_='d-flex flex-row justify-content-between align-items-center')
                if inner_card_div:
                    info_tags = inner_card_div.find_all('p')
                    instructor = info_tags[0].getText()
                    class_data['instructor'] = instructor
                    class_data['cancelled'] = get_cancelled(inner_card_div)
                dance_class = DanceClass(**class_data)
                dance_class_data.append(dance_class)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return dance_class_data

def get_modega_classes() -> list[DanceClass]:
    url = 'https://sutrapro.com/modega'
    return scrape_modega_classes(url)