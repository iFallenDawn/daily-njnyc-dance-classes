import os
from supabase import create_client, Client

def db() -> Client:
    url = os.environ.get("SUPABASE_URL") or ''
    key = os.environ.get("SUPABASE_KEY") or ''
    return create_client(url, key)