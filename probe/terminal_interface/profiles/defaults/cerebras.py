"""
This is an Probe profile to use Cerebras. 

Please set the CEREBRAS_API_KEY environment variable.

See https://inference-docs.cerebras.ai/introduction for more information.
"""

from probe import probe
import os

# LLM settings
probe.llm.api_base = "https://api.cerebras.ai/v1"
probe.llm.model = "openai/llama3.1-70b"  # or "openai/Llama-3.1-8B"
probe.llm.api_key = os.environ.get("CEREBRAS_API_KEY")
probe.llm.supports_functions = False
probe.llm.supports_vision = False
probe.llm.max_tokens = 4096
probe.llm.context_window = 8192


# Computer settings
probe.computer.import_computer_api = False

# Misc settings
probe.offline = False
probe.auto_run = False

# Custom Instructions
probe.custom_instructions = f"""

    """
