from models.models import DanceClass
from .mindbody import scrape_mindbody_widget

# https://www.pmthouseofdance.com/sign-up-for-classes
# widget id comes from the <healcode-widget> tag embedded on the page
def get_pmt_classes() -> list[DanceClass]:
    return scrape_mindbody_widget('19108839f01a', 'PMT House of Dance')
