from models.models import DanceClass
from .mindbody import scrape_mindbody_v2_widget

# https://www.pjmdancenyc.com/
# widget id comes from the <div class="mindbody-widget"> tag embedded on the page
def get_pjm_classes() -> list[DanceClass]:
    return scrape_mindbody_v2_widget('e141370d439', 'PJM Dance NYC')
