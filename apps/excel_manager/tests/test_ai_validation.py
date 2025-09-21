"""Tests for AI Excel validation feature."""

import json
from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from apps.excel_manager.models import AIValidation
from apps.excel_manager.views import validate_excel_with_ai


@pytest.mark.django_db
class TestAIValidationModel:
    """Test AIValidation model functionality."""

    def test_cost_calculation(self, excel_upload):
        """Test that cost is calculated correctly from token usage."""
        validation = AIValidation.objects.create(
            excel_upload=excel_upload,
            validation_result={"valid_rows": 100},
            ai_metadata={"tokens": {"input_tokens": 1000, "output_tokens": 500}},
        )

        # $0.003 per 1K input + $0.015 per 1K output
        expected_cost = (1000 * 0.003 + 500 * 0.015) / 1000
        assert validation.cost == round(expected_cost, 6)

    def test_total_tokens_property(self, excel_upload):
        """Test total tokens calculation."""
        validation = AIValidation.objects.create(
            excel_upload=excel_upload,
            validation_result={},
            ai_metadata={"tokens": {"input_tokens": 150, "output_tokens": 100}},
        )
        assert validation.total_tokens == 250

    def test_validation_properties(self, excel_upload):
        """Test validation result property accessors."""
        validation = AIValidation.objects.create(
            excel_upload=excel_upload,
            validation_result={
                "valid_rows": 95,
                "warning_rows": 3,
                "error_rows": 2,
                "severity": "low",
                "summary": "Data looks good overall",
            },
            issues_found=5,
        )

        assert validation.valid_rows == 95
        assert validation.warning_rows == 3
        assert validation.error_rows == 2
        assert validation.severity == "low"
        assert validation.summary == "Data looks good overall"


@pytest.mark.django_db
class TestExcelUploadAIIntegration:
    """Test ExcelUpload model AI integration methods."""

    def test_get_preview_data(self, excel_upload_with_data):
        """Test preview data extraction for AI validation."""
        preview = excel_upload_with_data.get_preview_data(rows=5)

        assert "columns" in preview
        assert "sample" in preview
        assert "total_rows" in preview
        assert "sheet_name" in preview
        assert len(preview["columns"]) == 3  # Based on fixture data
        assert len(preview["sample"]) <= 5

    def test_get_preview_data_empty(self, excel_upload):
        """Test preview data when no sheets exist."""
        preview = excel_upload.get_preview_data()

        assert preview["columns"] == []
        assert preview["sample"] == []

    def test_has_recent_validation(self, excel_upload):
        """Test checking for recent validations."""
        # No validations yet
        assert not excel_upload.has_recent_validation()

        # Create old validation (2 hours ago)
        old_validation = AIValidation.objects.create(
            excel_upload=excel_upload, validation_result={}
        )
        # Manually set validated_at to 2 hours ago
        old_validation.validated_at = timezone.now() - timedelta(hours=2)
        old_validation.save()

        assert not excel_upload.has_recent_validation(hours=1)

        # Create recent validation
        AIValidation.objects.create(excel_upload=excel_upload, validation_result={})
        assert excel_upload.has_recent_validation(hours=1)


