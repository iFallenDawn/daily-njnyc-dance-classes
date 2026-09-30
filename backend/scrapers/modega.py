from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from models.models import DanceClass

'''
modega uses arketa (sutrapro.com/modega), the page loads everything from a public json api
GET https://sutrapro.com/api/widget/data?widgetName=modega&type=all&challengeId=
{
    "data": {
        "classes": [
            {
                "name": "Int./Adv. Choreography",
                "host_name": "Youran Lee",               -> instructor, multiple are joined with &
                "intensity": "All Levels",                -> can be '' or 'none'
                "start_time": 1790548200,                 -> unix timestamps
                "end_time": 1790553300,
                "timezoneCalculated": "America/New_York",
                "canceled": true,
                "deleted": false,
                ...
            }
        ],
        ...
    }
}
classes includes a few days of past classes and goes out about 7 weeks
'''

API_URL = 'https://sutrapro.com/api/widget/data'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
DEFAULT_TIMEZONE = 'America/New_York'

def parse_timestamp(timestamp: int, timezone: str) -> datetime:
    # rest of the scrapers use naive datetimes in the studio's local time
    return datetime.fromtimestamp(timestamp, ZoneInfo(timezone)).replace(tzinfo=None)

def get_difficulty(dance_class: dict) -> str:
    intensity = (dance_class.get('intensity') or '').strip()
    if intensity.lower() == 'none':
        return ''
    return intensity

def scrape_modega_classes(widget_name: str) -> list[DanceClass]:
    dance_class_data = []
    try:
        params = {
            'widgetName': widget_name,
            'type': 'all',
            'challengeId': '',
        }
        response = requests.get(API_URL, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        classes = response.json().get('data', {}).get('classes') or []
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for dance_class in classes:
            try:
                if dance_class.get('deleted'):
                    continue
                timezone = dance_class.get('timezoneCalculated') or DEFAULT_TIMEZONE
                start_time = parse_timestamp(dance_class['start_time'], timezone)
                end_time = parse_timestamp(dance_class['end_time'], timezone)
                # api returns some classes that already happened
                if start_time < today:
                    continue
                class_data = {
                    'title': dance_class.get('name') or dance_class.get('class_name') or '',
                    'instructor': (dance_class.get('host_name') or '').strip(),
                    'studio': 'Modega',
                    'style': '',
                    'date': start_time.replace(hour=0, minute=0, second=0, microsecond=0),
                    'start_time': start_time,
                    'end_time': end_time,
                    'difficulty': get_difficulty(dance_class),
                    'cancelled': bool(dance_class.get('canceled'))
                }
                dance_class_data.append(DanceClass(**class_data))
            except Exception as e:
                print(f'Error parsing modega class {dance_class.get('id')}: {e}')
    except Exception as e:
        print(e)
    dance_class_data.sort(key=lambda dance_class: dance_class.start_time)
    return dance_class_data

def get_modega_classes() -> list[DanceClass]:
    return scrape_modega_classes('modega')
