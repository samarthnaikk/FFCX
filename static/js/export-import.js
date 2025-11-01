// Export/Import functionality
const exportImportMethods = {
    // Export functionality
    async exportTimetable() {
        this.loadingExport = true;
        
        try {
            const response = await fetch('/api/export-timetable', {
                method: 'POST'
            });

            const result = await response.json();
            
            if (result.success) {
                this.generatedCode = result.code;
                this.showExportModal = true;
            } else {
                alert('Error exporting timetable: ' + result.message);
            }
        } catch (error) {
            console.error('Error exporting timetable:', error);
            alert('Error exporting timetable');
        } finally {
            this.loadingExport = false;
        }
    },

    closeExportModal() {
        this.showExportModal = false;
        this.generatedCode = '';
        this.copyStatus = 'Copy to clipboard';
        this.copyIcon = 'fas fa-copy';
    },

    async copyCode() {
        if (!this.generatedCode) {
            return;
        }

        try {
            await navigator.clipboard.writeText(this.generatedCode);
            this.copyStatus = 'Copied!';
            this.copyIcon = 'fas fa-check text-success';
            
            setTimeout(() => {
                this.copyStatus = 'Copy to clipboard';
                this.copyIcon = 'fas fa-copy';
            }, 2000);
        } catch (error) {
            // Fallback for browsers that don't support clipboard API
            const textArea = document.createElement('textarea');
            textArea.value = this.generatedCode;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            this.copyStatus = 'Copied!';
            this.copyIcon = 'fas fa-check text-success';
            
            setTimeout(() => {
                this.copyStatus = 'Copy to clipboard';
                this.copyIcon = 'fas fa-copy';
            }, 2000);
        }
    },

    // Import functionality
    showImportModal() {
        this.showImportModalFlag = true;
        this.importCode = '';
    },

    closeImportModal() {
        this.showImportModalFlag = false;
        this.importCode = '';
    },

    async importTimetable() {
        if (!this.importCode.trim()) {
            alert('Please enter a timetable code');
            return;
        }

        this.loadingImport = true;
        
        try {
            const response = await fetch('/api/import-timetable', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code: this.importCode })
            });

            const result = await response.json();
            
            if (result.success) {
                // Refresh timetable and courses
                await this.fetchTimetable();
                await this.fetchCourses();
                this.importCode = '';
                alert(result.message);
            } else {
                alert('Error importing timetable: ' + result.message);
            }
        } catch (error) {
            console.error('Error importing timetable:', error);
            alert('Error importing timetable');
        } finally {
            this.loadingImport = false;
        }
    },

    // Utility methods for export/import
    validateImportCode(code) {
        try {
            const parsed = JSON.parse(code);
            return parsed && typeof parsed === 'object';
        } catch (error) {
            return false;
        }
    },

    formatExportCode(code) {
        try {
            const parsed = JSON.parse(code);
            return JSON.stringify(parsed, null, 2);
        } catch (error) {
            return code;
        }
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = exportImportMethods;
} else if (typeof window !== 'undefined') {
    window.exportImportMethods = exportImportMethods;
}