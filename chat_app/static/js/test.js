// سكريبت اختبار التطبيق
document.addEventListener('DOMContentLoaded', function() {
    // تسجيل بداية الاختبار
    console.log('بدء اختبار التطبيق...');
    
    // اختبار الاتصال بالخادم
    testServerConnection();
    
    // اختبار Socket.IO
    testSocketConnection();
    
    // اختبار واجهة المستخدم
    testUserInterface();
    
    // اختبار التوافق مع الأجهزة المحمولة
    testMobileResponsiveness();
});

// اختبار الاتصال بالخادم
function testServerConnection() {
    console.log('اختبار الاتصال بالخادم...');
    
    fetch('/api/health-check')
        .then(response => {
            if (response.ok) {
                console.log('✅ الاتصال بالخادم ناجح');
            } else {
                console.error('❌ فشل الاتصال بالخادم');
            }
        })
        .catch(error => {
            console.error('❌ فشل الاتصال بالخادم:', error);
        });
}

// اختبار اتصال Socket.IO
function testSocketConnection() {
    console.log('اختبار اتصال Socket.IO...');
    
    const socket = io();
    
    socket.on('connect', function() {
        console.log('✅ اتصال Socket.IO ناجح');
    });
    
    socket.on('connect_error', function(error) {
        console.error('❌ فشل اتصال Socket.IO:', error);
    });
}

// اختبار واجهة المستخدم
function testUserInterface() {
    console.log('اختبار واجهة المستخدم...');
    
    // التحقق من وجود العناصر الرئيسية
    const elements = [
        { selector: '.sidebar', name: 'الشريط الجانبي' },
        { selector: '.user-list', name: 'قائمة المستخدمين' },
        { selector: '.chat-container', name: 'حاوية الدردشة' },
        { selector: '.ad-container', name: 'حاوية الإعلانات' }
    ];
    
    elements.forEach(element => {
        if (document.querySelector(element.selector)) {
            console.log(`✅ تم العثور على ${element.name}`);
        } else {
            console.error(`❌ لم يتم العثور على ${element.name}`);
        }
    });
}

// اختبار التوافق مع الأجهزة المحمولة
function testMobileResponsiveness() {
    console.log('اختبار التوافق مع الأجهزة المحمولة...');
    
    const width = window.innerWidth;
    
    if (width < 768) {
        console.log('جاري الاختبار على جهاز محمول...');
        
        // التحقق من وجود زر التبديل للشريط الجانبي
        if (document.querySelector('.toggle-sidebar')) {
            console.log('✅ زر التبديل للشريط الجانبي موجود');
        } else {
            console.error('❌ زر التبديل للشريط الجانبي غير موجود');
        }
    } else {
        console.log('جاري الاختبار على جهاز سطح المكتب...');
    }
}

// اختبار الإشعارات
function testNotifications() {
    console.log('اختبار الإشعارات...');
    
    if ("Notification" in window) {
        console.log('✅ المتصفح يدعم الإشعارات');
        
        if (Notification.permission === "granted") {
            console.log('✅ تم منح إذن الإشعارات');
        } else {
            console.warn('⚠️ لم يتم منح إذن الإشعارات');
        }
    } else {
        console.error('❌ المتصفح لا يدعم الإشعارات');
    }
}

// اختبار الأداء
function testPerformance() {
    console.log('اختبار الأداء...');
    
    const startTime = performance.now();
    
    // محاكاة تحميل البيانات
    setTimeout(() => {
        const endTime = performance.now();
        const loadTime = endTime - startTime;
        
        console.log(`⏱️ وقت التحميل: ${loadTime.toFixed(2)} مللي ثانية`);
        
        if (loadTime < 1000) {
            console.log('✅ الأداء جيد');
        } else {
            console.warn('⚠️ الأداء بطيء');
        }
    }, 500);
}
