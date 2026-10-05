import json
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup
import requests
from models.models import DanceClass

'''
shared scrapers for studios that embed a mindbody schedule widget, there are two versions of the widget

v1 (healcode) - ilovedance, peridance, pmt
<healcode-widget data-type="schedules" data-widget-id="471574333fc9" ...>
the widget loads its html from a public endpoint, so we can request it directly
GET https://widgets.mindbodyonline.com/widgets/schedules/{widget_id}/load_markup?options[start_date]=2025-12-01
{
    "class_sessions": "<div class=\"bw-widget__day\">...", -> html starting at start_date, a week or a single day depending on how the studio set up the widget
    "calendar": "...",
    "filters": "..."
}

Example of class_sessions html
<div class="bw-widget__day"> -> each day
    <div class="bw-widget__date date-2025-12-01"> -> date of the day
    <div class="bw-session" id="173023860"> -> each class, has is-cancelled class if cancelled
        ...
        <time class="hc_starttime" datetime="2025-12-01T18:00"> -> start time
        <time class="hc_endtime" datetime="2025-12-01T19:20"> -> end time
        ...
        <div class="bw-session__name"> -> take text for class name
            <span class="bw-session__type" style="display: none;">K-pop - </span> -> hidden on the site, ignore
        <div class="bw-session__level" style="display: none;">Beg</div> -> difficulty, usually empty
        <div class="bw-session__staff"> -> take text for teacher
            <span class="bw-session__sub">(substitute)</span> -> ignore
    <div class="bw-session">
    ...
<div class="bw-widget__day bw-widget__day--empty"> -> day with no classes
...

v2 - pjm, x-space
<div class="mindbody-widget" data-widget-type="Schedules" data-widget-id="e141370d439"></div>
the widget is an iframe to a next.js page, the first week of classes is embedded in the page's data
GET https://go.mindbodyonline.com/book/widgets/schedules/view/{widget_id}/schedule
<script>self.__next_f.push([1,"..."])</script> -> join all of these to get the page data
    "locationTimezone":"America/New_York"
    "initialClasses":{
        "classes":[
            {
                "name":"Adv Beg Choreography - Youlmae Kim",
                "startDateTime":"2026-10-01T01:30:00.0000000Z",  -> utc
                "endDateTime":"2026-10-01T03:00:00.0000000Z",
                "staff":[{"displayLabel":"Youlmae Kim", ...}],    -> can be null, entries can be references like "$35" to another row in the page data
                "cancelled":false,
                ...
            }
        ],
        ...
    }
'''

WIDGET_URL = 'https://widgets.mindbodyonline.com/widgets/schedules/{widget_id}/load_markup'
WIDGET_V2_URL = 'https://go.mindbodyonline.com/book/widgets/schedules/view/{widget_id}/schedule'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
DEFAULT_TIMEZONE = 'America/New_York'

def parse_widget_day(day_div, studio: str) -> tuple[datetime | None, list[tuple[str, DanceClass]]]:
    class_date = None
    date_element = day_div.find('div', class_='bw-widget__date')
    #ex : 'bw-widget__date date-2025-12-01', need to get the year in the event the schedule goes over another year
    if date_element:
        date_classes = list(filter(lambda c: c.startswith('date-'), date_element.get('class') or []))
        if date_classes:
            class_date = datetime.strptime(date_classes[0].split('-', 1)[1], '%Y-%m-%d')

    dance_classes = []
    for session_div in day_div.find_all('div', class_='bw-session'):
        start_time_element = session_div.find('time', class_='hc_starttime')
        if not start_time_element:
            # placeholder session for days without classes
            continue
        # time is in standard iso 8601 format 2025-12-01T18:00
        start_time = datetime.fromisoformat(str(start_time_element.get('datetime')))
        session_date = class_date or start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        class_data = {
            'title': '',
            'instructor': '',
            'studio': studio,
            'style': '',
            'date': session_date,
            'start_time': start_time,
            'end_time': start_time,
            'difficulty': '',
            'cancelled': 'is-cancelled' in (session_div.get('class') or [])
        }

        end_time_element = session_div.find('time', class_='hc_endtime')
        if end_time_element:
            class_data['end_time'] = datetime.fromisoformat(str(end_time_element.get('datetime')))

        title_element = session_div.find('div', class_='bw-session__name')
        if title_element:
            type_element = title_element.find('span', class_='bw-session__type')
            if type_element:
                type_element.extract()
            class_data['title'] = title_element.getText(strip=True)

        level_element = session_div.find('div', class_='bw-session__level')
        if level_element:
            class_data['difficulty'] = level_element.getText(strip=True)

        instructor_element = session_div.find('div', class_='bw-session__staff')
        if instructor_element:
            substitute_element = instructor_element.find('span', class_='bw-session__sub')
            if substitute_element:
                substitute_element.extract()
            class_data['instructor'] = instructor_element.getText(strip=True)

        session_id = str(session_div.get('id') or f'{start_time}-{class_data['title']}')
        dance_classes.append((session_id, DanceClass(**class_data)))
    return class_date, dance_classes

