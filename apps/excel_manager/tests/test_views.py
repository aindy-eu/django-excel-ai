import pytest
from django.urls import reverse
from apps.excel_manager.models import ExcelUpload, ExcelData


@pytest.mark.django_db
class TestExcelUpload:

    def test_upload_requires_login(self, client):
        """Test that upload requires authentication."""
        url = reverse("excel_manager:upload")
        response = client.post(url)
        assert response.status_code == 302  # Redirect to login

    def test_main_page_requires_login(self, client):
        """Test that main page requires authentication."""
        url = reverse("excel_manager:index")
        response = client.get(url)
        assert response.status_code == 302  # Redirect to login

    def test_main_page_loads_for_authenticated_user(self, authenticated_client):
        """Test that authenticated users can access main page."""
        url = reverse("excel_manager:index")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert b"Excel Manager" in response.content
        assert b"Upload Excel File" in response.content

    def test_valid_excel_upload(self, authenticated_client, excel_file):
        """Test successful upload of valid Excel file."""
        url = reverse("excel_manager:upload")
        authenticated_client.post(url, {"file": excel_file})

        # Check upload was created
        assert ExcelUpload.objects.count() == 1
        upload = ExcelUpload.objects.first()
        assert upload.original_filename == "test_data.xlsx"
        assert upload.status == ExcelUpload.STATUS_COMPLETED
        assert upload.sheet_count == 2

        # Check sheets were parsed
        assert ExcelData.objects.count() == 2
        sheet1 = ExcelData.objects.get(sheet_index=0)
        assert sheet1.sheet_name == "Sheet1"
        assert len(sheet1.row_data["headers"]) == 4
        assert len(sheet1.row_data["rows"]) == 3

    def test_file_size_limit(self, authenticated_client):
        """Test that files over 5MB are rejected."""
        # Create a mock large file
        from django.core.files.uploadedfile import SimpleUploadedFile

        large_content = b"X" * (6 * 1024 * 1024)  # 6MB of data
        large_file = SimpleUploadedFile(
            "large.xlsx",
            large_content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        url = reverse("excel_manager:upload")
        authenticated_client.post(url, {"file": large_file})

        # Should not create upload due to size limit
        assert ExcelUpload.objects.count() == 0

    def test_invalid_file_type(self, authenticated_client, pdf_file_as_xlsx):
        """Test that non-Excel files are rejected even with .xlsx extension."""
        url = reverse("excel_manager:upload")
        authenticated_client.post(url, {"file": pdf_file_as_xlsx})

        # Should not create upload - validation should prevent it
        assert ExcelUpload.objects.count() == 0

    def test_duplicate_file_detection(self, authenticated_client, excel_file):
        """Test that duplicate files are detected by hash."""
        url = reverse("excel_manager:upload")

        # First upload
        authenticated_client.post(url, {"file": excel_file})
        assert ExcelUpload.objects.count() == 1

        # Try to upload same file again
        excel_file.seek(0)  # Reset file pointer
        authenticated_client.post(url, {"file": excel_file})

        # Should still only have 1 upload (duplicate detected)
        assert ExcelUpload.objects.count() == 1

    def test_htmx_partial_response(self, authenticated_client, excel_file):
        """Test that HTMX requests return partial templates."""
        url = reverse("excel_manager:upload")
        response = authenticated_client.post(
            url, {"file": excel_file}, HTTP_HX_REQUEST="true"
        )

        # Should return partial template, not redirect
        assert response.status_code == 200
        assert b"Your Excel Files" in response.content

    def test_user_can_only_see_own_uploads(
        self, authenticated_client, user, excel_file
    ):
        """Test that users can only see their own uploads."""
        # Upload file as first user
        url = reverse("excel_manager:upload")
        authenticated_client.post(url, {"file": excel_file})

        # Check user can see their upload
        index_url = reverse("excel_manager:index")
        response = authenticated_client.get(index_url)
        assert b"test_data.xlsx" in response.content

        # Create another user and check they can't see first user's upload
        from apps.users.tests.factories import UserFactory

        other_user = UserFactory()
        authenticated_client.force_login(other_user)

        response = authenticated_client.get(index_url)
        assert b"test_data.xlsx" not in response.content
        assert b"No Excel files uploaded yet" in response.content

    def test_excel_detail_view_requires_ownership(
        self, authenticated_client, user, excel_file
    ):
        """Test that users can only view details of their own uploads."""
        # Upload file
        url = reverse("excel_manager:upload")
        authenticated_client.post(url, {"file": excel_file})
        upload = ExcelUpload.objects.first()

        # User can view their own upload
        detail_url = reverse("excel_manager:detail", kwargs={"pk": upload.pk})
        response = authenticated_client.get(detail_url)
        assert response.status_code == 200
        assert b"test_data.xlsx" in response.content

        # Another user cannot view it
        from apps.users.tests.factories import UserFactory

        other_user = UserFactory()
        authenticated_client.force_login(other_user)

        response = authenticated_client.get(detail_url)
        assert response.status_code == 404  # Not found for other users

    def test_sheet_switching(self, authenticated_client, excel_file):
        """Test switching between sheets in detail view."""
        # Upload file
        url = reverse("excel_manager:upload")
        authenticated_client.post(url, {"file": excel_file})
        upload = ExcelUpload.objects.first()

        # Load detail view
        detail_url = reverse("excel_manager:detail", kwargs={"pk": upload.pk})
        response = authenticated_client.get(detail_url)
        assert response.status_code == 200
        assert b"Sheet1" in response.content
        assert b"Sheet2" in response.content

        # Test sheet switching via HTMX
        sheet_url = reverse(
            "excel_manager:sheet_data", kwargs={"pk": upload.pk, "sheet_index": 1}
        )
        response = authenticated_client.get(sheet_url, HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        # Sheet2 data should be in response
        assert b"Product" in response.content or b"Price" in response.content

    def test_upload_form_has_error_display_structure(self, authenticated_client):
        """Test that upload form includes error display structure for client-side validation."""
        url = reverse("excel_manager:index")
        response = authenticated_client.get(url)
        assert response.status_code == 200

        # Check for Alpine.js error handling structure
        assert b'x-show="error"' in response.content
        assert b'x-text="error"' in response.content
        assert b'@click="clearError()"' in response.content

        # Check for drag and drop functionality
        assert b'@drop.prevent="handleDrop($event)"' in response.content
        assert b"@dragover.prevent" in response.content

    def test_file_size_validation_message(self, authenticated_client):
        """Test that proper error message is shown for oversized files."""
        from django.core.files.uploadedfile import SimpleUploadedFile

        # Create file just over 5MB limit
        large_content = b"X" * (5 * 1024 * 1024 + 1)
        large_file = SimpleUploadedFile(
            "toolarge.xlsx",
            large_content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        url = reverse("excel_manager:upload")
        response = authenticated_client.post(url, {"file": large_file})

        # Should not create upload
        assert ExcelUpload.objects.count() == 0

        # Check response has form with errors
        if response.status_code == 400:
            # HTMX request returns 400 with error
            assert (
                b"error" in response.content.lower()
                or b"5mb" in response.content.lower()
            )
