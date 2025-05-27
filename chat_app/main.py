import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO
from flask_session import Session
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# تهيئة جلسات Flask
Session(app)

# تهيئة SocketIO للاتصال في الوقت الفعلي
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)

# تهيئة المجدول لحذف البيانات تلقائياً
scheduler = BackgroundScheduler()

# استيراد المسارات
from src.routes.auth import auth_bp
from src.routes.users import users_bp
from src.routes.messages import messages_bp
from src.routes.groups import groups_bp

# تسجيل المسارات
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(groups_bp)

# الصفحة الرئيسية
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('chat/index.html')

# تشغيل المجدول لحذف البيانات تلقائياً
@app.before_first_request
def initialize():
    from src.services.cleanup_service import cleanup_inactive_users
    scheduler.add_job(cleanup_inactive_users, 'interval', minutes=15)
    scheduler.start()

# إيقاف المجدول عند إيقاف التطبيق
@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    if scheduler.running:
        scheduler.shutdown()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
