from supabase import create_client
import os
from datetime import datetime

# تهيئة اتصال Supabase
# ملاحظة: في بيئة الإنتاج، يجب وضع هذه المفاتيح في متغيرات بيئية
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_KEY = "your-supabase-key"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_user(username):
    """
    تسجيل مستخدم جديد أو إرجاع المستخدم الموجود
    """
    # التحقق من وجود المستخدم
    response = supabase.table('users').select('*').eq('username', username).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    
    # إنشاء مستخدم جديد
    current_time = datetime.now().isoformat()
    new_user = {
        'username': username,
        'last_activity': current_time,
        'created_at': current_time
    }
    
    response = supabase.table('users').insert(new_user).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    
    return None

def login_user(username):
    """
    تسجيل دخول المستخدم أو إنشاء حساب جديد
    """
    user = register_user(username)
    
    if user:
        # تحديث وقت آخر نشاط
        update_last_activity(user['id'])
    
    return user

def update_last_activity(user_id):
    """
    تحديث وقت آخر نشاط للمستخدم
    """
    current_time = datetime.now().isoformat()
    
    supabase.table('users').update({
        'last_activity': current_time
    }).eq('id', user_id).execute()

def get_user_by_id(user_id):
    """
    الحصول على معلومات المستخدم بواسطة المعرف
    """
    response = supabase.table('users').select('*').eq('id', user_id).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    
    return None
