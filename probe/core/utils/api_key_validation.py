"""
API Key validation module for various LLM providers.
Provides robust validation, environment variable checking, and user prompts.
"""

import os
import re
from typing import Optional, Tuple
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError


class APIKeyValidator:
    """Validates API keys for different providers."""
    
    # Provider-specific validation patterns and rules
    PROVIDER_CONFIG = {
        'openai': {
            'pattern': r'^(sk-proj-|sk-)[A-Za-z0-9\-_]+$',
            'min_length': 20,
            'env_vars': ['OPENAI_API_KEY'],
            'name': 'OpenAI',
            'format_help': 'OpenAI keys start with "sk-" or "sk-proj-" and are at least 20 characters long'
        },
        'anthropic': {
            'pattern': r'^sk-ant-[A-Za-z0-9\-_]+$',
            'min_length': 20,
            'env_vars': ['ANTHROPIC_API_KEY'],
            'name': 'Anthropic',
            'format_help': 'Anthropic keys start with "sk-ant-" and are at least 20 characters long'
        },
        'google': {
            'pattern': r'^[A-Za-z0-9_\-]+$',
            'min_length': 10,
            'env_vars': ['GOOGLE_API_KEY'],
            'name': 'Google',
            'format_help': 'Google API keys must be at least 10 characters long'
        },
        'azure': {
            'pattern': r'^[A-Za-z0-9\-]+$',
            'min_length': 10,
            'env_vars': ['AZURE_API_KEY', 'AZURE_OPENAI_API_KEY'],
            'name': 'Azure OpenAI',
            'format_help': 'Azure keys must be at least 10 characters long'
        },
        'cohere': {
            'pattern': r'^[A-Za-z0-9\-_]+$',
            'min_length': 10,
            'env_vars': ['COHERE_API_KEY'],
            'name': 'Cohere',
            'format_help': 'Cohere keys must be at least 10 characters long'
        },
        'huggingface': {
            'pattern': r'^hf_[A-Za-z0-9_]+$',
            'min_length': 15,
            'env_vars': ['HF_API_KEY', 'HUGGINGFACE_API_KEY'],
            'name': 'Hugging Face',
            'format_help': 'Hugging Face keys start with "hf_" and are at least 15 characters long'
        },
        'default': {
            'pattern': r'^[A-Za-z0-9\-_]+$',
            'min_length': 10,
            'env_vars': ['API_KEY'],
            'name': 'API',
            'format_help': 'API keys must be at least 10 characters long'
        }
    }
    
    @staticmethod
    def get_config_for_provider(provider: str) -> dict:
        """Get validation config for a provider, with fallback to default."""
        provider_lower = provider.lower()
        return APIKeyValidator.PROVIDER_CONFIG.get(
            provider_lower, 
            APIKeyValidator.PROVIDER_CONFIG['default']
        )
    
    @staticmethod
    def check_env_variables(provider: str) -> Optional[str]:
        """
        Check if API key exists in environment variables.
        Returns the key if found, None otherwise.
        """
        config = APIKeyValidator.get_config_for_provider(provider)
        for env_var in config['env_vars']:
            key = os.environ.get(env_var)
            if key:
                return key
        return None
    
    @staticmethod
    def validate_format(api_key: str, provider: str = 'default') -> Tuple[bool, str]:
        """
        Validate API key format for a specific provider.
        Returns (is_valid, error_message)
        """
        api_key = api_key.strip()
        
        if not api_key:
            return False, "API key cannot be empty"
        
        config = APIKeyValidator.get_config_for_provider(provider)
        
        # Check minimum length
        if len(api_key) < config['min_length']:
            return False, f"API key is too short (minimum {config['min_length']} characters)"
        
        # Check format pattern
        if not re.match(config['pattern'], api_key):
            return False, f"API key format is invalid. {config['format_help']}"
        
        # Check for common mistakes
        if ' ' in api_key:
            return False, "API key contains spaces (should not have spaces)"
        
        if '\n' in api_key:
            return False, "API key contains newlines (should be a single line)"
        
        return True, "API key format is valid"
    
    @staticmethod
    def prompt_for_api_key(
        provider: str = 'openai',
        max_attempts: int = 3,
        display_message_func=None
    ) -> Optional[str]:
        """
        Prompt user for API key with validation and retries.
        
        Args:
            provider: Provider name (openai, anthropic, etc.)
            max_attempts: Maximum number of retry attempts
            display_message_func: Optional function to display messages (for UI integration)
        
        Returns:
            Valid API key if user provides one, None if they cancel/give up
        """
        config = APIKeyValidator.get_config_for_provider(provider)
        
        # First, check environment variables
        env_key = APIKeyValidator.check_env_variables(provider)
        if env_key:
            if display_message_func:
                display_message_func(f"✓ Using {config['name']} API key from environment variable")
            return env_key
        
        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            
            if display_message_func:
                display_message_func(
                    f"\n> Please enter your {config['name']} API key (Attempt {attempts}/{max_attempts})"
                )
            
            try:
                api_key = prompt(
                    f"{config['name']} API Key: ",
                    is_password=True
                )
            except (KeyboardInterrupt, EOFError):
                if display_message_func:
                    display_message_func("API key entry cancelled.")
                return None
            
            # Validate the key
            is_valid, error_msg = APIKeyValidator.validate_format(api_key, provider)
            
            if is_valid:
                if display_message_func:
                    display_message_func(f"✓ {config['name']} API key accepted")
                return api_key
            else:
                if display_message_func:
                    display_message_func(f"✗ Invalid {config['name']} API key: {error_msg}")
                
                if attempts < max_attempts:
                    if display_message_func:
                        display_message_func(f"Please try again or press Ctrl+C to cancel.")
        
        if display_message_func:
            display_message_func(f"Maximum attempts ({max_attempts}) reached. Giving up.")
        
        return None
    
    @staticmethod
    def get_setup_instructions(provider: str = 'openai', os_type: str = None) -> str:
        """
        Get OS-specific instructions for saving API keys permanently.
        
        Args:
            provider: Provider name
            os_type: Operating system type ('linux', 'darwin', 'win32', None for auto-detect)
        
        Returns:
            Instructions string
        """
        if os_type is None:
            import sys
            os_type = sys.platform
        
        config = APIKeyValidator.get_config_for_provider(provider)
        env_var = config['env_vars'][0]
        
        if 'linux' in os_type or 'darwin' in os_type:
            return f"""
To save your {config['name']} API key permanently on Linux/macOS:

Option 1: Add to shell profile (~/.bashrc, ~/.zshrc, or ~/.bash_profile):
    export {env_var}='your-api-key-here'

Option 2: Use environment file management:
    export {env_var}='your-api-key-here'

Then reload your shell:
    source ~/.bashrc  # or ~/.zshrc or ~/.bash_profile

Option 3: Use a .env file with python-dotenv
"""
        elif 'win32' in os_type:
            return f"""
To save your {config['name']} API key permanently on Windows:

Option 1: Set environment variable via GUI:
    1. Press Win + X and select "System"
    2. Click "Advanced system settings"
    3. Click "Environment Variables"
    4. Click "New" under "User variables"
    5. Variable name: {env_var}
    6. Variable value: your-api-key-here
    7. Click OK and restart your terminal

Option 2: Set environment variable via PowerShell (run as Administrator):
    [Environment]::SetEnvironmentVariable('{env_var}', 'your-api-key-here', 'User')
    $env:{env_var} = 'your-api-key-here'

Option 3: Use .env file with python-dotenv
"""
        else:  # Generic instructions
            return f"""
To save your {config['name']} API key permanently:

1. Add to your shell profile:
    export {env_var}='your-api-key-here'

2. Reload your shell configuration

3. Or use a .env file with python-dotenv library
"""


def validate_api_key_interactive(
    provider: str = 'openai',
    max_attempts: int = 3,
    display_message_func=None,
    show_setup_instructions: bool = True
) -> Optional[str]:
    """
    Full interactive API key validation flow.
    
    Args:
        provider: Provider name
        max_attempts: Maximum retry attempts
        display_message_func: Optional message display function
        show_setup_instructions: Whether to show setup instructions
    
    Returns:
        Valid API key if obtained, None otherwise
    """
    api_key = APIKeyValidator.prompt_for_api_key(
        provider=provider,
        max_attempts=max_attempts,
        display_message_func=display_message_func
    )
    
    if api_key is None and show_setup_instructions and display_message_func:
        instructions = APIKeyValidator.get_setup_instructions(provider)
        display_message_func(instructions)
    
    return api_key
