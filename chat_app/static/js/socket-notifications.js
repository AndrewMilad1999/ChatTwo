// دمج الإشعارات مع Socket.IO
document.addEventListener('DOMContentLoaded', function() {
    // إعداد Socket.IO
    const socket = io();
    
    // إعداد الإشعارات
    setupNotifications();
    
    // الاستماع لأحداث الرسائل الجديدة
    const userId = document.getElementById('currentUserId')?.value || '';
    
    if (userId) {
        // الاستماع للرسائل المباشرة الجديدة
        socket.on(`new_message_${userId}`, function(message) {
            // التحقق مما إذا كانت المحادثة الحالية ليست مع مرسل الرسالة
            const currentChatUserId = document.getElementById('currentChatUserId')?.value || '';
            
            if (currentChatUserId !== message.sender_id.toString()) {
                // الحصول على اسم المرسل
                fetch(`/users/profile/${message.sender_id}`)
                    .then(response => response.json())
                    .then(user => {
                        // عرض إشعار
                        showNotification(
                            `رسالة جديدة من ${user.username}`,
                            message.content
                        );
                        
                        // تشغيل صوت الإشعار
                        playNotificationSound();
                        
                        // تحديث عدد الرسائل غير المقروءة
                        updateUnreadCount(message.sender_id);
                    })
                    .catch(error => console.error('Error fetching user:', error));
            }
        });
        
        // الاستماع لرسائل المجموعة الجديدة
        socket.on('group_message', function(data) {
            // التحقق مما إذا كانت المجموعة الحالية ليست هي المجموعة التي تم إرسال الرسالة إليها
            const currentGroupId = document.getElementById('currentGroupId')?.value || '';
            
            if (currentGroupId !== data.group_id.toString() && data.sender_id.toString() !== userId) {
                // عرض إشعار
                showNotification(
                    `رسالة جديدة في مجموعة ${data.group_name}`,
                    `${data.sender_name}: ${data.content}`
                );
                
                // تشغيل صوت الإشعار
                playNotificationSound();
                
                // تحديث عدد الرسائل غير المقروءة للمجموعة
                updateGroupUnreadCount(data.group_id);
            }
        });
    }
});

// تحديث عدد الرسائل غير المقروءة للمستخدم
function updateUnreadCount(senderId) {
    const userItem = document.querySelector(`.user-item[data-user-id="${senderId}"]`);
    
    if (userItem) {
        let badge = userItem.querySelector('.unread-badge');
        
        if (!badge) {
            badge = document.createElement('div');
            badge.className = 'unread-badge';
            userItem.appendChild(badge);
            badge.textContent = '1';
        } else {
            const count = parseInt(badge.textContent) + 1;
            badge.textContent = count.toString();
        }
    }
}

// تحديث عدد الرسائل غير المقروءة للمجموعة
function updateGroupUnreadCount(groupId) {
    const groupItem = document.querySelector(`.user-item[data-group-id="${groupId}"]`);
    
    if (groupItem) {
        let badge = groupItem.querySelector('.unread-badge');
        
        if (!badge) {
            badge = document.createElement('div');
            badge.className = 'unread-badge';
            groupItem.appendChild(badge);
            badge.textContent = '1';
        } else {
            const count = parseInt(badge.textContent) + 1;
            badge.textContent = count.toString();
        }
    }
}

// إعادة تعيين عدد الرسائل غير المقروءة عند فتح محادثة
function resetUnreadCount(id, type) {
    const selector = type === 'user' 
        ? `.user-item[data-user-id="${id}"]` 
        : `.user-item[data-group-id="${id}"]`;
    
    const item = document.querySelector(selector);
    
    if (item) {
        const badge = item.querySelector('.unread-badge');
        
        if (badge) {
            item.removeChild(badge);
        }
    }
}
