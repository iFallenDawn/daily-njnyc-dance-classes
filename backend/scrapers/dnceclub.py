import re
from datetime import datetime, timedelta
import requests
from models.models import DanceClass

'''
dnce.club has a public json api that the site uses for its /classes page, so no selenium needed
GET https://api.dnce.club/classes/discover?limit=100&offset=0&sort=date_asc&from_date=2025-12-01
{
    "classes": [
        {
            "title": "Beginner Heels Class",
            "location": "Pearl Studios",                  -> venue name, sometimes free text
            "address": "500 8th Avenue, New York, NY, USA", -> can be null
            "date": "2025-12-01",
            "start_time": "19:00:00",
            "end_time": "20:30:00",
            "timezone": "America/New_York",
            "status": "open" | "waitlist" | "sold_out" | "canceled",
            "latitude": 40.75, "longitude": -73.99,        -> can be null
            "profile": { "full_name": "..." },             -> instructor, null for guest instructors
            "guest_instructor_name": "...",
            "substitute_profile": { "full_name": "..." },
            "substitute_guest_name": "...",
            "studio_info": { "name": "..." },              -> null unless it's a studio on dnce.club
            ...
        }
    ],
    "total": 593,
    "has_more": true
}
the api is nationwide so we have to filter down to nj/nyc ourselves
'''

API_URL = 'https://api.dnce.club/classes/discover'
PAGE_SIZE = 100
# api 403s the default python user agent
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# rough box around nj + nyc
MIN_LAT, MAX_LAT = 38.9, 41.4
MIN_LNG, MAX_LNG = -75.6, -73.65
# fallback for classes without coordinates
NJ_NYC_PATTERN = re.compile(r'new york|nyc|\bny\b|\bnj\b|new jersey|ripley.?grier|pearl studios', re.IGNORECASE)

def is_nj_nyc(dance_class: dict) -> bool:
    lat = dance_class.get('latitude')
    lng = dance_class.get('longitude')
    if lat is not None and lng is not None:
        return MIN_LAT <= lat <= MAX_LAT and MIN_LNG <= lng <= MAX_LNG
    if dance_class.get('timezone') != 'America/New_York':
        return False
    location_text = f'{dance_class.get('address') or ''} {dance_class.get('location') or ''}'
    return bool(NJ_NYC_PATTERN.search(location_text))

def get_instructor(dance_class: dict) -> str:
    # subs take priority over the original instructor
    substitute_profile = dance_class.get('substitute_profile') or {}
    profile = dance_class.get('profile') or {}
    names = [
        substitute_profile.get('full_name'),
        dance_class.get('substitute_guest_name'),
        profile.get('full_name'),
        dance_class.get('guest_instructor_name'),
    ]
    return next((name.strip() for name in names if name and name.strip()), '')

def get_studio(dance_class: dict) -> str:
    studio_info = dance_class.get('studio_info') or {}
    return studio_info.get('name') or dance_class.get('location') or 'dnce.club'

def get_start_end_time(class_date: datetime, start: str, end: str) -> tuple[datetime, datetime]:
    # times come as 19:00:00
    start_time = datetime.combine(class_date.date(), datetime.strptime(start, '%H:%M:%S').time())
    end_time = datetime.combine(class_date.date(), datetime.strptime(end, '%H:%M:%S').time())
    # class goes past midnight
    if end_time < start_time:
        end_time += timedelta(days=1)
    return (start_time, end_time)

def fetch_dnceclub_classes() -> list[dict]:
    all_classes = []
    offset = 0
    from_date = datetime.now().strftime('%Y-%m-%d')
    while True:
        params = {
            'limit': PAGE_SIZE,
            'offset': offset,
            'sort': 'date_asc',
            'from_date': from_date,
        }
        response = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        classes = data.get('classes') or []
        all_classes.extend(classes)
        if not data.get('has_more') or not classes:
            break
        offset += len(classes)
    return all_classes

def get_dnceclub_classes() -> list[DanceClass]:
    dance_class_data = []
    try:
        for dance_class in fetch_dnceclub_classes():
            if not is_nj_nyc(dance_class):
                continue
            try:
                class_date = datetime.strptime(dance_class['date'], '%Y-%m-%d')
                start_time, end_time = get_start_end_time(class_date, dance_class['start_time'], dance_class['end_time'])
                class_data = {
                    'title': dance_class.get('title') or '',
                    'instructor': get_instructor(dance_class),
                    'studio': get_studio(dance_class),
                    'style': '',
                    'date': class_date,
                    'start_time': start_time,
                    'end_time': end_time,
                    'difficulty': '',
                    'cancelled': dance_class.get('status') == 'canceled'
                }
                dance_class_data.append(DanceClass(**class_data))
            except Exception as e:
                print(f'Error parsing dnce.club class {dance_class.get('id')}: {e}')
    except Exception as e:
        print(e)
    return dance_class_data
