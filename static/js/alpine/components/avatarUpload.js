/**
 * Alpine.js Avatar Upload Component
 * Handles avatar upload with drag-and-drop, preview, and file validation
 */
document.addEventListener('alpine:init', () => {
    Alpine.data('avatarUpload', (hasCurrentAvatar = false) => ({
        isDragging: false,
        fileName: '',
        previewUrl: null,
        uploading: false,
        hasCurrentAvatar: hasCurrentAvatar,

        handleDrop(event) {
            this.isDragging = false;
            const file = event.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {
                this.setFile(file);
            }
        },

        setFile(file) {
            // Update the hidden file input
            const fileInput = this.$refs.fileInput;
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;

            // Set file name
            this.fileName = file.name;

            // Generate preview
            const reader = new FileReader();
            reader.onload = (e) => {
                this.previewUrl = e.target.result;
            };
            reader.readAsDataURL(file);
        },

        clearSelection() {
            this.$refs.fileInput.value = '';
            this.fileName = '';
            this.previewUrl = null;
        },

        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                this.setFile(file);
            }
        },

        init() {
            // Reset state when component initializes
            this.uploading = false;
            this.fileName = '';
            this.previewUrl = null;
        }
    }));
});