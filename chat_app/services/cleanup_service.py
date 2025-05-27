from src.services.auth_service import supabase
from datetime import datetime, timedelta

def cleanup_inactive_users():
    """
    حذف بيانات المستخدمين غير النشطين لأكثر من ساعة
    """
    # حساب الوقت قبل ساعة واحدة
    one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
    
    # الحصول على المستخدمين غير النشطين
    inactive_users = supabase.table('users').select('id').lt('last_activity', one_hour_ago).execute()
    
    if not inactive_users.data or len(inactive_users.data) == 0:
        return []
    
    deleted_users = []
    
    for user in inactive_users.data:
        user_id = user['id']
        
        # حذف رسائل المستخدم المباشرة
        supabase.table('direct_messages').delete().or_(
            f'sender_id.eq.{user_id},receiver_id.eq.{user_id}'
        ).execute()
        
        # حذف رسائل المستخدم في المجموعات
        supabase.table('group_messages').delete().eq('user_id', user_id).execute()
        
        # حذف عضوية المستخدم في المجموعات
        supabase.table('user_groups').delete().eq('user_id', user_id).execute()
        
        # حذف المستخدم نفسه
        supabase.table('users').delete().eq('id', user_id).execute()
        
        deleted_users.append(user_id)
    
    return deleted_users
