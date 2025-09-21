import magic
from django import forms
from django.core.exceptions import ValidationError
from .models import ExcelUpload


class ExcelUploadForm(forms.ModelForm):
    """Form for Excel file upload with validation."""

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
    ALLOWED_EXTENSIONS = ["xls", "xlsx"]
    ALLOWED_MIME_TYPES = [
        "application/vnd.ms-excel",  # .xls
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    ]

    class Meta:
        model = ExcelUpload
        fields = ["file"]
        widgets = {
            "file": forms.FileInput(
                attrs={
                    "accept": ".xls,.xlsx",
                    "class": "hidden",
                    "x-ref": "fileInput",
                }
            ),
        }

    def clean_file(self):
        """Validate the uploaded Excel file."""
        excel_file = self.cleaned_data.get("file")

        if excel_file:
            # Check file size
            if hasattr(excel_file, "size") and excel_file.size > self.MAX_FILE_SIZE:
                raise ValidationError(
                    f"File too large (max {self.MAX_FILE_SIZE // (1024*1024)}MB)"
                )

            # Check file extension
            if hasattr(excel_file, "name"):
                ext = excel_file.name.split(".")[-1].lower()
                if ext not in self.ALLOWED_EXTENSIONS:
                    raise ValidationError(
                        f'Invalid file type. Allowed: {", ".join(self.ALLOWED_EXTENSIONS)}'
                    )

            # Check magic bytes (actual file type, not just extension)
            try:
                file_mime = magic.from_buffer(excel_file.read(2048), mime=True)
                excel_file.seek(0)  # Reset file pointer

                if file_mime not in self.ALLOWED_MIME_TYPES:
                    raise ValidationError("Invalid Excel file format")

            except Exception as e:
                raise ValidationError(f"Could not validate file type: {str(e)}")

            # Basic check for malicious content
            # Excel files with macros could be dangerous
            excel_file.seek(0)
            content = excel_file.read(1024)
            excel_file.seek(0)

            # Check for VBA macro signatures
            if b"vbaProject" in content or b"_VBA_PROJECT" in content:
                raise ValidationError(
                    "Files with macros are not allowed for security reasons"
                )

        return excel_file
