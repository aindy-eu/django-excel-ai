# US-006-excel-upload-display

## Story
As a logged-in user
I want to upload Excel files (.xls/.xlsx) and view their contents in the browser
So that I can share and analyze spreadsheet data without requiring desktop software

## Context
Users frequently need to share Excel data with team members who may not have Excel installed. This feature enables web-based viewing of Excel files, with future potential for data import into the system. Starting with display-only MVP, focusing on files under 5MB for synchronous processing.

## UI Flow
```
1. Main Page (/excel/)
   ┌─────────────────────────────────────┐
   │ [Navigation with Excel Manager]      │
   ├─────────────────────────────────────┤
   │ ┌───────────────────────────────┐   │
   │ │  📊 Drop Excel files here     │   │  <- Drag & drop area
   │ │     or click to browse        │   │
   │ └───────────────────────────────┘   │
   │                                      │
   │ Your Excel Files:                   │
   │ ┌─────────────────────────────────┐ │
   │ │ File         Size   Date   Action│ │
   │ │ report.xlsx  2.3MB  Today  [View]│ │  <- Click View
   │ │ data.xls     1.1MB  Jan 15 [View]│ │
   │ └─────────────────────────────────┘ │
   └─────────────────────────────────────┘

2. Detail Page (/excel/1/)
   ┌─────────────────────────────────────┐
   │ [< Back to Excel Manager]           │
   ├─────────────────────────────────────┤
   │ report.xlsx - 3 sheets               │
   │ [Sheet1] [Sheet2] [Summary]         │  <- Tabs
   │ ┌─────────────────────────────────┐ │
   │ │ Col A │ Col B │ Col C │ Col D    │ │
   │ │ Data1 │ Data2 │ Data3 │ Data4    │ │  <- Table
   │ │ ...   │ ...   │ ...   │ ...      │ │
   │ └─────────────────────────────────┘ │
   └─────────────────────────────────────┘
```

## Acceptance Criteria
- [ ] Navigation menu includes "Excel Manager" item (with icon) that links to main page
- [ ] Main page shows drag-and-drop upload area at top with border and "Drop Excel files here or click to browse"
- [ ] User can drag-and-drop Excel files onto upload area with visual feedback (dashed border becomes solid)
- [ ] User can click upload area to select files via browser dialog
- [ ] System validates file is actual Excel format (not just .xlsx extension) with error "Invalid Excel file format"
- [ ] System validates file size (max 5MB) with error "File too large (max 5MB)"
- [ ] After successful upload, new file appears in list below without page refresh (HTMX)
- [ ] List of uploaded files shows: filename, file size, sheet count, uploaded date/time, and "View" button
- [ ] Clicking "View" button navigates to detail page showing Excel data
- [ ] Detail page displays sheet names as tabs, with first sheet active
- [ ] Detail page shows first 100 rows of active sheet in responsive HTML table
- [ ] Table displays with proper column headers from first row
- [ ] Empty cells show as blank (not "null" or "undefined")
- [ ] User can navigate back to main page via breadcrumb or "Back to Excel Manager" link

## Technical Approach

### Models Required
- [ ] Model: ExcelUpload with fields:
  - user (ForeignKey to AUTH_USER_MODEL)
  - file (FileField with upload_to='excel_uploads/%Y/%m/%d/')
  - original_filename (CharField max_length=255)
  - file_hash (CharField max_length=64, unique=True for duplicate detection)
  - status (CharField choices: pending/processing/completed/failed)
  - error_message (TextField blank=True)
  - file_size (BigIntegerField)
  - sheet_count (IntegerField null=True)
  - uploaded_at (DateTimeField auto_now_add=True)
  - processed_at (DateTimeField null=True)
- [ ] Model: ExcelData with fields:
  - upload (ForeignKey to ExcelUpload)
  - sheet_name (CharField max_length=255)
  - sheet_index (IntegerField)
  - row_data (JSONField for headers and rows)
- [ ] Encryption needed for PII: No (unless data contains sensitive info - phase 2)
- [ ] Admin registration needed: Yes (DEBUG only) for troubleshooting
- [ ] Migrations: Create new models
- [ ] Audit trail: No (MVP - add in phase 2)

### Views & URLs
- [ ] View type: TemplateView for main page with upload area and list (ExcelManagerView)
- [ ] View type: FormView for HTMX upload handling (ExcelUploadView)
- [ ] View type: DetailView for viewing Excel data (ExcelDetailView)
- [ ] URL patterns:
  - /excel/ (main page with upload area and list)
  - /excel/upload/ (HTMX POST endpoint for file upload)
  - /excel/<int:pk>/ (detail view for specific Excel file)
  - /excel/<int:pk>/sheet/<int:sheet_index>/ (HTMX partial for sheet switching)
- [ ] Templates:
  - excel_manager/index.html (main page with upload area and file list)
  - excel_manager/detail.html (Excel data display page)
  - excel_manager/partials/_file_list.html (HTMX partial for list refresh)
  - excel_manager/partials/_upload_area.html (reusable upload component)
  - excel_manager/partials/_data_table.html (sheet data display)
- [ ] Login required: Yes (all views)
- [ ] Permission class: IsAuthenticated
- [ ] Rate limiting: No (MVP - add if abuse detected)

### Templates
- [ ] Extends: base.html
- [ ] Blocks used: content, extra_js
- [ ] Components needed: upload area, file list table, sheet tabs, data table
- [ ] HTMX patterns:
  - Upload posts to /excel/upload/ and refreshes file list
  - Sheet switching loads partials without page refresh