def scrape_mindbody_widget(widget_id: str, studio: str, days: int = 7) -> list[DanceClass]:
    dance_class_data = []
    seen_session_ids = set()
    try:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=days)
        # some widgets return a week per request, others only a day, so keep requesting until we have enough days
        while start_date < end_date:
            params = {'options[start_date]': start_date.strftime('%Y-%m-%d')}
            response = requests.get(WIDGET_URL.format(widget_id=widget_id), params=params, headers=HEADERS, timeout=15)
            response.raise_for_status()
            html = response.json().get('class_sessions') or ''
            soup = BeautifulSoup(html, 'html.parser')
            last_date = start_date
            for day_div in soup.find_all('div', class_='bw-widget__day'):
                class_date, dance_classes = parse_widget_day(day_div, studio)
                if class_date and class_date > last_date:
                    last_date = class_date
                for session_id, dance_class in dance_classes:
                    if session_id in seen_session_ids or dance_class.date >= end_date:
                        continue
                    seen_session_ids.add(session_id)
                    dance_class_data.append(dance_class)
            start_date = last_date + timedelta(days=1)
    except Exception as e:
        print(f'Error scraping {studio}: {e}')
    return dance_class_data

def get_page_data(html: str) -> str:
    chunks = re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', html)
    return ''.join(json.loads(chunk) for chunk in chunks)

def get_page_data_rows(page_data: str) -> dict[str, str]:
    # page data is a list of rows that look like <row id>:<json>\n
    # text rows look like <row id>:T<length in hex>,<text> and are not followed by a newline
    rows = {}
    data = page_data.encode()
    position = 0
    while position < len(data):
        colon = data.find(b':', position)
        if colon == -1:
            break
        row_id = data[position:colon].decode()
        if data[colon + 1:colon + 2] == b'T':
            comma = data.find(b',', colon)
            end = comma + 1 + int(data[colon + 2:comma], 16)
            rows[row_id] = data[comma + 1:end].decode()
            position = end
        else:
            end = data.find(b'\n', colon)
            if end == -1:
                end = len(data)
            rows[row_id] = data[colon + 1:end].decode()
            position = end + 1
    return rows

def resolve_reference(rows: dict[str, str], value):
    # next.js dedupes repeated objects by replacing them with "$<row id>"
    if not isinstance(value, str) or not re.fullmatch(r'\$[0-9a-f]+', value):
        return value
    row = rows.get(value[1:])
    if not row or row[0] not in '[{':
        return None
    return json.loads(row)

def parse_utc_time(time: str, timezone: str) -> datetime:
    # rest of the scrapers use naive datetimes in the studio's local time
    return datetime.fromisoformat(time).astimezone(ZoneInfo(timezone)).replace(tzinfo=None)

def scrape_mindbody_v2_widget(widget_id: str, studio: str) -> list[DanceClass]:
    dance_class_data = []
    try:
        response = requests.get(WIDGET_V2_URL.format(widget_id=widget_id), headers=HEADERS, timeout=30)
        response.raise_for_status()
        page_data = get_page_data(response.text)
        rows = get_page_data_rows(page_data)
        classes_key = '"initialClasses":'
        classes_index = page_data.find(classes_key)
        if classes_index == -1:
            raise ValueError('could not find initialClasses in page data')
        initial_classes = json.JSONDecoder().raw_decode(page_data[classes_index + len(classes_key):])[0]
        timezone_match = re.search(r'"locationTimezone":"([^"]+)"', page_data)
        timezone = timezone_match.group(1) if timezone_match else DEFAULT_TIMEZONE
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for dance_class in initial_classes.get('classes') or []:
            try:
                start_time = parse_utc_time(dance_class['startDateTime'], timezone)
                end_time = parse_utc_time(dance_class['endDateTime'], timezone)
                # page data starts a day early
                if start_time < today:
                    continue
                instructors = []
                for staff in resolve_reference(rows, dance_class.get('staff')) or []:
                    staff = resolve_reference(rows, staff)
                    if not isinstance(staff, dict):
                        continue
                    name = (staff.get('displayLabel') or '').strip()
                    if name:
                        instructors.append(name)
                class_data = {
                    'title': (dance_class.get('name') or '').strip(),
                    'instructor': ' & '.join(instructors),
                    'studio': studio,
                    'style': '',
                    'date': start_time.replace(hour=0, minute=0, second=0, microsecond=0),
                    'start_time': start_time,
                    'end_time': end_time,
                    'difficulty': '',
                    'cancelled': bool(dance_class.get('cancelled'))
                }
                dance_class_data.append(DanceClass(**class_data))
            except Exception as e:
                print(f'Error parsing {studio} class {dance_class.get('id')}: {e}')
    except Exception as e:
        print(f'Error scraping {studio}: {e}')
    return dance_class_data
