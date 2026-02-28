"""
This is an Probe profile. It configures Probe to run `llama3` using Ollama.

Images sent to the model will be described with `moondream`.
"""

from probe import probe

probe.system_message = """You are an AI assistant that writes markdown code snippets to answer the user's request. You speak very concisely and quickly, you say nothing irrelevant to the user's request. For example:

User: Open the chrome app.
Assistant: On it. 
```python
import webbrowser
webbrowser.open('https://chrome.google.com')
```
User: The code you ran produced no output. Was this expected, or are we finished?
Assistant: No further action is required; the provided snippet opens Chrome.

Now, your turn:""".strip()

# Message templates
probe.code_output_template = '''I executed that code. This was the output: """{content}"""\n\nWhat does this output mean (I can't understand it, please help) / what code needs to be run next (if anything, or are we done)? I can't replace any placeholders.'''
probe.empty_code_output_template = "The code above was executed on my machine. It produced no text output. What's next (if anything, or are we done?)"
probe.code_output_sender = "user"

# LLM settings
probe.llm.model = "ollama/llama3"
probe.llm.supports_functions = False
probe.llm.execution_instructions = False
probe.llm.max_tokens = 1000
probe.llm.context_window = 7000
probe.llm.load()  # Loads Ollama models

# Computer settings
probe.computer.import_computer_api = False

# Misc settings
probe.auto_run = False
probe.offline = True

# Final message
probe.display_message(
    "> Model set to `llama3`\n\n**Probe** will require approval before running code.\n\nUse `probe -y` to bypass this.\n\nPress `CTRL-C` to exit.\n"
)
