"""Management command to test AI service connection."""

from django.core.management.base import BaseCommand
from apps.core.services.ai_service import AIService


class Command(BaseCommand):
    help = 'Test AI service connection'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Testing AI service connection...\n')

            service = AIService()
            if service.test_connection():
                self.stdout.write(
                    self.style.SUCCESS('✅ AI service is working!')
                )

                # Detailed test
                self.stdout.write('\nRunning detailed test...')
                result = service.send_message(
                    "What is 2+2? Reply with just the number."
                )

                if result['success']:
                    self.stdout.write(f"\nResponse: {result['content']}")
                    self.stdout.write(
                        f"Tokens used: input={result['usage']['input_tokens']}, "
                        f"output={result['usage']['output_tokens']}"
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Test failed: {result.get('error')}")
                    )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ AI service test failed - could not connect')
                )

        except ValueError as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Configuration error: {str(e)}')
            )
            self.stdout.write(
                '\nPlease ensure you have set the following environment variables:\n'
                '  - AI_FEATURES_ENABLED=True\n'
                '  - ANTHROPIC_API_KEY=your_api_key_here\n'
                '  - CLAUDE_MODEL (optional)\n'
                '  - CLAUDE_MAX_TOKENS (optional)'
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Unexpected error: {str(e)}')
            )