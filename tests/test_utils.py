import pytest

from probe.terminal_interface import provider_selection
from probe.core.utils import api_key_validation


def test_provider_selection_plain(monkeypatch, capsys):
    # Simulate user entering invalid then valid selection
    inputs = ['invalid', '1']
    def fake_prompt(prompt_text, validator=None):
        # return next input
        return inputs.pop(0)
    monkeypatch.setattr('probe.terminal_interface.provider_selection.prompt', fake_prompt)

    # Force plain text fallback
    monkeypatch.setattr(provider_selection, 'HAS_RICH', False)

    selected = provider_selection.select_provider(display_message_func=print, max_attempts=3)
    assert selected == 'openai'
    captured = capsys.readouterr()
    assert 'AVAILABLE LLM PROVIDERS' in captured.out


def test_api_key_validation(monkeypatch):
    valid, msg = api_key_validation.APIKeyValidator.validate_format('sk-1234567890abcdef', 'openai')
    assert valid
    invalid, msg = api_key_validation.APIKeyValidator.validate_format('foo', 'openai')
    assert not invalid

    # environment variable check
    monkeypatch.setenv('OPENAI_API_KEY', 'sk-envkey1234567890')
    assert api_key_validation.APIKeyValidator.check_env_variables('openai') == 'sk-envkey1234567890'

    # test interactive prompt function
    prompts = ['bad', 'sk-validkey12345678901234']
    def fake_prompt(msg, is_password=False):
        return prompts.pop(0)
    monkeypatch.setattr(api_key_validation, 'prompt', fake_prompt)
    # capture output
    def collector(message):
        print(message)
    key = api_key_validation.validate_api_key_interactive(
        provider='openai',
        max_attempts=3,
        display_message_func=collector,
        show_setup_instructions=False,
    )
    assert key.startswith('sk-')
