from flask import Blueprint, jsonify, request, session, render_template
from src.services.group_service import create_group, join_group, get_group_messages, send_group_message, get_user_groups
from flask_socketio import emit
from src.main import socketio

groups_bp = Blueprint('groups', __name__, url_prefix='/groups')

@groups_bp.route('/create', methods=['POST'])
def create_new_group():
    """
    إنشاء مجموعة دردشة جديدة
    """
    if 'user_id' not in session:
        return jsonify({'error': 'غير مصرح'}), 401
    
    data = request.json
    group_name = data.get('name')
    
    if not group_name:
        return jsonify({'error': 'اسم المجموعة مطلوب'}), 400
    
    creator_id = session['user_id']
    
    # إنشاء المجموعة
    group = create_group(group_name, creator_id)
    
    if group:
        return jsonify(group)
    
    return jsonify({'error': 'فشل في إنشاء المجموعة'}), 500

@groups_bp.route('/join/<int:group_id>', methods=['POST'])
def join_existing_group(group_id):
    """
    الانضمام إلى مجموعة موجودة
    """
    if 'user_id' not in session:
        return jsonify({'error': 'غير مصرح'}), 401
    
    user_id = session['user_id']
    
    # الانضمام إلى المجموعة
    result = join_group(user_id, group_id)
    
    if result:
        # إرسال إشعار في الوقت الفعلي
        socketio.emit(f'group_{group_id}_user_joined', {
            'user_id': user_id,
            'username': session.get('username')
        })
        return jsonify({'success': True})
    
    return jsonify({'error': 'فشل في الانضمام إلى المجموعة'}), 500

@groups_bp.route('/<int:group_id>/messages', methods=['GET'])
def get_messages(group_id):
    """
    الحصول على رسائل المجموعة
    """
    if 'user_id' not in session:
        return jsonify({'error': 'غير مصرح'}), 401
    
    messages = get_group_messages(group_id)
    return jsonify(messages)

@groups_bp.route('/<int:group_id>/messages', methods=['POST'])
def send_message(group_id):
    """
    إرسال رسالة إلى المجموعة
    """
    if 'user_id' not in session:
        return jsonify({'error': 'غير مصرح'}), 401
    
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'محتوى الرسالة مطلوب'}), 400
    
    sender_id = session['user_id']
    
    # إرسال الرسالة
    message = send_group_message(sender_id, group_id, content)
    
    if message:
        # إرسال إشعار في الوقت الفعلي
        socketio.emit(f'group_{group_id}_new_message', message)
        return jsonify(message)
    
    return jsonify({'error': 'فشل في إرسال الرسالة'}), 500

@groups_bp.route('/user', methods=['GET'])
def get_my_groups():
    """
    الحصول على المجموعات التي ينتمي إليها المستخدم
    """
    if 'user_id' not in session:
        return jsonify({'error': 'غير مصرح'}), 401
    
    user_id = session['user_id']
    
    groups = get_user_groups(user_id)
    return jsonify(groups)

@groups_bp.route('/<int:group_id>', methods=['GET'])
def group_chat(group_id):
    """
    عرض صفحة الدردشة الجماعية
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('chat/group.html', group_id=group_id)
