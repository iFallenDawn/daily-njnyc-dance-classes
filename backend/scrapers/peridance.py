from models.models import DanceClass
from .mindbody import scrape_mindbody_widget

# https://www.peridance.com/open-classes
# widget id comes from the <healcode-widget> tag embedded on the page
def get_peridance_classes() -> list[DanceClass]:
    return scrape_mindbody_widget('f9143499b7be', 'Peridance')
