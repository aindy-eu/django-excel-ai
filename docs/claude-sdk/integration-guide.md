# Claude SDK Integration Guide

This guide explains how to integrate AI features into new Django components using our Claude SDK service layer.

## Implementation Status

✅ **Working**: AIService core, Excel validation implementation
📚 **Examples**: The patterns below are working examples you can copy
🚧 **Not Built**: AIUsageLog model, ai_analyze command, aiValidator Alpine component

## 📦 Prerequisites

1. Ensure environment variables are configured (.env file)
2. Service layer is available at `apps.core.services.ai_service`
3. Django settings include AI_CONFIG

## 🚀 Quick Integration Steps

### Step 1: Import the Service

```python
from apps.core.services.ai_service import AIService
```

### Step 2: Initialize and Use

```python
def your_view_function(request):
    try:
        # Initialize the AI service
        ai_service = AIService()

        # Send a message
        result = ai_service.send_message("Your prompt here")

        # Check success and use response
        if result['success']:
            content = result['content']
            # Process the AI response
        else:
            # Handle error
            error_msg = result['error']
    except ValueError as e:
        # AI features not enabled or configured
        pass
```

## 📝 Common Integration Patterns

### 1. Form Validation with AI (📚 EXAMPLE)

```python
# forms.py
from django import forms
from apps.core.services.ai_service import AIService

class DataUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']

        # Use AI to validate file content
        try:
            ai_service = AIService()
            content_sample = file.read(1000).decode('utf-8')

            result = ai_service.send_message(
                f"Check this data for issues: {content_sample}"
            )

            if result['success'] and 'error' in result['content'].lower():
                raise forms.ValidationError(
                    f"AI detected issues: {result['content'][:200]}"
                )
        except:
            # AI unavailable, continue with normal validation
            pass

        return file
```

### 2. HTMX Partial View with AI (✅ PATTERN USED IN EXCEL)

```python
# views.py
from django.views.generic import View
from django.shortcuts import render
from apps.core.services.ai_service import AIService

class AIValidateView(View):
    def post(self, request, pk):
        # Get the object to validate
        obj = MyModel.objects.get(pk=pk)

        # Initialize AI service
        ai_service = AIService()

        # Prepare data for validation
        prompt = f"""
        Validate this data:
        {obj.get_data_for_validation()}

        Return issues in JSON format.
        """

        # Get AI response
        result = ai_service.send_message(prompt)

        context = {
            'object': obj,
            'ai_result': result,
            'success': result.get('success', False)
        }

        # Return HTMX partial
        return render(
            request,
            'partials/htmx/_ai_validation_results.html',
            context
        )
```

### 3. Template Integration

```html
<!-- Button to trigger AI validation -->
<button
  hx-post="{% url 'validate_with_ai' object.id %}"
  hx-target="#ai-results"
  hx-indicator="#loading"
  class="btn btn-primary"
>
  🤖 Validate with AI
</button>

<!-- Loading indicator -->
<div id="loading" class="htmx-indicator">🔄 AI is analyzing...</div>

<!-- Results container -->
<div id="ai-results">
  <!-- AI results will be inserted here -->
</div>
```

### 4. Alpine.js Component (🚧 EXAMPLE - NOT IMPLEMENTED)

```javascript
// static/js/alpine/components/aiValidator.js
document.addEventListener("alpine:init", () => {
  Alpine.data("aiValidator", () => ({
    validating: false,
    result: null,
    error: null,

    async validate(data) {
      this.validating = true;
      this.error = null;

      try {
        const response = await fetch("/api/ai-validate/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({ data }),
        });

        this.result = await response.json();
      } catch (error) {
        this.error = "AI validation failed";
      } finally {
        this.validating = false;
      }
    },
  }));
});
```

### 5. Management Command Integration (📚 EXAMPLE - Similar to test_ai)

```python
# management/commands/ai_analyze.py
from django.core.management.base import BaseCommand
from apps.core.services.ai_service import AIService

class Command(BaseCommand):
    help = 'Analyze data using AI'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='File to analyze')

    def handle(self, *args, **options):
        file_path = options.get('file')

        try:
            ai_service = AIService()

            with open(file_path, 'r') as f:
                content = f.read()

            result = ai_service.send_message(
                f"Analyze this content and provide insights: {content[:1000]}"
            )

            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(f"Analysis: {result['content']}")
                )
                self.stdout.write(
                    f"Tokens used: {result['usage']}"
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"Error: {result['error']}")
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed: {str(e)}")
            )
```

## 🎯 Best Practices

### 1. Always Handle AI Unavailability

```python
try:
    ai_service = AIService()
    # AI operations
except ValueError:
    # AI not configured - gracefully degrade
    return regular_processing()
```

### 2. Cache Expensive Operations

```python
from django.core.cache import cache

def get_ai_analysis(data_key):
    # Check cache first
    cached = cache.get(f'ai_analysis_{data_key}')
    if cached:
        return cached

    # Get from AI
    ai_service = AIService()
    result = ai_service.send_message(f"Analyze: {data}")

    # Cache for 1 hour
    if result['success']:
        cache.set(f'ai_analysis_{data_key}', result, 3600)

    return result
```

