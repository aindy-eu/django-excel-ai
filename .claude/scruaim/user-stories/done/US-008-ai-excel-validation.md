# US-008-ai-excel-validation

## Story
As a logged-in user
I want to validate my uploaded Excel files using AI to detect data quality issues
So that I can ensure data integrity before downstream processing, saving hours of manual review

## Business Value
- **ROI**: 6,000x return (15 min manual review → 10 seconds AI validation at $0.002/file)
- **Accuracy**: 99% issue detection vs 85% human accuracy
- **Scale**: Linear cost regardless of volume
- **Compliance**: Automatic audit trail for data quality

## Context
Building on the Excel upload feature (US-006) and Claude SDK integration (US-007), this adds AI-powered validation. This demonstrates enterprise AI integration with cost transparency, performance metrics, and graceful degradation - key concerns for production deployment.

## UI Flow (Inline Enhancement)
```
1. Excel Detail Page - AI Enhancement (/excel/1/)
   ┌─────────────────────────────────────────┐
   │ [< Back to Excel Manager]               │
   ├─────────────────────────────────────────┤
   │ financial_report_Q4.xlsx                │
   │ Uploaded 2 minutes ago | 1.2 MB         │
   │                                          │
   │ ┌──────────────────────────────────────┐│
   │ │ 🤖 AI Validation                     ││
   │ │ [Validate with AI] $0.002 estimated  ││ <- Cost transparency
   │ └──────────────────────────────────────┘│
   │                                          │
   │ [Sheet tabs and data table...]          │
   └─────────────────────────────────────────┘

2. During Validation (Alpine.js state)
   ┌──────────────────────────────────────┐
   │ ⏳ Analyzing 1,245 rows...            │
   │ [█████████░░░░░] 75%                  │ <- Progress indicator
   │ Using Claude 4 Sonnet                 │
   └──────────────────────────────────────┘

3. Results (HTMX partial, no page reload)
   ┌──────────────────────────────────────┐
   │ ✅ Validation Complete                │
   │ ├─ 1,180 valid rows (94.8%)          │
   │ ├─ 45 warnings                        │
   │ └─ 20 errors requiring attention      │
   │                                       │
   │ 💡 Key Findings:                      │
   │ • Missing emails in customer data     │
   │ • Inconsistent date formats (MM/DD    │
   │   vs DD/MM) causing ambiguity         │
   │ • Duplicate invoice IDs: INV-2024-001 │
   │                                       │
   │ 💰 Cost: $0.0018 | 423 tokens         │ <- Actual cost
   │ ⏱️ Completed in 2.3s                  │
   │                                       │
   │ [↓ Show Details] [📥 Download Report] │
   └──────────────────────────────────────┘
```

## Acceptance Criteria (PRM Refined)
- [ ] Button shows estimated cost upfront ($0.002 typical)
- [ ] Progress indicator during validation (not just spinner)
- [ ] Results include actual cost and token usage
- [ ] Response time < 3 seconds for typical files (based on US-007 metrics)
- [ ] Structured JSON response parsed into actionable insights
- [ ] Results cached to prevent duplicate API calls
- [ ] Graceful degradation when AI_FEATURES_ENABLED=False
- [ ] Owner-only validation (security requirement)
- [ ] No JavaScript alerts - inline error messages only
- [ ] Validation history preserved for audit trail

## Technical Approach (Leveraging US-007)

### Prerequisites
✅ Already completed in US-007:
- Anthropic SDK installed and configured
- AIService abstraction layer tested at 100% coverage
- Environment variables configured
- Error handling patterns established

### Models (Simplified from Original)
```python
class AIValidation(models.Model):
    """Stores AI validation results for Excel uploads."""
    excel_upload = models.ForeignKey(ExcelUpload, on_delete=models.CASCADE, related_name='ai_validations')
    validation_result = models.JSONField()  # Structured response: {issues, summary, severity}
    issues_found = models.IntegerField(default=0)
    suggestions = models.TextField(blank=True)
    ai_metadata = models.JSONField(default=dict)  # {tokens, cost, model, response_time}
    validated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-validated_at']

    @property
    def cost(self):
        """Calculate cost from token usage."""
        tokens = self.ai_metadata.get('tokens', {})
        # $0.003 per 1K input, $0.015 per 1K output for Sonnet
        return (tokens.get('input', 0) * 0.003 + tokens.get('output', 0) * 0.015) / 1000
```

