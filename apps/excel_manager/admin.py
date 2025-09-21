from django.conf import settings
from django.contrib import admin
from .models import ExcelUpload, ExcelData

# TODO: Update to use consistent pattern with other apps:
# if settings.DEBUG or getattr(settings, 'ADMIN_ENABLED', False):
if settings.DEBUG:

    @admin.register(ExcelUpload)
    class ExcelUploadAdmin(admin.ModelAdmin):
        list_display = [
            "original_filename",
            "user",
            "status",
            "file_size_mb",
            "sheet_count",
            "uploaded_at",
        ]
        list_filter = ["status", "uploaded_at"]
        search_fields = ["original_filename", "user__email"]
        readonly_fields = [
            "file_hash",
            "file_size",
            "uploaded_at",
            "processed_at",
        ]

        def file_size_mb(self, obj):
            return f"{obj.file_size_mb} MB"

        file_size_mb.short_description = "Size"

    @admin.register(ExcelData)
    class ExcelDataAdmin(admin.ModelAdmin):
        list_display = ["upload", "sheet_name", "sheet_index", "row_count"]
        list_filter = ["upload__uploaded_at"]
        search_fields = ["upload__original_filename", "sheet_name"]
