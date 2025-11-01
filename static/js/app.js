// Main Vue.js Application
// This file combines all modular components into a single Vue application

const { createApp } = Vue;

const VueApp = createApp({
    data() {
        return {
            ...vueData,
            // Additional app-level data can be added here
        };
    },
    
    computed: {
        ...vueComputed,
        // Additional computed properties can be added here
    },
    
    methods: {
        ...vueMethods,
        ...dragDropMethods,
        ...exportImportMethods,
        ...darkModeMethods,
        
        // App initialization
        async initializeApp() {
            console.log('Initializing FFCX Timetable Application...');
            
            // Initialize dark mode
            this.initializeDarkMode();
            
            // Load initial data
            await this.fetchTimetable();
            await this.fetchCourses();
            
            // Initialize preferences
            this.initializePreferences();
            
            console.log('Application initialized successfully');
        },
        
        // Lifecycle hooks
        onMounted() {
            this.initializeApp();
            
            // Add keyboard shortcuts
            this.setupKeyboardShortcuts();
            
            // Setup global event listeners
            this.setupGlobalEventListeners();
        },
        
        // Keyboard shortcuts
        setupKeyboardShortcuts() {
            document.addEventListener('keydown', (e) => {
                // Ctrl/Cmd + D for dark mode toggle
                if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                    e.preventDefault();
                    this.toggleDarkMode();
                }
                
                // Ctrl/Cmd + E for export
                if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
                    e.preventDefault();
                    this.exportTimetable();
                }
                
                // Ctrl/Cmd + I for import
                if ((e.ctrlKey || e.metaKey) && e.key === 'i') {
                    e.preventDefault();
                    this.showImportModal();
                }
                
                // Ctrl/Cmd + P for preferences
                if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
                    e.preventDefault();
                    this.showPreferencesModal();
                }
                
                // Escape to close modals
                if (e.key === 'Escape') {
                    this.closeAllModals();
                }
            });
        },
        
        // Global event listeners
        setupGlobalEventListeners() {
            // Handle window resize
            window.addEventListener('resize', this.handleWindowResize);
            
            // Handle page visibility changes
            document.addEventListener('visibilitychange', this.handleVisibilityChange);
            
            // Handle online/offline status
            window.addEventListener('online', this.handleOnlineStatus);
            window.addEventListener('offline', this.handleOfflineStatus);
        },
        
        // Event handlers
        handleWindowResize() {
            // Recalculate layout if needed
            this.checkMobileLayout();
        },
        
        handleVisibilityChange() {
            if (document.visibilityState === 'visible') {
                // Page became visible, refresh data if needed
                this.refreshDataIfStale();
            }
        },
        
        handleOnlineStatus() {
            console.log('Application is online');
            this.isOnline = true;
        },
        
        handleOfflineStatus() {
            console.log('Application is offline');
            this.isOnline = false;
        },
        
        // Utility methods
        closeAllModals() {
            this.showExportModal = false;
            this.showImportModalFlag = false;
            this.showPreferences = false;
            this.showDropdown = false;
            this.showPreferenceCourseDropdown = false;
        },
        
        checkMobileLayout() {
            this.isMobile = window.innerWidth < 768;
        },
        
        async refreshDataIfStale() {
            const lastUpdate = localStorage.getItem('lastDataUpdate');
            const now = Date.now();
            const fiveMinutes = 5 * 60 * 1000;
            
            if (!lastUpdate || (now - parseInt(lastUpdate)) > fiveMinutes) {
                await this.fetchTimetable();
                await this.fetchCourses();
                localStorage.setItem('lastDataUpdate', now.toString());
            }
        },
        
        // Error handling
        handleError(error, context = '') {
            console.error(`Error in ${context}:`, error);
            
            // Show user-friendly error message
            const errorMessage = this.getErrorMessage(error);
            this.showErrorNotification(errorMessage);
        },
        
        getErrorMessage(error) {
            if (error.message) {
                return error.message;
            } else if (typeof error === 'string') {
                return error;
            } else {
                return 'An unexpected error occurred. Please try again.';
            }
        },
        
        showErrorNotification(message) {
            // Create a simple notification
            const notification = document.createElement('div');
            notification.className = 'error-notification';
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--danger-color, #dc3545);
                color: white;
                padding: 12px 16px;
                border-radius: 4px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                z-index: 10000;
                max-width: 300px;
            `;
            
            document.body.appendChild(notification);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 5000);
        },
        
        // Performance monitoring
        measurePerformance(label, fn) {
            const start = performance.now();
            const result = fn();
            const end = performance.now();
            console.log(`${label} took ${end - start} milliseconds`);
            return result;
        },
        
        async measureAsyncPerformance(label, fn) {
            const start = performance.now();
            const result = await fn();
            const end = performance.now();
            console.log(`${label} took ${end - start} milliseconds`);
            return result;
        }
    },
    
    // Vue lifecycle hooks
    mounted() {
        this.onMounted();
    },
    
    beforeUnmount() {
        // Cleanup event listeners
        window.removeEventListener('resize', this.handleWindowResize);
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
        window.removeEventListener('online', this.handleOnlineStatus);
        window.removeEventListener('offline', this.handleOfflineStatus);
    }
});

// Global error handler
VueApp.config.errorHandler = (err, instance, info) => {
    console.error('Vue error:', err, info);
    
    // Handle the error gracefully
    if (instance && instance.handleError) {
        instance.handleError(err, info);
    }
};

// Global warning handler (for development)
if (process.env.NODE_ENV === 'development') {
    VueApp.config.warnHandler = (msg, instance, trace) => {
        console.warn('Vue warning:', msg, trace);
    };
}

// Export the app for mounting
window.VueApp = VueApp;

// Auto-mount if in browser environment
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        VueApp.mount('#app');
    });
}