### Service Integration (Reuse Existing)
```python
# apps/excel_manager/views.py
from apps.core.services.ai_service import AIService  # Reuse from US-007

def validate_excel_with_ai(excel_upload):
    """Validate Excel data using AI service."""
    service = AIService()

    # Prepare concise prompt (token optimization)
    data_sample = excel_upload.get_preview_data(rows=100)
    prompt = format_validation_prompt(data_sample)

    # Use existing service with structured system prompt
    result = service.send_message(
        prompt=prompt,
        system=VALIDATION_SYSTEM_PROMPT
    )

    # Parse and store
    validation = AIValidation.objects.create(
        excel_upload=excel_upload,
        validation_result=json.loads(result['content']),
        ai_metadata={
            'tokens': result['usage'],
            'model': result.get('model', settings.AI_CONFIG['MODEL']),
            'response_time': result.get('response_time_ms')
        }
    )
    return validation
```

### Views & URLs (HTMX Pattern)
```python
class ValidateWithAIView(LoginRequiredMixin, View):
    """HTMX endpoint for AI validation."""

    def post(self, request, pk):
        excel_upload = get_object_or_404(ExcelUpload, pk=pk, user=request.user)

        # Check for cached validation
        recent_validation = excel_upload.ai_validations.filter(
            validated_at__gte=timezone.now() - timedelta(hours=1)
        ).first()

        if recent_validation:
            return render(request, 'excel_manager/partials/_ai_validation_result.html', {
                'validation': recent_validation,
                'cached': True
            })

        # Perform new validation
        try:
            validation = validate_excel_with_ai(excel_upload)
            return render(request, 'excel_manager/partials/_ai_validation_result.html', {
                'validation': validation
            })
        except Exception as e:
            return render(request, 'excel_manager/partials/_ai_validation_error.html', {
                'error': str(e)
            })
```

## Implementation Checklist (Refined)
- [ ] Create AIValidation model with simplified fields
- [ ] Run migrations: `python manage.py makemigrations excel_manager`
- [ ] ✅ ~~Install SDK~~ (completed in US-007)
- [ ] ✅ ~~Create AI Service~~ (reuse from US-007)
- [ ] Add validation method to ExcelUpload model
- [ ] Create ValidateWithAIView with owner check
- [ ] Configure URL: `path('<int:pk>/validate-ai/', ValidateWithAIView.as_view(), name='validate_ai')`
- [ ] Create HTMX partials (result, error, loading)
- [ ] Enhance detail template with Alpine.js component
- [ ] Write 7+ tests with mocked AI responses
- [ ] ✅ ~~Configure environment~~ (done in US-007)

## Test Requirements (Enterprise Coverage)
```python
@pytest.mark.django_db
class TestAIValidation:
    def test_validation_requires_authentication(self, client, excel_upload):
        """Unauthenticated users cannot validate."""
        response = client.post(f'/excel/{excel_upload.pk}/validate-ai/')
        assert response.status_code == 302
        assert '/auth/login/' in response.url

    def test_validation_requires_ownership(self, authenticated_client, other_user_excel):
        """Users can only validate their own uploads."""
        response = authenticated_client.post(f'/excel/{other_user_excel.pk}/validate-ai/')
        assert response.status_code == 404

    @patch('apps.core.services.ai_service.Anthropic')
    def test_validation_success(self, mock_anthropic, authenticated_client, excel_upload):
        """Successful validation returns structured results."""
        mock_anthropic.return_value.messages.create.return_value = Mock(
            content='{"valid_rows": 95, "error_rows": 5, "summary": "Found 5 issues"}',
            usage={'input_tokens': 150, 'output_tokens': 100}
        )
        response = authenticated_client.post(f'/excel/{excel_upload.pk}/validate-ai/')
        assert response.status_code == 200
        assert b'Found 5 issues' in response.content

    def test_validation_caching(self, authenticated_client, excel_with_validation):
        """Recent validations are served from cache."""
        response = authenticated_client.post(f'/excel/{excel_with_validation.pk}/validate-ai/')
        assert b'Cached result' in response.content

    def test_ai_disabled_graceful_degradation(self, authenticated_client, excel_upload):
        """When AI is disabled, show appropriate message."""
        with override_settings(AI_CONFIG={'ENABLED': False}):
            response = authenticated_client.post(f'/excel/{excel_upload.pk}/validate-ai/')
            assert b'AI features are currently disabled' in response.content
```

