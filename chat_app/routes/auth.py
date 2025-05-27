from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.services.auth_service import register_user, login_user, update_last_activity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        
        if not username:
            flash('يرجى إدخال اسم المستخدم')
            return redirect(url_for('auth.login'))
        
        # تسجيل الدخول أو إنشاء مستخدم جديد
        user = login_user(username)
        
        if user:
            session['username'] = username
            session['user_id'] = user['id']
            update_last_activity(user['id'])
            return redirect(url_for('index'))
        
        flash('حدث خطأ أثناء تسجيل الدخول')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

@auth_bp.before_request
def update_activity():
    if 'user_id' in session:
        update_last_activity(session['user_id'])
