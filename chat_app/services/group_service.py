from src.services.auth_service import supabase
from datetime import datetime

def create_group(name, creator_id):
    """
    إنشاء مجموعة دردشة جديدة
    """
    current_time = datetime.now().isoformat()
    
    group = {
        'name': name,
        'creator_id': creator_id,
        'created_at': current_time
    }
    
    # إنشاء المجموعة
    response = supabase.table('groups').insert(group).execute()
    
    if response.data and len(response.data) > 0:
        group_id = response.data[0]['id']
        
        # إضافة المنشئ كعضو في المجموعة
        join_group(creator_id, group_id)
        
        return response.data[0]
    
    return None

def join_group(user_id, group_id):
    """
    انضمام مستخدم إلى مجموعة
    """
    current_time = datetime.now().isoformat()
    
    user_group = {
        'user_id': user_id,
        'group_id': group_id,
        'joined_at': current_time
    }
    
    # التحقق من عدم وجود المستخدم في المجموعة مسبقاً
    check = supabase.table('user_groups').select('*').eq('user_id', user_id).eq('group_id', group_id).execute()
    
    if check.data and len(check.data) > 0:
        return check.data[0]
    
    # إضافة المستخدم إلى المجموعة
    response = supabase.table('user_groups').insert(user_group).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    
    return None

def get_group_messages(group_id):
    """
    الحصول على رسائل المجموعة
    """
    response = supabase.table('group_messages').select(
        'id, content, sent_at, group_messages.user_id, users.username'
    ).eq('group_id', group_id).join(
        'users', 'group_messages.user_id', 'users.id'
    ).order('sent_at').execute()
    
    if response.data:
        return response.data
    
    return []

def send_group_message(user_id, group_id, content):
    """
    إرسال رسالة إلى المجموعة
    """
    current_time = datetime.now().isoformat()
    
    message = {
        'user_id': user_id,
        'group_id': group_id,
        'content': content,
        'sent_at': current_time
    }
    
    response = supabase.table('group_messages').insert(message).execute()
    
    if response.data and len(response.data) > 0:
        # إضافة اسم المستخدم للرسالة المرسلة
        user = supabase.table('users').select('username').eq('id', user_id).execute()
        
        if user.data and len(user.data) > 0:
            response.data[0]['username'] = user.data[0]['username']
        
        return response.data[0]
    
    return None

def get_user_groups(user_id):
    """
    الحصول على المجموعات التي ينتمي إليها المستخدم
    """
    response = supabase.table('user_groups').select(
        'groups.id, groups.name, groups.created_at'
    ).eq('user_id', user_id).join(
        'groups', 'user_groups.group_id', 'groups.id'
    ).execute()
    
    if response.data:
        return response.data
    
    return []
