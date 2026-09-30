from models.models import DanceClass
from .arketa import scrape_arketa_classes

# https://www.phreshnyc.com/class-schedule embeds https://app.arketa.co/iframe/iamphresh/calendar
# we only want the phresh nyc location
def get_phresh_classes() -> list[DanceClass]:
    return scrape_arketa_classes('iamphresh', 'Phresh NYC', location_name='Phresh NYC')
