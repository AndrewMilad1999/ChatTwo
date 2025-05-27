// إعداد مواقع الإعلانات
document.addEventListener('DOMContentLoaded', function() {
    // تهيئة جميع مواقع الإعلانات
    initializeAdSlots();
});

// تهيئة مواقع الإعلانات
function initializeAdSlots() {
    // تحديد جميع مواقع الإعلانات
    const adContainers = document.querySelectorAll('.ad-container');
    
    // إضافة معرف فريد لكل موقع إعلاني
    adContainers.forEach((container, index) => {
        container.id = `ad-container-${index}`;
        
        // إضافة تعليق توضيحي للمستخدم
        const adPlaceholder = document.createElement('div');
        adPlaceholder.className = 'ad-placeholder';
        adPlaceholder.innerHTML = `
            <p class="mb-0">مساحة إعلانية</p>
            <small class="text-muted">يمكنك إضافة كود AdSense هنا</small>
        `;
        
        // إضافة نموذج للإعلان
        container.innerHTML = '';
        container.appendChild(adPlaceholder);
    });
}

// دالة لإضافة كود AdSense
function insertAdSenseCode(containerId, adSlotId) {
    const container = document.getElementById(containerId);
    
    if (container) {
        // نموذج لكود AdSense
        // يمكن للمستخدم استبدال هذا بكود AdSense الخاص به
        container.innerHTML = `
            <!-- نموذج لكود AdSense -->
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
                 data-ad-slot="${adSlotId}"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                (adsbygoogle = window.adsbygoogle || []).push({});
            </script>
        `;
    }
}

// دالة لتحديث حجم الإعلانات عند تغيير حجم النافذة
window.addEventListener('resize', function() {
    // يمكن إضافة منطق لتعديل حجم الإعلانات هنا
    // على سبيل المثال، إخفاء بعض الإعلانات في الشاشات الصغيرة
    const adContainers = document.querySelectorAll('.ad-container');
    
    adContainers.forEach(container => {
        if (window.innerWidth < 768) {
            // إخفاء بعض الإعلانات في الشاشات الصغيرة
            if (container.classList.contains('sidebar-ad')) {
                container.style.display = 'none';
            }
        } else {
            // إظهار جميع الإعلانات في الشاشات الكبيرة
            container.style.display = 'block';
        }
    });
});
