from models.models import DanceClass
from .arketa import scrape_arketa_classes

# https://sutrapro.com/modega
def get_modega_classes() -> list[DanceClass]:
    return scrape_arketa_classes('modega', 'Modega')
