from models.models import DanceClass
from supabasedb.supabase import db

# table is called danceclasses
supabase = db()

async def get_all_dance_classes() -> list:
    response = supabase.table('danceclasses').select('*').execute()
    return response.data

async def create_dance_classes(dance_class_data: list[DanceClass]) -> list:
    json_data = [dance_class.model_dump(mode='json') for dance_class in dance_class_data]
    response = supabase.table('danceclasses').insert(json_data).execute()
    return response.data

async def delete_all_dance_classes():
    # we have a stored procedure in supabase that truncates the table
    response = supabase.rpc('truncate_table', {'table_name': 'danceclasses'}).execute()
    return response.data

async def get_dance_classes_by_studio(studio: str) -> list:
    if studio.lower() == 'ilovedance':
        return supabase.table('danceclasses').select('*').ilike('studio', '%ilovedance%').execute().data
    response = supabase.table('danceclasses').select('*').ilike('studio', studio).execute()
    return response.data