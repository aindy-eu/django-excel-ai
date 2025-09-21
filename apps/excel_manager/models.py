import hashlib
from typing import Dict, Any
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


def upload_to(instance, filename):
    """Generate upload path for Excel files."""
    return f"excel_uploads/{instance.user.id}/{filename}"


class ExcelUpload(models.Model):
    """Represents an uploaded Excel file."""

    # Status choices
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]

    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="excel_uploads"
    )

    # File info
    file = models.FileField(
        upload_to="excel_uploads/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=["xls", "xlsx"])],
    )
    original_filename = models.CharField(max_length=255)
    file_hash = models.CharField(
        max_length=64, unique=True, help_text="SHA256 hash for duplicate detection"
    )

    # Processing status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    error_message = models.TextField(blank=True)

    # Metadata
    file_size = models.BigIntegerField()
    sheet_count = models.IntegerField(null=True, blank=True)

    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["user", "-uploaded_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["file_hash"]),
        ]

    def __str__(self):
        return f"{self.original_filename} ({self.user.email})"

    def get_absolute_url(self):
        return reverse("excel_manager:detail", kwargs={"pk": self.pk})

    def calculate_file_hash(self):
        """Calculate SHA256 hash of the file content."""
        sha256_hash = hashlib.sha256()
        for chunk in self.file.chunks():
            sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    @property
    def file_size_mb(self):
        """Return file size in MB."""
        return round(self.file_size / (1024 * 1024), 2)

    def get_preview_data(self, rows: int = 100) -> Dict[str, Any]:
        """Get preview data for AI validation.

        Args:
            rows: Number of rows to include in preview

        Returns:
            Dict with columns and sample data
        """
        # Get first sheet's data for validation
        first_sheet = self.sheets.first()  # type: ignore
        if not first_sheet:
            return {"columns": [], "sample": []}

        sheet_data = first_sheet.row_data
        headers = sheet_data.get("headers", [])
        data_rows = sheet_data.get("rows", [])[:rows]

        return {
            "columns": headers,
            "sample": data_rows,
            "total_rows": len(sheet_data.get("rows", [])),
            "sheet_name": first_sheet.sheet_name,
        }

    def has_recent_validation(self, hours: int = 1) -> bool:
        """Check if a recent validation exists."""
        from datetime import timedelta

        cutoff = timezone.now() - timedelta(hours=hours)
        return self.ai_validations.filter(validated_at__gte=cutoff).exists()  # type: ignore


class ExcelData(models.Model):
    """Stores parsed Excel data for display."""

    # Relationships
    upload = models.ForeignKey(
        ExcelUpload, on_delete=models.CASCADE, related_name="sheets"
    )

    # Sheet info
    sheet_name = models.CharField(max_length=255)
    sheet_index = models.IntegerField()

    # Data storage
    row_data = models.JSONField(
        default=dict, help_text="Stores headers and rows as JSON"
    )

    class Meta:
        ordering = ["sheet_index"]
        unique_together = ["upload", "sheet_index"]

    def __str__(self):
        return f"{self.upload.original_filename} - {self.sheet_name}"

    @property
    def row_count(self):
        """Return the number of rows in this sheet."""
        return len(self.row_data.get("rows", []))

    @property
    def headers(self):
        """Return the headers for this sheet."""
        return self.row_data.get("headers", [])


class AIValidation(models.Model):
    """Stores AI validation results for Excel uploads."""

    # Relationships
    excel_upload = models.ForeignKey(
        ExcelUpload, on_delete=models.CASCADE, related_name="ai_validations"
    )

    # Validation results
    validation_result = models.JSONField(
        help_text="Structured response: {issues, summary, severity}"
    )
    issues_found = models.IntegerField(default=0)
    suggestions = models.TextField(blank=True)

    # Metadata
    ai_metadata = models.JSONField(
        default=dict, help_text="Stores tokens, cost, model, response_time"
    )

    # Timestamps
    validated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-validated_at"]
        indexes = [
            models.Index(fields=["excel_upload", "-validated_at"]),
        ]

    def __str__(self):
        return f"Validation for {self.excel_upload.original_filename} at {self.validated_at}"

    @property
    def cost(self) -> float:
        """Calculate cost from token usage.

        Returns:
            float: Cost in dollars
        """
        tokens = self.ai_metadata.get("tokens", {})
        # Claude 4 Sonnet pricing: $0.003 per 1K input, $0.015 per 1K output
        input_cost = tokens.get("input_tokens", 0) * 0.003 / 1000
        output_cost = tokens.get("output_tokens", 0) * 0.015 / 1000
        return round(input_cost + output_cost, 6)

    @property
    def total_tokens(self) -> int:
        """Total tokens used in validation."""
        tokens = self.ai_metadata.get("tokens", {})
        return tokens.get("input_tokens", 0) + tokens.get("output_tokens", 0)

    @property
    def severity(self) -> str:
        """Get overall severity from validation result."""
        return self.validation_result.get("severity", "unknown")

    @property
    def valid_rows(self) -> int:
        """Number of valid rows found."""
        return self.validation_result.get("valid_rows", 0)

    @property
    def warning_rows(self) -> int:
        """Number of rows with warnings."""
        return self.validation_result.get("warning_rows", 0)

    @property
    def error_rows(self) -> int:
        """Number of rows with errors."""
        return self.validation_result.get("error_rows", 0)

    @property
    def summary(self) -> str:
        """Get summary from validation result."""
        return self.validation_result.get("summary", "")
