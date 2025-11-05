/**
 * Notifications System
 */

class NotificationManager {
    constructor() {
        this.container = this.createContainer();
        this.notifications = [];
    }
    
    createContainer() {
        let container = document.getElementById('notification-container');
        
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.style.cssText = `
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 10000;
                max-width: 400px;
            `;
            document.body.appendChild(container);
        }
        
        return container;
    }
    
    show(message, type = 'info', duration = 5000) {
        const notification = this.createNotification(message, type);
        this.container.appendChild(notification);
        this.notifications.push(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        }, 10);
        
        // Auto remove
        if (duration > 0) {
            setTimeout(() => {
                this.remove(notification);
            }, duration);
        }
        
        return notification;
    }
    
    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            padding: 16px;
            margin-bottom: 12px;
            background: white;
            border: 1px solid var(--gray-200);
            border-left: 4px solid ${this.getColor(type)};
            border-radius: 8px;
            box-shadow: var(--shadow-lg);
            transform: translateX(400px);
            opacity: 0;
            transition: all 0.3s ease-out;
            display: flex;
            align-items: center;
            gap: 12px;
        `;
        
        const icon = this.getIcon(type);
        const closeBtn = this.createCloseButton();
        
        notification.innerHTML = `
            <div style="flex-shrink: 0; color: ${this.getColor(type)};">
                ${icon}
            </div>
            <div style="flex: 1; font-size: 14px; color: var(--gray-700);">
                ${message}
            </div>
        `;
        
        notification.appendChild(closeBtn);
        
        closeBtn.addEventListener('click', () => {
            this.remove(notification);
        });
        
        return notification;
    }
    
    createCloseButton() {
        const btn = document.createElement('button');
        btn.innerHTML = `
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
        `;
        btn.style.cssText = `
            flex-shrink: 0;
            background: none;
            border: none;
            color: var(--gray-400);
            cursor: pointer;
            padding: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            transition: all 0.2s;
        `;
        
        btn.addEventListener('mouseenter', () => {
            btn.style.background = 'var(--gray-100)';
            btn.style.color = 'var(--gray-600)';
        });
        
        btn.addEventListener('mouseleave', () => {
            btn.style.background = 'none';
            btn.style.color = 'var(--gray-400)';
        });
        
        return btn;
    }
    
    remove(notification) {
        notification.style.transform = 'translateX(400px)';
        notification.style.opacity = '0';
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
            
            const index = this.notifications.indexOf(notification);
            if (index > -1) {
                this.notifications.splice(index, 1);
            }
        }, 300);
    }
    
    getIcon(type) {
        const icons = {
            success: '<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
            error: '<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
            warning: '<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>',
            info: '<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
        };
        return icons[type] || icons.info;
    }
    
    getColor(type) {
        const colors = {
            success: '#22c55e',
            error: '#ef4444',
            warning: '#eab308',
            info: '#3b82f6'
        };
        return colors[type] || colors.info;
    }
    
    success(message, duration) {
        return this.show(message, 'success', duration);
    }
    
    error(message, duration) {
        return this.show(message, 'error', duration);
    }
    
    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }
    
    info(message, duration) {
        return this.show(message, 'info', duration);
    }
}

// Create global instance
window.notify = new NotificationManager();

// Example usage:
// notify.success('Book added to cart!');
// notify.error('Failed to load books');
// notify.warning('Your subscription expires soon');
// notify.info('New books available');