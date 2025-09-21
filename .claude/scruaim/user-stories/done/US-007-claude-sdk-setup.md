# US-007-claude-sdk-setup

## Story
As a developer
I want to set up the Anthropic Claude SDK in our Django application
So that we can integrate AI capabilities for features like Excel validation

## Context
This is a foundational setup task that prepares our Django application for AI integration. We need to properly install, configure, and verify the Anthropic Python SDK before building features that depend on it (like US-008 Excel AI validation). This demonstrates enterprise-level integration of cutting-edge AI tools.

## Acceptance Criteria
- [ ] Anthropic Python SDK is installed and locked in requirements files
- [ ] API key is configured through environment variables (never hardcoded)
- [ ] Basic connection test confirms SDK is working
- [ ] Service layer abstraction created for AI interactions
- [ ] Error handling implemented for API failures
- [ ] Settings properly configured for development and production
- [ ] Basic smoke test can call Claude API and get response
- [ ] Documentation updated with setup instructions

## Technical Approach

### Installation
```bash
# Add to requirements/base.txt
anthropic>=0.39.0  # Claude AI SDK

# Regenerate lock files
pip-compile requirements/base.txt --output-file requirements/base.lock
pip-compile requirements/development.txt --output-file requirements/development.lock
pip-sync requirements/development.lock
```

### Environment Configuration
```env
# .env (never commit)
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-3-sonnet-20240229  # or claude-3-opus-20240229
CLAUDE_MAX_TOKENS=1000
AI_FEATURES_ENABLED=True
```

### Settings Configuration
```python
# settings/base.py
import os
from dotenv import load_dotenv

load_dotenv()

# AI Configuration
AI_CONFIG = {
    'ENABLED': os.environ.get('AI_FEATURES_ENABLED', 'False') == 'True',
    'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY'),
    'MODEL': os.environ.get('CLAUDE_MODEL', 'claude-3-sonnet-20240229'),
    'MAX_TOKENS': int(os.environ.get('CLAUDE_MAX_TOKENS', '1000')),
    'TIMEOUT': 30,  # seconds
}
```

### Service Layer Architecture
```python
# apps/core/services/ai_service.py
from typing import Optional, Dict, Any
import logging
from anthropic import Anthropic
from django.conf import settings

logger = logging.getLogger(__name__)

class AIService:
    """Base service for AI interactions using Anthropic Claude SDK."""

    def __init__(self):
        if not settings.AI_CONFIG['ENABLED']:
            raise ValueError("AI features are not enabled")

        if not settings.AI_CONFIG['ANTHROPIC_API_KEY']:
            raise ValueError("ANTHROPIC_API_KEY not configured")

        self.client = Anthropic(
            api_key=settings.AI_CONFIG['ANTHROPIC_API_KEY']
        )
        self.model = settings.AI_CONFIG['MODEL']
        self.max_tokens = settings.AI_CONFIG['MAX_TOKENS']

    def send_message(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to Claude and return the response."""
        try:
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": messages
            }

            if system:
                kwargs["system"] = system

            message = self.client.messages.create(**kwargs)

            return {
                "success": True,
                "content": message.content[0].text if message.content else "",
                "usage": {
                    "input_tokens": message.usage.input_tokens,
                    "output_tokens": message.usage.output_tokens
                }
            }

        except Exception as e:
            logger.error(f"AI Service error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": None
            }

    def test_connection(self) -> bool:
        """Test if the AI service is properly configured and working."""
        result = self.send_message("Say 'OK' if you receive this.")
        return result.get("success", False)
```

### Management Command for Testing
```python
# apps/core/management/commands/test_ai.py
from django.core.management.base import BaseCommand
from apps.core.services.ai_service import AIService

class Command(BaseCommand):
    help = 'Test AI service connection'

    def handle(self, *args, **options):
        try:
            service = AIService()
            if service.test_connection():
                self.stdout.write(
                    self.style.SUCCESS('✅ AI service is working!')
                )

                # Detailed test
                result = service.send_message(
                    "What is 2+2? Reply with just the number."
                )
                if result['success']:
                    self.stdout.write(f"Response: {result['content']}")
                    self.stdout.write(f"Tokens used: {result['usage']}")
            else:
                self.stdout.write(
                    self.style.ERROR('❌ AI service test failed')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
```

