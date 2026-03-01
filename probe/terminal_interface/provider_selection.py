"""
Provider selection module for Probe.
Displays an interactive menu for users to select their preferred LLM provider.
"""

import os
import sys
from typing import Optional, Dict, List

# Try to import rich for nice formatting, fallback to plain text
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError


class ProviderValidator(Validator):
    """Validates provider selection input."""
    
    def __init__(self, max_option: int):
        self.max_option = max_option
    
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(message="Please enter a number")
        if not text.isdigit():
            raise ValidationError(message="Please enter a valid number")
        if int(text) < 1 or int(text) > self.max_option:
            raise ValidationError(message=f"Please enter a number between 1 and {self.max_option}")


# Provider configurations
PROVIDERS = {
    'openai': {
        'name': 'OpenAI',
        'description': 'GPT-4, GPT-4o, GPT-3.5-turbo (requires API key)',
        'requires_key': True,
        'env_vars': ['OPENAI_API_KEY'],
        'models': ['gpt-4o', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'],
        'default_model': 'gpt-4o',
    },
    'anthropic': {
        'name': 'Anthropic',
        'description': 'Claude 3.5 Sonnet, Claude 3 Opus (requires API key)',
        'requires_key': True,
        'env_vars': ['ANTHROPIC_API_KEY'],
        'models': ['claude-3-5-sonnet', 'claude-3-opus', 'claude-3-sonnet'],
        'default_model': 'claude-3-5-sonnet-20240620',
    },
    'ollama': {
        'name': 'Ollama',
        'description': 'Local models via Ollama (requires Ollama running locally)',
        'requires_key': False,
        'env_vars': [],
        'models': ['llama2', 'mistral', 'neural-chat', 'dolphin-mixtral'],
        'default_model': 'llama2',
    },
    'llamafile': {
        'name': 'Llamafile',
        'description': 'Single file LLM distribution (requires Llamafile running)',
        'requires_key': False,
        'env_vars': [],
        'models': ['auto-detected'],
        'default_model': 'auto-detected',
    },
    'lm-studio': {
        'name': 'LM Studio',
        'description': 'Local models via LM Studio (requires LM Studio running)',
        'requires_key': False,
        'env_vars': [],
        'models': ['auto-detected'],
        'default_model': 'auto-detected',
    },
    'jan': {
        'name': 'Jan',
        'description': 'Jan AI models (requires Jan running locally)',
        'requires_key': False,
        'env_vars': [],
        'models': ['auto-detected'],
        'default_model': 'auto-detected',
    },
    'google': {
        'name': 'Google Generative AI',
        'description': 'Gemini models (requires API key)',
        'requires_key': True,
        'env_vars': ['GOOGLE_API_KEY'],
        'models': ['gemini-pro', 'gemini-1.5-pro'],
        'default_model': 'gemini-pro',
    },
    'azure': {
        'name': 'Azure OpenAI',
        'description': 'OpenAI models hosted on Azure (requires API key and deployment)',
        'requires_key': True,
        'env_vars': ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT'],
        'models': ['gpt-4', 'gpt-35-turbo'],
        'default_model': 'gpt-4',
    },
    'cohere': {
        'name': 'Cohere',
        'description': 'Cohere models (requires API key)',
        'requires_key': True,
        'env_vars': ['COHERE_API_KEY'],
        'models': ['command', 'command-light'],
        'default_model': 'command',
    },
}


def is_termux() -> bool:
    """Detect if running in Termux environment."""
    return os.path.exists('/data/data/com.termux')


def get_terminal_width() -> int:
    """Get terminal width for formatting."""
    try:
        import shutil
        return shutil.get_terminal_size().columns
    except:
        return 80


def display_provider_menu_rich(providers: Dict[str, dict]) -> str:
    """Display provider menu using Rich library."""
    if not HAS_RICH:
        return display_provider_menu_plain(providers)
    
    console = Console()
    
    # Create a table for providers
    table = Table(title="[bold cyan]Available LLM Providers[/bold cyan]", show_header=True)
    table.add_column("[bold]#[/bold]", justify="center", width=3)
    table.add_column("[bold]Provider[/bold]", justify="left")
    table.add_column("[bold]Description[/bold]", justify="left")
    
    provider_list = list(providers.items())
    for idx, (key, config) in enumerate(provider_list, 1):
        key_emoji = "🔑" if config['requires_key'] else "✓"
        table.add_row(
            str(idx),
            f"{config['name']} {key_emoji}",
            config['description']
        )
    
    console.print(table)
    console.print(Panel("[yellow]Note: 🔑 = Requires API key[/yellow]", expand=False))
    
    return str(len(provider_list))


def display_provider_menu_plain(providers: Dict[str, dict]) -> str:
    """Display provider menu using plain text."""
    print("\n" + "=" * 70)
    print("AVAILABLE LLM PROVIDERS")
    print("=" * 70)
    print()
    
    provider_list = list(providers.items())
    for idx, (key, config) in enumerate(provider_list, 1):
        requires_key_str = "(requires API key)" if config['requires_key'] else "(local)"
        print(f"  {idx}. {config['name']} {requires_key_str}")
        print(f"     {config['description']}")
        print()
    
    print("=" * 70)
    return str(len(provider_list))


def select_provider(
    display_message_func=None,
    max_attempts: int = 3,
    available_providers: Optional[List[str]] = None
) -> Optional[str]:
    # Debug logging for troubleshooting (prints to stderr so it's visible in non-clean buffers)
    try:
        sys.stdout.write(f"[debug] select_provider called, max_attempts={max_attempts}\n")
        sys.stdout.flush()
    except Exception:
        pass
    """
    Display provider selection menu and get user's choice.
    
    Args:
        display_message_func: Optional function to display messages
        max_attempts: Maximum number of retry attempts
        available_providers: List of provider keys to show (None = all)
    
    Returns:
        Selected provider key or None if cancelled
    """
    # Filter providers if specified
    if available_providers:
        providers = {k: v for k, v in PROVIDERS.items() if k in available_providers}
    else:
        providers = PROVIDERS
    
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        try:
            sys.stdout.write(f"[debug] attempt {attempts}/{max_attempts}\n")
            sys.stdout.flush()
            # Display menu
            if HAS_RICH:
                max_idx = display_provider_menu_rich(providers)
            else:
                max_idx = display_provider_menu_plain(providers)

            # We print a plain prompt header to make automation easier
            sys.stdout.write("\nProvider menu displayed.\n")
            sys.stdout.flush()
            
            # Get user input
            try:
                choice = prompt(
                    "Select a provider (enter number): ",
                    validator=ProviderValidator(int(max_idx))
                )
            except (KeyboardInterrupt, EOFError):
                if display_message_func:
                    display_message_func("Provider selection cancelled.")
                return None
            
            # Convert choice to provider key
            choice_idx = int(choice) - 1
            provider_list = list(providers.items())
            selected_key = provider_list[choice_idx][0]
            selected_config = provider_list[choice_idx][1]
            
            if display_message_func:
                display_message_func(f"✓ Selected: {selected_config['name']}")
            
            return selected_key
        
        except (ValidationError, ValueError) as e:
            if attempts < max_attempts:
                if display_message_func:
                    display_message_func(f"Invalid selection. Please try again.")
            else:
                if display_message_func:
                    display_message_func(f"Maximum attempts reached.")
                return None
        except KeyboardInterrupt:
            if display_message_func:
                display_message_func("Provider selection cancelled.")
            return None
        except Exception as e:
            if display_message_func:
                display_message_func(f"Error: {str(e)}")
            if attempts < max_attempts:
                if display_message_func:
                    display_message_func("Please try again.")
            else:
                return None
    
    return None


def get_provider_config(provider_key: str) -> Optional[dict]:
    """Get configuration for a specific provider."""
    return PROVIDERS.get(provider_key)


def get_provider_name(provider_key: str) -> str:
    """Get human-readable name for a provider."""
    config = PROVIDERS.get(provider_key)
    return config['name'] if config else provider_key


def get_default_model_for_provider(provider_key: str) -> str:
    """Get default model for a provider."""
    config = PROVIDERS.get(provider_key)
    return config['default_model'] if config else 'unknown'


def requires_api_key(provider_key: str) -> bool:
    """Check if provider requires an API key."""
    config = PROVIDERS.get(provider_key)
    return config['requires_key'] if config else False


def get_environment_variables_for_provider(provider_key: str) -> List[str]:
    """Get the environment variables used by a provider."""
    config = PROVIDERS.get(provider_key)
    return config['env_vars'] if config else []
