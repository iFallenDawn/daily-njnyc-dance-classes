from models.models import DanceClass
from supabasedb.supabase import db
from datetime import datetime

# table is called danceclasses
supabase = db()

async def get_all_dance_classes(
    title: str | None, 
    instructors: list[str] | None,
    studios: list[str] | None,
    style: str | None,
    date: datetime | None,
    start_time: datetime | None,
    end_time: datetime | None,
    difficulty: str | None,
    cancelled: bool | None,
    page: int,
    limit: int
) -> dict:
    query = supabase.table('danceclasses').select('*')
    if title:
        query = query.ilike('title', f'%{title}%')
    if instructors:
        queried_instructors = []
        for instructor in instructors:
            queried_instructors.append(f'instructor.ilike.%{instructor}%')
        if queried_instructors:
            query = query.or_(','.join(queried_instructors))
    if studios:
        queried_studios = []
        for studio in studios:
            studio_name = studio.lower()
            if studio_name == 'ilovedance':
                queried_studios.append(f'studio.ilike.%ilovedance%')
            else:
                queried_studios.append(f'studio.ilike.%{studio_name}%')
        if queried_studios:
            query = query.or_(','.join(queried_studios))
    if style:
        query = query.ilike('style', f'%{style}%')
    if date:
        query = query.eq('date', date)
    if start_time:
        query = query.gte('start_time', start_time)
    if end_time:
        query = query.lte('end_time', end_time)
    if difficulty:
        query = query.ilike('difficulty', f'%{difficulty}%')
    if cancelled:
        query = query.eq('cancelled', cancelled)
    
    # Get total count first
    count_query = supabase.table('danceclasses').select('*', count='exact')
    if title:
        count_query = count_query.ilike('title', f'%{title}%')
    if instructors:
        queried_instructors = []
        for instructor in instructors:
            queried_instructors.append(f'instructor.ilike.%{instructor}%')
        if queried_instructors:
            count_query = count_query.or_(','.join(queried_instructors))
    if studios:
        queried_studios = []
        for studio in studios:
            studio_name = studio.lower()
            if studio_name == 'ilovedance':
                queried_studios.append(f'studio.ilike.%ilovedance%')
            else:
                queried_studios.append(f'studio.ilike.%{studio_name}%')
        if queried_studios:
            count_query = count_query.or_(','.join(queried_studios))
    if style:
        count_query = count_query.ilike('style', f'%{style}%')
    if date:
        count_query = count_query.eq('date', date)
    if start_time:
        count_query = count_query.gte('start_time', start_time)
    if end_time:
        count_query = count_query.lte('end_time', end_time)
    if difficulty:
        count_query = count_query.ilike('difficulty', f'%{difficulty}%')
    if cancelled:
        count_query = count_query.eq('cancelled', cancelled)
    
    count_response = count_query.execute()
    total_count = count_response.count if count_response.count else 0
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0
    
    pagination_start = (page - 1) * limit
    pagination_end = pagination_start + limit - 1
    query = query.range(pagination_start, pagination_end)

    query.order('start_time')
    
    response = query.execute()
    return {
        'data': response.data,
        'page': page,
        'total_pages': total_pages,
        'total_count': total_count,
        'limit': limit
    }

async def create_dance_classes(dance_class_data: list[DanceClass]) -> list:
    json_data = [dance_class.model_dump(mode='json') for dance_class in dance_class_data]
    response = supabase.table('danceclasses').insert(json_data).execute()
    return response.data

async def delete_all_dance_classes():
    # we have a stored procedure in supabase that truncates the table
    response = supabase.rpc('truncate_table', {'table_name': 'danceclasses'}).execute()
    return response.data