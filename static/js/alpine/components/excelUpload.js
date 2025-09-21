document.addEventListener('alpine:init', () => {
    Alpine.data('excelUpload', () => ({
        isDragging: false,
        fileName: '',
        fileSize: '',
        uploading: false,
        file: null,
        error: '',

        handleDrop(event) {
            this.isDragging = false;
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                this.processFile(files[0]);
            }
        },

        handleFileSelect(event) {
            const files = event.target.files;
            if (files.length > 0) {
                this.processFile(files[0]);
            }
        },

        processFile(file) {
            // Check file extension
            const validExtensions = ['.xls', '.xlsx'];
            const fileName = file.name.toLowerCase();
            const hasValidExtension = validExtensions.some(ext => fileName.endsWith(ext));

            if (!hasValidExtension) {
                this.error = 'Please select an Excel file (.xls or .xlsx)';
                this.resetForm();
                return;
            }

            // Check file size (5MB max)
            const maxSize = 5 * 1024 * 1024; // 5MB in bytes
            if (file.size > maxSize) {
                const actualSize = this.formatFileSize(file.size);
                this.error = `File exceeds 5MB limit (your file: ${actualSize})`;
                this.resetForm();
                return;
            }

            // Clear any previous errors
            this.error = '';

            // Set file info for display
            this.file = file;
            this.fileName = file.name;
            this.fileSize = this.formatFileSize(file.size);

            // Update the actual file input
            const fileInput = this.$refs.fileInput;
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
        },

        formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },

        resetForm() {
            this.fileName = '';
            this.fileSize = '';
            this.uploading = false;
            this.file = null;
            this.isDragging = false;
            // Keep error message visible after reset
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = '';
            }
        },

        clearError() {
            this.error = '';
        },

        init() {
            // Set up form submission handling
            const form = document.getElementById('excel-upload-form');
            if (form) {
                form.addEventListener('htmx:beforeRequest', () => {
                    this.uploading = true;
                });

                form.addEventListener('htmx:afterRequest', (event) => {
                    if (event.detail.successful) {
                        this.resetForm();
                        this.error = '';
                    }
                    this.uploading = false;
                });

                // Listen for the reset event
                document.addEventListener('excel-uploaded', () => {
                    this.resetForm();
                    this.error = '';
                });
            }
        }
    }));
});