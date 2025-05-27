from src.services.auth_service import supabase
from datetime import datetime, timedelta

def get_active_users():
    """
    الحصول على قائمة المستخدمين النشطين خلال الساعة الماضية
    """
    # حساب الوقت قبل ساعة واحدة
    one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
    
    # الحصول على المستخدمين النشطين
    response = supabase.table('users').select('id, username, last_activity').gt('last_activity', one_hour_ago).execute()
    
    if response.data:
        return response.data
    
    return []

def search_users(query):
    """
    البحث عن مستخدمين بناءً على اسم المستخدم
    """
    response = supabase.table('users').select('id, username').ilike('username', f'%{query}%').execute()
    
    if response.data:
        return response.data
    
    return []
