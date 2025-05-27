from flask import Blueprint, jsonify, session
from src.services.auth_service import get_user_by_id
from src.services.user_service import get_active_users

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/active', methods=['GET'])
def active_users():
    """
    الحصول على قائمة المستخدمين النشطين
    """
    if 'user_id' not in session:
        return jsonify({'error': 'غير مصرح'}), 401
    
    users = get_active_users()
    return jsonify(users)

@users_bp.route('/profile/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    """
    الحصول على معلومات المستخدم
    """
    if 'user_id' not in session:
        return jsonify({'error': 'غير مصرح'}), 401
    
    user = get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'المستخدم غير موجود'}), 404
    
    # إزالة المعلومات الحساسة قبل إرسالها
    user_data = {
        'id': user['id'],
        'username': user['username'],
        'created_at': user['created_at']
    }
    
    return jsonify(user_data)
