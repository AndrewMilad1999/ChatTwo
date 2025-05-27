from src.services.auth_service import supabase
from datetime import datetime

def send_direct_message(sender_id, receiver_id, content):
    """
    إرسال رسالة مباشرة إلى مستخدم
    """
    current_time = datetime.now().isoformat()
    
    message = {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'content': content,
        'sent_at': current_time,
        'is_read': False
    }
    
    response = supabase.table('direct_messages').insert(message).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    
    return None

def get_direct_messages(user1_id, user2_id):
    """
    الحصول على الرسائل المباشرة بين مستخدمين
    """
    # استعلام للحصول على الرسائل المرسلة من المستخدم الأول إلى الثاني
    query1 = supabase.table('direct_messages').select('*').eq('sender_id', user1_id).eq('receiver_id', user2_id)
    
    # استعلام للحصول على الرسائل المرسلة من المستخدم الثاني إلى الأول
    query2 = supabase.table('direct_messages').select('*').eq('sender_id', user2_id).eq('receiver_id', user1_id)
    
    # دمج نتائج الاستعلامين
    response1 = query1.execute()
    response2 = query2.execute()
    
    messages = []
    
    if response1.data:
        messages.extend(response1.data)
    
    if response2.data:
        messages.extend(response2.data)
    
    # ترتيب الرسائل حسب وقت الإرسال
    messages.sort(key=lambda x: x['sent_at'])
    
    return messages

def mark_message_as_read(message_id):
    """
    تحديث حالة قراءة الرسالة
    """
    response = supabase.table('direct_messages').update({
        'is_read': True
    }).eq('id', message_id).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    
    return None
