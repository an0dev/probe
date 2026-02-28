"""
This is an Probe profile. It configures Probe to run `Llama 3.1 70B` using Groq.

Make sure to set GROQ_API_KEY environment variable to your API key.
"""

from probe import probe

probe.llm.model = "groq/llama-3.1-70b-versatile"

probe.computer.import_computer_api = True

probe.llm.supports_functions = False
probe.llm.supports_vision = False
probe.llm.context_window = 110000
probe.llm.max_tokens = 4096