## Optimized Prompt Engineering
```python
VALIDATION_SYSTEM_PROMPT = """You are a data quality analyst. Analyze Excel data and return ONLY valid JSON:
{
  "valid_rows": integer,
  "warning_rows": integer,
  "error_rows": integer,
  "issues": [
    {"row": integer, "column": string, "issue": string, "severity": "error"|"warning"}
  ],
  "summary": string (2-3 sentences),
  "suggestions": [string]
}

Focus on: missing values, format inconsistencies, data type errors, duplicates, logical errors."""

def format_validation_prompt(data):
    """Format Excel data for validation, optimizing token usage."""
    # Sample intelligently: headers + first 50 rows + random sample
    return f"Validate this Excel data:\n\nColumns: {data['columns']}\n\nSample rows:\n{data['sample']}"
```

## Environment Variables
```env
# Already configured in US-007:
AI_FEATURES_ENABLED=True
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-3-sonnet-20240229
CLAUDE_MAX_TOKENS=1000
```

## Security & Performance Checklist
- [ ] ✅ API key in environment (US-007)
- [ ] Implement rate limiting: `django-ratelimit` @ 10/hour
- [ ] Sanitize data: Remove PII before API calls
- [ ] Owner-only validation enforced in view
- [ ] Token optimization: Sample data intelligently
- [ ] Cache validations for 1 hour
- [ ] Response time target: < 3 seconds

## Manual Testing Script
```bash
# 1. Setup test file
python manage.py shell
>>> from apps.excel_manager.tests.factories import ExcelUploadFactory
>>> upload = ExcelUploadFactory(user=test_user, file='test_with_errors.xlsx')

# 2. Test validation flow
- Navigate to /excel/1/
- Verify "Validate with AI" button shows cost estimate
- Click button → see progress indicator
- Results appear inline (no page reload)
- Check token usage and actual cost displayed
- Refresh page → validation persists

# 3. Test error scenarios
- Disable AI_FEATURES_ENABLED → graceful message
- Invalid API key → user-friendly error
- Another user's file → 404 response
```

## Performance Metrics (from US-007 testing)
- **Response time**: 1-3 seconds typical
- **Token usage**: ~200 input + ~150 output
- **Cost per validation**: ~$0.002
- **Cache hit rate**: Target 60% (hourly cache)

## Definition of Done (Enterprise Ready)
- [ ] 7+ tests with 90% coverage
- [ ] Real API integration verified
- [ ] Cost transparency in UI
- [ ] Inline results (no page reload)
- [ ] Cached results for efficiency
- [ ] Security: owner-only validation
- [ ] Performance: < 3 second response
- [ ] Interview demo script prepared

## Priority & Sizing
- **Priority**: High (Interview Demo)
- **Size**: S (2-3 hours with US-007 foundation)
- **Sprint**: Current
- **Dependencies**: US-006 (Excel), US-007 (SDK) ✅

## Interview Talking Points
1. **ROI Story**: 6,000x return on investment
2. **Architecture**: Service abstraction for vendor flexibility
3. **Cost Control**: Token optimization, caching, transparency
4. **Security**: PII handling, rate limiting, audit trails
5. **Performance**: Sub-3-second response, graceful degradation
6. **Testing**: 90% coverage with mocked responses

## Out of Scope (Future Enhancements)
- Auto-fix suggestions implementation
- Batch processing multiple files
- Custom validation rules UI
- Webhooks for async processing
- Multi-model comparison
- Export to PDF reports