- [ ] Alpine.js: excelUpload component for drag-drop (like avatarUpload.js)

### Forms
- [ ] Form class: ExcelUploadForm
- [ ] Fields: file (FileField)
- [ ] Validation:
  - Check magic bytes (not just extension)
  - Validate max size (5MB)
  - Basic malicious content check
- [ ] Crispy forms: Yes

### Static Files
- [ ] Custom CSS needed: No (Tailwind sufficient)
- [ ] JavaScript functionality: Alpine.js component for drag-drop
- [ ] Tailwind utilities sufficient: Yes
- [ ] Alpine component: static/js/alpine/components/excelUpload.js

## Implementation Checklist
- [ ] Create excel_manager app
- [ ] Create models (ExcelUpload, ExcelData)
- [ ] Create and run migrations
- [ ] Register models in admin (DEBUG only)
- [ ] Create ExcelUploadForm with validation
- [ ] Create views (ExcelManagerView, ExcelUploadView, ExcelDetailView)
- [ ] Configure URLs with namespace
- [ ] Create main page template (index.html) with upload area and file list
- [ ] Create detail page template (detail.html) for Excel viewing
- [ ] Create HTMX partials for dynamic updates
- [ ] Create Alpine.js component for drag-drop
- [ ] Add to base.html Alpine components
- [ ] Style with Tailwind (dark mode support)
- [ ] Add "Excel Manager" to main navigation menu with icon
- [ ] Write tests (minimum 10 tests for MVP)
- [ ] Test manually with various Excel files

## Test Requirements
```python
# Unit Tests (pytest-django)
class TestExcelUpload:
    def test_upload_requires_login(self, client):
        # Security: Must be authenticated
        response = client.post('/excel/upload/')
        assert response.status_code == 302  # Redirect to login

    def test_valid_excel_upload(self, authenticated_client, excel_file):
        # Happy path: Valid .xlsx file
        response = authenticated_client.post('/excel/upload/', {'file': excel_file})
        assert ExcelUpload.objects.count() == 1

    def test_file_size_limit(self, authenticated_client, large_excel):
        # Validation: Reject files over 5MB
        response = authenticated_client.post('/excel/upload/', {'file': large_excel})
        assert 'too large' in response.content

    def test_invalid_file_type(self, authenticated_client, pdf_file):
        # Security: Reject non-Excel files even with .xlsx extension
        response = authenticated_client.post('/excel/upload/', {'file': pdf_file})
        assert 'Invalid Excel file' in response.content

    def test_duplicate_file_detection(self, authenticated_client, excel_file):
        # Feature: Detect identical files by hash
        authenticated_client.post('/excel/upload/', {'file': excel_file})
        excel_file.seek(0)
        response = authenticated_client.post('/excel/upload/', {'file': excel_file})
        assert 'already uploaded' in response.content or ExcelUpload.objects.count() == 1

    def test_htmx_partial_response(self, authenticated_client, excel_file):
        # HTMX: Return partial template for HTMX requests
        response = authenticated_client.post(
            '/excel/upload/',
            {'file': excel_file},
            HTTP_HX_REQUEST='true'
        )
        assert 'partials/' in response.template_name
```

## Security Checklist
- [ ] File type validation using python-magic (not just extension)
- [ ] File size limit enforced server-side
- [ ] No formula evaluation (display only)
- [ ] No macro execution
- [ ] User can only see own uploads
- [ ] CSRF protection on upload form
- [ ] XSS prevention in data display

## Manual Testing Steps
1. Navigate to Excel Manager via menu item
2. Test drag-and-drop upload with valid .xlsx file
3. Verify file appears in list immediately after upload (no refresh)
4. Click "View" button and verify navigation to detail page
5. Test sheet tab switching on detail page
6. Test navigation back to main page
7. Test upload area click to open file browser
8. Test large file rejection (>5MB)
9. Test non-Excel file with .xlsx extension (should reject)
10. Verify file list shows: filename, size, sheet count, upload date
11. Test multi-sheet Excel file (all tabs visible on detail page)
12. Test Excel with 1000+ rows (should show first 100)
13. Verify dark mode styling on both pages
14. Test on mobile (responsive table and layout)
15. Verify user can only see own uploads in list

## Performance Criteria
- [ ] Upload processing < 3s for 5MB file
- [ ] Page load < 2s with 10 uploads in history
- [ ] Sheet switching < 500ms (HTMX partial)
- [ ] No memory issues with 5MB files

## Questions/Blockers
- Consider using openpyxl vs pandas for parsing (openpyxl simpler for MVP)
- Future: Add pagination for >100 rows?
- Future: Add search within Excel data?
- Future: Add export to CSV option?

## Definition of Done
- [ ] All tests passing (minimum 10 tests)
- [ ] Manual testing completed
- [ ] No linting errors (ruff, black)
- [ ] Dark mode verified
- [ ] Responsive design verified
- [ ] Documentation updated
- [ ] Added to navigation menu
- [ ] Follows avatar upload patterns

## Priority & Size
- Priority: Medium
- Size: L (4-8 hours)
- Sprint: Current

## Out of Scope
- Cell editing or data modification
- Formula evaluation or calculation
- Chart/graph rendering
- Conditional formatting display
- Files larger than 5MB (requires async processing)
- Export functionality (phase 2)
- Sharing with other users (phase 2)
- API endpoints (phase 3)
- Real-time collaboration
- Version history/comparison
- Scheduled imports
- Data import into Django models (requires mapping UI)