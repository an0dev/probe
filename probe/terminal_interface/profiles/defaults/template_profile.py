"""
This is the template Probe profile.

A starting point for creating a new profile.

Learn about all the available settings - https://github.com/an0dev/probe/settings/all-settings

"""

# Import the probe
from probe import probe

# You can import other libraries too
from datetime import date

# You can set variables
today = date.today()

# LLM Settings
probe.llm.model = "groq/llama-3.1-70b-versatile"
probe.llm.context_window = 110000
probe.llm.max_tokens = 4096
probe.llm.api_base = "https://api.example.com"
probe.llm.api_key = "your_api_key_here"
probe.llm.supports_functions = False
probe.llm.supports_vision = False


# Probe Settings
probe.offline = False
probe.loop = True
probe.auto_run = False

# Toggle OS Mode - https://github.com/an0dev/probe/guides/os-mode
probe.os = False

# Import Computer API - https://github.com/an0dev/probe/code-execution/computer-api
probe.computer.import_computer_api = True


# Set Custom Instructions to improve your Probe's performance at a given task
probe.custom_instructions = f"""
    Today's date is {today}.
    """