## Implementation Checklist
- [ ] Add anthropic to requirements/base.txt
- [ ] Run pip-compile for all requirement files
- [ ] Run pip-sync to install packages
- [ ] Add AI configuration to .env.example
- [ ] Update settings/base.py with AI_CONFIG
- [ ] Create apps/core/services/ai_service.py
- [ ] Create management command test_ai
- [ ] Run python manage.py test_ai to verify
- [ ] Write unit tests for AIService
- [ ] Update README with setup instructions

## Test Requirements
```python
# apps/core/tests/test_ai_service.py
import pytest
from unittest.mock import patch, MagicMock
from apps.core.services.ai_service import AIService

class TestAIService:
    @patch('apps.core.services.ai_service.settings')
    def test_service_requires_enabled_flag(self, mock_settings):
        """AI service should raise error if not enabled."""
        mock_settings.AI_CONFIG = {'ENABLED': False}
        with pytest.raises(ValueError, match="not enabled"):
            AIService()

    @patch('apps.core.services.ai_service.settings')
    def test_service_requires_api_key(self, mock_settings):
        """AI service should raise error if API key missing."""
        mock_settings.AI_CONFIG = {
            'ENABLED': True,
            'ANTHROPIC_API_KEY': None
        }
        with pytest.raises(ValueError, match="not configured"):
            AIService()

    @patch('apps.core.services.ai_service.Anthropic')
    @patch('apps.core.services.ai_service.settings')
    def test_send_message_success(self, mock_settings, mock_anthropic):
        """Test successful message sending."""
        mock_settings.AI_CONFIG = {
            'ENABLED': True,
            'ANTHROPIC_API_KEY': 'test-key',
            'MODEL': 'test-model',
            'MAX_TOKENS': 100
        }

        # Mock response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Test response")]
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 20

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        service = AIService()
        result = service.send_message("Test prompt")

        assert result['success'] is True
        assert result['content'] == "Test response"
        assert result['usage']['input_tokens'] == 10

    @patch('apps.core.services.ai_service.Anthropic')
    @patch('apps.core.services.ai_service.settings')
    def test_send_message_handles_errors(self, mock_settings, mock_anthropic):
        """Test error handling in message sending."""
        mock_settings.AI_CONFIG = {
            'ENABLED': True,
            'ANTHROPIC_API_KEY': 'test-key',
            'MODEL': 'test-model',
            'MAX_TOKENS': 100
        }

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = Exception("API Error")
        mock_anthropic.return_value = mock_client

        service = AIService()
        result = service.send_message("Test prompt")

        assert result['success'] is False
        assert "API Error" in result['error']
        assert result['content'] is None
```

## Manual Testing Steps
1. Add ANTHROPIC_API_KEY to .env file
2. Run `pip-sync requirements/development.lock`
3. Run `python manage.py test_ai`
4. Verify "AI service is working!" message appears
5. Check response shows "4" for the 2+2 test
6. Test with invalid API key (should show error)
7. Test with AI_FEATURES_ENABLED=False (should show disabled message)

## Security Checklist
- [ ] API key stored in environment variables only
- [ ] .env file is in .gitignore
- [ ] No API keys in code or commits
- [ ] API responses logged without sensitive data
- [ ] Rate limiting considered for production
- [ ] Error messages don't expose API details

## Documentation Updates
Update README.md with:
```markdown
## AI Features Setup

### Prerequisites
1. Obtain an API key from [Anthropic Console](https://console.anthropic.com/)
2. Install dependencies: `pip-sync requirements/development.lock`

### Configuration
Add to your `.env` file:
```env
ANTHROPIC_API_KEY=your_api_key_here
AI_FEATURES_ENABLED=True
CLAUDE_MODEL=claude-3-sonnet-20240229
```

### Testing
Verify setup: `python manage.py test_ai`
```

## Definition of Done
- [ ] All tests passing (pytest apps/core/tests/test_ai_service.py)
- [ ] Management command confirms API connection
- [ ] No API keys in code
- [ ] Service layer properly abstracted
- [ ] Error handling tested
- [ ] Documentation updated
- [ ] Ready for US-008 implementation

## Priority & Size
- Priority: High (Blocker for US-008)
- Size: S (1-2 hours)
- Sprint: Current

## Questions/Blockers
- Confirm API key is available for development
- Verify model names (claude-3-sonnet vs claude-3-opus)
- Check rate limits for demo usage

## Dependencies
- Blocks: US-008 (AI Excel Validation)
- Depends on: None

## Out of Scope
- Streaming responses
- Async implementation (can add later if needed)
- Multiple model support
- Token usage tracking/billing
- Advanced prompt templates
- Caching responses
- Batch processing