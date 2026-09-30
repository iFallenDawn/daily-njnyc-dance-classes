from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from models.models import DanceClass

'''
ilovedance embeds a mindbody (healcode) schedule widget on each location page
<healcode-widget data-type="schedules" data-widget-id="471574333fc9" ...>
the widget loads its html from a public endpoint, so we can request it directly
GET https://widgets.mindbodyonline.com/widgets/schedules/{widget_id}/load_markup?options[start_date]=2025-12-01
{
    "class_sessions": "<div class=\"bw-widget__day\">...", -> html for 7 days starting at start_date
    "calendar": "...",
    "filters": "..."
}

Example of class_sessions html
<div class="bw-widget__day"> -> each day
    <div class="bw-widget__date date-2025-12-01"> -> date of the day
    <div class="bw-session"> -> each class, has is-cancelled class if cancelled
        ...
        <time class="hc_starttime" datetime="2025-12-01T18:00"> -> start time
        <time class="hc_endtime" datetime="2025-12-01T19:20"> -> end time
        ...
        <div class="bw-session__name"> -> take text for class name
            <span class="bw-session__type" style="display: none;">K-pop - </span> -> hidden on the site, ignore
        <div class="bw-session__staff"> -> take text for teacher
    <div class="bw-session">
    ...
<div class="bw-widget__day bw-widget__day--empty"> -> day with no classes
...
'''

WIDGET_URL = 'https://widgets.mindbodyonline.com/widgets/schedules/{widget_id}/load_markup'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_ilovedance_classes(widget_id: str, location: str) -> list[DanceClass]:
    dance_class_data = []
    try:
        params = {'options[start_date]': datetime.now().strftime('%Y-%m-%d')}
        response = requests.get(WIDGET_URL.format(widget_id=widget_id), params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        html = response.json().get('class_sessions') or ''
        soup = BeautifulSoup(html, 'html.parser')
        days_divs = soup.find_all('div', class_='bw-widget__day')
        for day_div in days_divs:
            session_divs = day_div.find_all('div', class_='bw-session')
            date_element = day_div.find('div', class_='bw-widget__date')
            #ex : 'bw-widget__date date-2025-12-01', need to get the year in the event the schedule goes over another year
            class_date = datetime.now()
            if date_element:
                element_classes = date_element.get('class') or []
                if isinstance(element_classes, str):
                    element_classes = [element_classes]
                date_classes = list(filter(lambda c: c.startswith('date-'), element_classes))
                if date_classes:
                    class_date = datetime.strptime(date_classes[0].split('-', 1)[1], '%Y-%m-%d')
            for session_div in session_divs:
                studio = f'ILoveDance {location}'
                class_data = {
                    'title': '',
                    'instructor': '',
                    'studio': studio,
                    'style': '',
                    'date': class_date,
                    'start_time': class_date,
                    'end_time': class_date,
                    'difficulty': '',
                    'cancelled': 'is-cancelled' in (session_div.get('class') or [])
                }

                start_time_element = session_div.find('time', class_='hc_starttime')
                if start_time_element:
                    start_time = str(start_time_element.get('datetime'))
                    # time is in standard iso 8601 format 2025-12-01T18:00
                    class_data['start_time'] = datetime.fromisoformat(start_time)
                else:
                    # placeholder session for days without classes
                    continue
                end_time_element = session_div.find('time', class_='hc_endtime')
                if end_time_element:
                    end_time = str(end_time_element.get('datetime'))
                    # time is in standard iso 8601 format 2025-12-01T18:00
                    class_data['end_time'] = datetime.fromisoformat(end_time)

                title_element = session_div.find('div', class_='bw-session__name')
                if title_element:
                    type_element = title_element.find('span', class_='bw-session__type')
                    if type_element:
                        type_element.extract()
                    class_data['title'] = title_element.getText(strip=True)

                instructor_element = session_div.find('div', class_='bw-session__staff')
                if instructor_element:
                    class_data['instructor'] = instructor_element.getText(strip=True)

                dance_class = DanceClass(**class_data)
                dance_class_data.append(dance_class)
    except Exception as e:
        print(e)
    return dance_class_data

def get_ilovedance_classes() -> list[DanceClass]:
    all_dance_class_data = []
    # widget ids come from the <healcode-widget> tag on each page
    locations = [
        # https://www.ilovedancenyc.com/instudio-classesnewjersey
        ('471574333fc9', 'New Jersey'),
        # https://www.ilovedancenyc.com/instudio-classesmanhattan
        ('471584193fc9', 'Manhattan'),
        # https://www.ilovedancenyc.com/instudio-classesqueens
        ('471556353fc9', 'Queens')
    ]
    # https://docs.python.org/3/library/concurrent.futures.html
    with ThreadPoolExecutor(max_workers = 3) as executor:
        # futures are like promises from js
        future_to_location = {
            executor.submit(scrape_ilovedance_classes, widget_id, location): location for widget_id, location in locations
        }
        for future in as_completed(future_to_location):
            location = future_to_location[future]
            try:
                classes = future.result()
                all_dance_class_data.extend(classes)
            except Exception as e:
                print(f'Error scraping {location}: {e}')
    return all_dance_class_data
