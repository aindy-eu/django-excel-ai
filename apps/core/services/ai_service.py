"""AI Service for Claude SDK integration."""

from typing import Optional, Dict, Any
import logging
from anthropic import Anthropic
from django.conf import settings

logger = logging.getLogger(__name__)


class AIService:
    """Base service for AI interactions using Anthropic Claude SDK."""

    def __init__(self):
        if not settings.AI_CONFIG["ENABLED"]:
            raise ValueError("AI features are not enabled")

        if not settings.AI_CONFIG["ANTHROPIC_API_KEY"]:
            raise ValueError("ANTHROPIC_API_KEY not configured")

        self.client = Anthropic(api_key=settings.AI_CONFIG["ANTHROPIC_API_KEY"])
        self.model = settings.AI_CONFIG["MODEL"]
        self.max_tokens = settings.AI_CONFIG["MAX_TOKENS"]

    def send_message(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a message to Claude and return the response.

        Args:
            prompt: The user prompt to send
            system: Optional system message for context

        Returns:
            Dict containing success status, content, and usage info
        """
        try:
            logger.debug(f"Sending message to Claude API with model: {self.model}")
            logger.debug(f"Prompt length: {len(prompt)} characters")

            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": messages,
            }

            if system:
                kwargs["system"] = system
                logger.debug(f"Using system prompt: {system[:100]}...")

            message = self.client.messages.create(**kwargs)

            response_text = message.content[0].text if message.content else ""
            logger.debug(f"Response received: {response_text[:100]}...")
            logger.info(
                f"Tokens used: input={message.usage.input_tokens}, "
                f"output={message.usage.output_tokens}"
            )

            return {
                "success": True,
                "content": response_text,
                "usage": {
                    "input_tokens": message.usage.input_tokens,
                    "output_tokens": message.usage.output_tokens,
                },
            }

        except Exception as e:
            logger.error(f"AI Service error: {str(e)}")
            return {"success": False, "error": str(e), "content": None}

    def test_connection(self) -> bool:
        """Test if the AI service is properly configured and working."""
        result = self.send_message("Say 'OK' if you receive this.")
        return result.get("success", False)
