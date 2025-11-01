// Dark mode functionality
const darkModeMethods = {
    // Dark mode state
    isDarkMode: false,

    // Initialize dark mode from localStorage
    initializeDarkMode() {
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode !== null) {
            this.isDarkMode = savedDarkMode === 'true';
        } else {
            // Check system preference
            this.isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        }
        
        this.applyDarkMode();
        this.setupDarkModeListener();
    },

    // Apply dark mode styles
    applyDarkMode() {
        document.documentElement.setAttribute('data-theme', this.isDarkMode ? 'dark' : 'light');
        
        // Update meta theme-color for mobile browsers
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.content = this.isDarkMode ? '#1a1a1a' : '#ffffff';
        }
    },

    // Toggle dark mode
    toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
        this.applyDarkMode();
        localStorage.setItem('darkMode', this.isDarkMode);
        
        // Emit custom event for other components
        window.dispatchEvent(new CustomEvent('darkModeChanged', {
            detail: { isDarkMode: this.isDarkMode }
        }));
    },

    // Listen for system theme changes
    setupDarkModeListener() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                // Only update if user hasn't manually set preference
                const savedDarkMode = localStorage.getItem('darkMode');
                if (savedDarkMode === null) {
                    this.isDarkMode = e.matches;
                    this.applyDarkMode();
                }
            });
        }
    },

    // Get current theme
    getCurrentTheme() {
        return this.isDarkMode ? 'dark' : 'light';
    },

    // Set theme programmatically
    setTheme(theme) {
        this.isDarkMode = theme === 'dark';
        this.applyDarkMode();
        localStorage.setItem('darkMode', this.isDarkMode);
    },

    // Reset to system preference
    resetToSystemTheme() {
        localStorage.removeItem('darkMode');
        if (window.matchMedia) {
            this.isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
        } else {
            this.isDarkMode = false;
        }
        this.applyDarkMode();
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = darkModeMethods;
} else if (typeof window !== 'undefined') {
    window.darkModeMethods = darkModeMethods;
}