@pytest.mark.django_db
class TestValidateWithAIView:
    """Test AI validation view."""

    def test_validation_requires_authentication(self, client, excel_upload):
        """Unauthenticated users cannot validate."""
        url = reverse("excel_manager:validate_ai", kwargs={"pk": excel_upload.pk})
        response = client.post(url)

        assert response.status_code == 302
        assert "/auth/login/" in response.url

    def test_validation_requires_ownership(
        self, authenticated_client, other_user, excel_upload_factory
    ):
        """Users can only validate their own uploads."""
        other_upload = excel_upload_factory(user=other_user)
        url = reverse("excel_manager:validate_ai", kwargs={"pk": other_upload.pk})
        response = authenticated_client.post(url)

        assert response.status_code == 404

    @patch("apps.excel_manager.views.AIService")
    def test_validation_success(
        self, mock_ai_service, authenticated_client, excel_upload_with_data
    ):
        """Successful validation returns structured results."""
        # Mock AI service response
        mock_service = Mock()
        mock_ai_service.return_value = mock_service
        mock_service.send_message.return_value = {
            "success": True,
            "content": json.dumps(
                {
                    "valid_rows": 95,
                    "warning_rows": 3,
                    "error_rows": 2,
                    "issues": [
                        {
                            "row": 5,
                            "column": "Email",
                            "issue": "Missing value",
                            "severity": "error",
                        }
                    ],
                    "summary": "Found 5 data quality issues",
                    "suggestions": ["Check email fields"],
                    "severity": "low",
                }
            ),
            "usage": {"input_tokens": 150, "output_tokens": 100},
            "model": "claude-sonnet-4-20250514",
        }

        url = reverse(
            "excel_manager:validate_ai", kwargs={"pk": excel_upload_with_data.pk}
        )
        response = authenticated_client.post(url)

        assert response.status_code == 200
        assert b"Validation Complete" in response.content
        assert b"Found 5 data quality issues" in response.content
        assert b"95" in response.content  # Valid rows

        # Check that validation was created
        validation = AIValidation.objects.get(excel_upload=excel_upload_with_data)
        assert validation.valid_rows == 95
        assert validation.issues_found == 1

    def test_validation_caching(self, authenticated_client, excel_upload_with_data):
        """Recent validations are served from cache."""
        # Create a recent validation
        AIValidation.objects.create(
            excel_upload=excel_upload_with_data,
            validation_result={
                "valid_rows": 100,
                "summary": "Cached validation result",
            },
            validated_at=timezone.now() - timedelta(minutes=30),
        )

        url = reverse(
            "excel_manager:validate_ai", kwargs={"pk": excel_upload_with_data.pk}
        )
        response = authenticated_client.post(url)

        assert response.status_code == 200
        # Check for cache indicator in the response
        assert b"Cached" in response.content or b"cached" in response.content
        assert b"Cached validation result" in response.content

    @override_settings(AI_CONFIG={"ENABLED": False})
    def test_ai_disabled_graceful_degradation(self, authenticated_client, excel_upload):
        """When AI is disabled, show appropriate message."""
        url = reverse("excel_manager:validate_ai", kwargs={"pk": excel_upload.pk})
        response = authenticated_client.post(url)

        assert response.status_code == 503
        assert b"AI features are currently disabled" in response.content

    @patch("apps.excel_manager.views.AIService")
    def test_validation_handles_ai_error(
        self, mock_ai_service, authenticated_client, excel_upload_with_data
    ):
        """Handle AI service errors gracefully."""
        mock_service = Mock()
        mock_ai_service.return_value = mock_service
        mock_service.send_message.side_effect = Exception("AI service unavailable")

        url = reverse(
            "excel_manager:validate_ai", kwargs={"pk": excel_upload_with_data.pk}
        )
        response = authenticated_client.post(url)

        assert response.status_code == 500
        assert b"AI service unavailable" in response.content

    @patch("apps.excel_manager.views.AIService")
    def test_validation_handles_invalid_json(
        self, mock_ai_service, authenticated_client, excel_upload_with_data
    ):
        """Handle non-JSON AI responses gracefully."""
        mock_service = Mock()
        mock_ai_service.return_value = mock_service
        mock_service.send_message.return_value = {
            "success": True,
            "content": "This is not valid JSON",
            "usage": {"input_tokens": 100, "output_tokens": 50},
        }

        url = reverse(
            "excel_manager:validate_ai", kwargs={"pk": excel_upload_with_data.pk}
        )
        response = authenticated_client.post(url)

        assert response.status_code == 200
        # Should create validation with fallback structure
        validation = AIValidation.objects.get(excel_upload=excel_upload_with_data)
        assert validation.validation_result["severity"] == "unknown"
        assert "This is not valid JSON" in validation.validation_result["summary"]


@pytest.mark.django_db
class TestValidateExcelWithAI:
    """Test the validate_excel_with_ai function."""

    @patch("apps.excel_manager.views.AIService")
    def test_validate_excel_with_ai_success(
        self, mock_ai_service, excel_upload_with_data
    ):
        """Test successful AI validation."""
        mock_service = Mock()
        mock_ai_service.return_value = mock_service
        mock_service.send_message.return_value = {
            "success": True,
            "content": json.dumps(
                {
                    "valid_rows": 90,
                    "warning_rows": 5,
                    "error_rows": 5,
                    "issues": [
                        {
                            "row": 3,
                            "column": "Date",
                            "issue": "Invalid format",
                            "severity": "warning",
                        }
                    ],
                    "summary": "Data quality is good",
                    "suggestions": ["Standardize date formats"],
                    "severity": "low",
                }
            ),
            "usage": {"input_tokens": 200, "output_tokens": 150},
            "model": "claude-sonnet-4-20250514",
        }

        validation = validate_excel_with_ai(excel_upload_with_data)

        assert validation.excel_upload == excel_upload_with_data
        assert validation.valid_rows == 90
        assert validation.issues_found == 1
        assert "Standardize date formats" in validation.suggestions
        assert validation.ai_metadata["tokens"]["input_tokens"] == 200

    @patch("apps.excel_manager.views.AIService")
    def test_validate_excel_no_data(self, mock_ai_service, excel_upload):
        """Test validation with no data raises error."""
        with pytest.raises(ValueError, match="No data to validate"):
            validate_excel_with_ai(excel_upload)


@pytest.mark.django_db
class TestDetailViewAIIntegration:
    """Test detail view AI integration."""

    def test_detail_view_shows_ai_section(self, authenticated_client, excel_upload):
        """Detail view should show AI validation section when enabled."""
        url = reverse("excel_manager:detail", kwargs={"pk": excel_upload.pk})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        if settings.AI_CONFIG.get("ENABLED"):
            assert b"AI Validation Available" in response.content
            assert b"Validate with AI" in response.content
            assert b"Estimated cost: $0.002" in response.content

    def test_detail_view_shows_previous_validation(
        self, authenticated_client, excel_upload
    ):
        """Detail view should show previous validation if exists."""
        # Create a validation
        AIValidation.objects.create(
            excel_upload=excel_upload,
            validation_result={"summary": "Previous validation summary"},
            issues_found=3,
        )

        url = reverse("excel_manager:detail", kwargs={"pk": excel_upload.pk})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        if settings.AI_CONFIG.get("ENABLED"):
            # Check for validation result display
            assert b"validation" in response.content.lower()
            # Check for issue count display (might be shown as "detailed issues (3)")
            assert b"(3)" in response.content or b"Issues found: 3" in response.content
