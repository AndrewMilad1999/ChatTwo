// إعداد الإشعارات
function setupNotifications() {
    // التحقق من دعم الإشعارات
    if (!("Notification" in window)) {
        console.log("هذا المتصفح لا يدعم الإشعارات");
        return;
    }

    // طلب إذن الإشعارات
    if (Notification.permission !== "granted" && Notification.permission !== "denied") {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                console.log("تم منح إذن الإشعارات");
            }
        });
    }
}

// عرض إشعار
function showNotification(title, body) {
    // التحقق من دعم الإشعارات وإذن المستخدم
    if (!("Notification" in window) || Notification.permission !== "granted") {
        // عرض إشعار داخل التطبيق إذا لم يتم منح الإذن
        showInAppNotification(title, body);
        return;
    }

    // إنشاء إشعار
    const notification = new Notification(title, {
        body: body,
        icon: '/static/images/notification-icon.png'
    });

    // إغلاق الإشعار بعد 5 ثوانٍ
    setTimeout(() => {
        notification.close();
    }, 5000);

    // إضافة حدث النقر
    notification.onclick = function() {
        window.focus();
        this.close();
    };
}

// عرض إشعار داخل التطبيق
function showInAppNotification(title, body) {
    // إنشاء عنصر الإشعار
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        <strong>${title}</strong>
        <p>${body}</p>
    `;

    // إضافة الإشعار إلى الصفحة
    document.body.appendChild(notification);

    // عرض الإشعار
    setTimeout(() => {
        notification.style.display = 'block';
        notification.style.opacity = '1';
    }, 100);

    // إخفاء الإشعار بعد 5 ثوانٍ
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// تشغيل صوت الإشعار
function playNotificationSound() {
    const audio = new Audio('/static/sounds/notification.mp3');
    audio.play();
}

// استدعاء دالة إعداد الإشعارات عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    setupNotifications();
});
