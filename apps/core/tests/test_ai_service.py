"""Unit tests for AI Service."""

import pytest
from unittest.mock import patch, MagicMock
from apps.core.services.ai_service import AIService


class TestAIService:
    """Test cases for AIService class."""

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
        # Configure mock settings
        mock_settings.AI_CONFIG = {
            'ENABLED': True,
            'ANTHROPIC_API_KEY': 'test-key',
            'MODEL': 'test-model',
            'MAX_TOKENS': 100
        }

        # Mock response
        mock_content = MagicMock()
        mock_content.text = "Test response"

        mock_usage = MagicMock()
        mock_usage.input_tokens = 10
        mock_usage.output_tokens = 20

        mock_response = MagicMock()
        mock_response.content = [mock_content]
        mock_response.usage = mock_usage

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        # Test the service
        service = AIService()
        result = service.send_message("Test prompt")

        # Assertions
        assert result['success'] is True
        assert result['content'] == "Test response"
        assert result['usage']['input_tokens'] == 10
        assert result['usage']['output_tokens'] == 20

        # Verify the API was called correctly
        mock_client.messages.create.assert_called_once_with(
            model='test-model',
            max_tokens=100,
            messages=[{'role': 'user', 'content': 'Test prompt'}]
        )

    @patch('apps.core.services.ai_service.Anthropic')
    @patch('apps.core.services.ai_service.settings')
    def test_send_message_with_system(self, mock_settings, mock_anthropic):
        """Test message sending with system prompt."""
        # Configure mock settings
        mock_settings.AI_CONFIG = {
            'ENABLED': True,
            'ANTHROPIC_API_KEY': 'test-key',
            'MODEL': 'test-model',
            'MAX_TOKENS': 100
        }

        # Mock response
        mock_content = MagicMock()
        mock_content.text = "Response with system"

        mock_usage = MagicMock()
        mock_usage.input_tokens = 15
        mock_usage.output_tokens = 25

        mock_response = MagicMock()
        mock_response.content = [mock_content]
        mock_response.usage = mock_usage

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        # Test the service with system prompt
        service = AIService()
        result = service.send_message("User prompt", system="System context")

        # Assertions
        assert result['success'] is True
        assert result['content'] == "Response with system"

        # Verify the API was called with system parameter
        mock_client.messages.create.assert_called_once_with(
            model='test-model',
            max_tokens=100,
            messages=[{'role': 'user', 'content': 'User prompt'}],
            system="System context"
        )

    @patch('apps.core.services.ai_service.Anthropic')
    @patch('apps.core.services.ai_service.settings')
    def test_send_message_handles_errors(self, mock_settings, mock_anthropic):
        """Test error handling in message sending."""
        # Configure mock settings
        mock_settings.AI_CONFIG = {
            'ENABLED': True,
            'ANTHROPIC_API_KEY': 'test-key',
            'MODEL': 'test-model',
            'MAX_TOKENS': 100
        }

        # Mock an API error
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = Exception("API Error")
        mock_anthropic.return_value = mock_client

        # Test the service
        service = AIService()
        result = service.send_message("Test prompt")

        # Assertions
        assert result['success'] is False
        assert "API Error" in result['error']
        assert result['content'] is None

    @patch('apps.core.services.ai_service.Anthropic')
    @patch('apps.core.services.ai_service.settings')
    def test_test_connection_success(self, mock_settings, mock_anthropic):
        """Test the connection test method when successful."""
        # Configure mock settings
        mock_settings.AI_CONFIG = {
            'ENABLED': True,
            'ANTHROPIC_API_KEY': 'test-key',
            'MODEL': 'test-model',
            'MAX_TOKENS': 100
        }

        # Mock successful response
        mock_content = MagicMock()
        mock_content.text = "OK"

        mock_usage = MagicMock()
        mock_usage.input_tokens = 5
        mock_usage.output_tokens = 2

        mock_response = MagicMock()
        mock_response.content = [mock_content]
        mock_response.usage = mock_usage

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        # Test the service
        service = AIService()
        result = service.test_connection()

        # Assertions
        assert result is True

    @patch('apps.core.services.ai_service.Anthropic')
    @patch('apps.core.services.ai_service.settings')
    def test_test_connection_failure(self, mock_settings, mock_anthropic):
        """Test the connection test method when it fails."""
        # Configure mock settings
        mock_settings.AI_CONFIG = {
            'ENABLED': True,
            'ANTHROPIC_API_KEY': 'test-key',
            'MODEL': 'test-model',
            'MAX_TOKENS': 100
        }

        # Mock API error
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = Exception("Connection failed")
        mock_anthropic.return_value = mock_client

        # Test the service
        service = AIService()
        result = service.test_connection()

        # Assertions
        assert result is False