### 3. Use System Prompts for Consistency

```python
VALIDATION_SYSTEM_PROMPT = """
You are a data quality expert. Always respond in JSON format:
{
    "valid": boolean,
    "issues": [],
    "suggestions": []
}
"""

result = ai_service.send_message(
    prompt=user_data,
    system=VALIDATION_SYSTEM_PROMPT
)
```

### 4. Log Important Operations

```python
import logging

logger = logging.getLogger(__name__)

def process_with_ai(data):
    logger.info(f"Starting AI processing for {data.id}")

    result = ai_service.send_message(prompt)

    logger.info(
        f"AI processing complete. "
        f"Success: {result['success']}, "
        f"Tokens: {result.get('usage', {})}"
    )

    return result
```

### 5. Implement Rate Limiting

```python
from django.core.cache import cache
from django.http import JsonResponse

def rate_limited_ai_view(request):
    # Check rate limit (10 requests per hour per user)
    cache_key = f'ai_rate_{request.user.id}'
    count = cache.get(cache_key, 0)

    if count >= 10:
        return JsonResponse({
            'error': 'Rate limit exceeded. Try again later.'
        }, status=429)

    # Increment counter
    cache.set(cache_key, count + 1, 3600)

    # Process with AI
    # ...
```

## 🔧 Configuration Options

### Custom Token Limits

```python
# For specific use cases requiring more tokens
ai_service = AIService()
ai_service.max_tokens = 2000  # Override default
```

### Different Models

```python
# Future: When multiple models are available
ai_service = AIService()
ai_service.model = 'claude-opus-4'  # Use Opus 4 for complex tasks
```

## 📊 Monitoring and Debugging

### Enable Debug Logging

Already configured in settings:

```python
LOGGING = {
    'loggers': {
        'apps.core.services.ai_service': {
            'level': 'DEBUG',
        },
        'anthropic': {
            'level': 'INFO',
        },
    }
}
```

### Track Usage Metrics (🚧 EXAMPLE MODEL - NOT IMPLEMENTED)

```python
from django.db import models

class AIUsageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt_tokens = models.IntegerField()
    completion_tokens = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def log_usage(cls, user, result):
        if result.get('success'):
            usage = result['usage']
            # Calculate cost (example rates)
            cost = (usage['input_tokens'] * 0.003 +
                   usage['output_tokens'] * 0.015) / 1000

            cls.objects.create(
                user=user,
                prompt_tokens=usage['input_tokens'],
                completion_tokens=usage['output_tokens'],
                total_cost=cost
            )
```

## 🚨 Error Handling Examples

### Network Errors

```python
result = ai_service.send_message(prompt)

if not result['success']:
    error = result['error']

    if 'timeout' in error.lower():
        # Handle timeout
        messages.warning(request, "AI service is slow, please try again.")
    elif 'authentication' in error.lower():
        # Handle API key issues
        logger.error("AI API key issue detected")
        messages.error(request, "AI service unavailable.")
    else:
        # Generic error
        messages.error(request, "AI analysis failed.")
```

### Validation Errors

```python
try:
    ai_service = AIService()
except ValueError as e:
    if "not enabled" in str(e):
        # Feature flag is off
        return HttpResponse("AI features are disabled", status=503)
    elif "not configured" in str(e):
        # Missing API key
        logger.error("AI service misconfigured")
        return HttpResponse("AI service unavailable", status=503)
```

## 📋 Testing Your Integration

### Unit Test Example

```python
from unittest.mock import patch, MagicMock
from django.test import TestCase

class TestAIIntegration(TestCase):
    @patch('your_app.views.AIService')
    def test_ai_validation(self, mock_ai_service):
        # Mock the AI response
        mock_instance = MagicMock()
        mock_instance.send_message.return_value = {
            'success': True,
            'content': 'No issues found',
            'usage': {'input_tokens': 10, 'output_tokens': 5}
        }
        mock_ai_service.return_value = mock_instance

        # Test your view/function
        response = self.client.post('/validate-with-ai/', data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        mock_instance.send_message.assert_called_once()
```

## 📊 What's Actually Implemented

| Feature | Status | Location |
|---------|--------|----------|
| AIService core | ✅ Working | `apps/core/services/ai_service.py` |
| Excel validation | ✅ Production | `apps/excel_manager/views.py` |
| test_ai command | ✅ Working | `apps/core/management/commands/test_ai.py` |
| Error handling | ✅ Implemented | Throughout AIService and views |
| Caching pattern | ✅ Used | Excel validation with 1-hour cache |
| AIUsageLog model | 🚧 Example only | Not implemented |
| aiValidator Alpine | 🚧 Example only | Not implemented |
| ai_analyze command | 🚧 Example only | Not implemented |

## 🎯 Key Takeaways

1. **AIService is flexible** - Can handle any prompt/system combination
2. **Error handling works** - Graceful degradation when unavailable
3. **Examples are copyable** - Patterns shown work with minor adjustments
4. **Excel is the reference** - See `apps/excel_manager/` for production patterns

---

_Last verified against codebase: 2025-09-20_
