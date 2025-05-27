from flask import Blueprint, jsonify, request, session
from src.services.message_service import send_direct_message, get_direct_messages
from flask_socketio import emit
from src.main import socketio

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.route('/direct/<int:receiver_id>', methods=['POST'])
def send_message(receiver_id):
    """
    إرسال رسالة مباشرة إلى مستخدم
    """
    if 'user_id' not in session:
        return jsonify({'error': 'غير مصرح'}), 401
    
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'محتوى الرسالة مطلوب'}), 400
    
    sender_id = session['user_id']
    
    # إرسال الرسالة
    message = send_direct_message(sender_id, receiver_id, content)
    
    if message:
        # إرسال إشعار في الوقت الفعلي
        socketio.emit(f'new_message_{receiver_id}', message)
        return jsonify(message)
    
    return jsonify({'error': 'فشل في إرسال الرسالة'}), 500

@messages_bp.route('/direct/<int:user_id>', methods=['GET'])
def get_messages(user_id):
    """
    الحصول على الرسائل المباشرة بين المستخدم الحالي والمستخدم المحدد
    """
    if 'user_id' not in session:
        return jsonify({'error': 'غير مصرح'}), 401
    
    current_user_id = session['user_id']
    
    messages = get_direct_messages(current_user_id, user_id)
    return jsonify(messages)

# معالجة الأحداث في الوقت الفعلي
@socketio.on('typing')
def handle_typing(data):
    """
    إرسال إشعار عندما يكون المستخدم يكتب
    """
    if 'user_id' not in session:
        return
    
    sender_id = session['user_id']
    receiver_id = data.get('receiver_id')
    
    if receiver_id:
        emit(f'typing_{receiver_id}', {
            'sender_id': sender_id,
            'is_typing': data.get('is_typing', True)
        }, broadcast=True)

@socketio.on('read_message')
def handle_read_message(data):
    """
    تحديث حالة قراءة الرسالة
    """
    if 'user_id' not in session:
        return
    
    message_id = data.get('message_id')
    sender_id = data.get('sender_id')
    
    if message_id and sender_id:
        # تحديث حالة القراءة في قاعدة البيانات (سيتم تنفيذها لاحقاً)
        # mark_message_as_read(message_id)
        
        emit(f'message_read_{sender_id}', {
            'message_id': message_id
        }, broadcast=True)
