from .ilovedance import get_ilovedance_classes
from .modega import get_modega_classes
from data import danceclasses
import asyncio

async def main():
    loop = asyncio.get_event_loop()
    ilovedance_task = loop.run_in_executor(None, get_ilovedance_classes)
    modega_task = loop.run_in_executor(None, get_modega_classes)
    
    ilovedance_results, modega_results = await asyncio.gather(
        ilovedance_task,
        modega_task
    )
    dance_class_data = []
    dance_class_data.extend(ilovedance_results)
    dance_class_data.extend(modega_results)
    await danceclasses.delete_all_dance_classes()
    return await danceclasses.create_dance_classes(dance_class_data)
    
if __name__ == '__main__':
    asyncio.run(main())