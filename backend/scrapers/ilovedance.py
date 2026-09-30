from concurrent.futures import ThreadPoolExecutor, as_completed
from models.models import DanceClass
from .mindbody import scrape_mindbody_widget

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
            executor.submit(scrape_mindbody_widget, widget_id, f'ILoveDance {location}'): location for widget_id, location in locations
        }
        for future in as_completed(future_to_location):
            location = future_to_location[future]
            try:
                classes = future.result()
                all_dance_class_data.extend(classes)
            except Exception as e:
                print(f'Error scraping {location}: {e}')
    return all_dance_class_data
