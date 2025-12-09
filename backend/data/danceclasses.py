from models.models import DanceClass
from supabasedb.supabase import db
from datetime import datetime

# table is called danceclasses
supabase = db()

async def get_all_dance_classes(
    title: str | None, 
    instructor: str | None,
    studios: list[str] | None,
    style: str | None,
    date: datetime | None,
    start_time: datetime | None,
    end_time: datetime | None,
    difficulty: str | None,
    cancelled: bool | None,
    page: int,
    limit: int
) -> list:
    query = supabase.table('danceclasses').select('*')
    if title:
        query = query.ilike('title', f'%{title}%')
    if instructor: 
        query = query.ilike('instructor', f'%{instructor}%')
    if studios:
        if len(studios) == 1:
            studio_name = studios[0].lower()
            if studio_name == 'ilovedance':
                query = query.ilike('studio', '%ilovedance%')
            else:
                query = query.ilike('studio', f'%{studios}%')
        else:
            queried_studios = []
            for studio in studios:
                studio_name = studio.lower()
                if studio_name == 'ilovedance':
                    query = query.or_(f'studio.ilike.%ilovedance%')
                else:
                    queried_studios.append(f'studio.ilike.%{studio_name}%')
            if queried_studios:
                all_ors = ','.join(queried_studios)
                query = query.or_(all_ors)
    if style:
        query = query.ilike('style', f'%{style}%')
    if date:
        query = query.eq('date', date)
    if start_time:
        query = query.eq('start_time', start_time)
    if end_time:
        query = query.eq('end_time', end_time)
    if difficulty:
        query = query.ilike('difficulty', f'%{difficulty}%')
    if cancelled:
        query = query.eq('cancelled', cancelled)
    
    query.order('start_time')
    
    pagination_start = (page - 1) + limit
    pagination_end = pagination_start + limit - 1
    query = query.range(pagination_start, pagination_end)
    
    response = query.execute()
    return response.data

async def create_dance_classes(dance_class_data: list[DanceClass]) -> list:
    json_data = [dance_class.model_dump(mode='json') for dance_class in dance_class_data]
    response = supabase.table('danceclasses').insert(json_data).execute()
    return response.data

async def delete_all_dance_classes():
    # we have a stored procedure in supabase that truncates the table
    response = supabase.rpc('truncate_table', {'table_name': 'danceclasses'}).execute()
    return response.data