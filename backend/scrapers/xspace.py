from models.models import DanceClass
from .mindbody import scrape_mindbody_v2_widget

# https://xspacelic.studio/schedule embeds https://brandedweb.mindbodyonline.com/iframe/v2_schedule/44235
# widget id comes from the <div class="mindbody-widget"> tag in that iframe
def get_xspace_classes() -> list[DanceClass]:
    return scrape_mindbody_v2_widget('0744235e061', 'X-Space Dance')
