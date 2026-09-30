from .ilovedance import get_ilovedance_classes
from .modega import get_modega_classes
from .dnceclub import get_dnceclub_classes
from .peridance import get_peridance_classes
from .pmt import get_pmt_classes
from .pjm import get_pjm_classes
from .phresh import get_phresh_classes
from .xspace import get_xspace_classes
from data import danceclasses
import asyncio

# add new studios here
SCRAPERS = [
    get_ilovedance_classes,
    get_modega_classes,
    get_dnceclub_classes,
    get_peridance_classes,
    get_pmt_classes,
    get_pjm_classes,
    get_phresh_classes,
    get_xspace_classes,
]

async def main():
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, scraper) for scraper in SCRAPERS]
    results = await asyncio.gather(*tasks)
    dance_class_data = []
    for result in results:
        dance_class_data.extend(result)
    await danceclasses.delete_all_dance_classes()
    return await danceclasses.create_dance_classes(dance_class_data)
    
if __name__ == '__main__':
    asyncio.run(main())
