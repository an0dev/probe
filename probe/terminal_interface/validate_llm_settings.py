import os
import subprocess
import time

os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
import litellm
from prompt_toolkit import prompt

from probe.terminal_interface.contributing_conversations import (
    contribute_conversation_launch_logic,
)
from probe.core.utils import api_key_validation


def validate_llm_settings(probe):
    """
    Interactively prompt the user for required LLM settings
    """

    # This runs in a while loop so `continue` lets us start from the top
    # after changing settings (like switching to/from local)
    while True:
        if probe.offline:
            # We have already displayed a message.
            # (This strange behavior makes me think validate_llm_settings needs to be rethought / refactored)
            break

        else:
            # Ensure API keys are set as environment variables

            # OpenAI
            if probe.llm.model in [
                "gpt-4",
                "gpt-3.5-turbo",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4-turbo",
            ]:
                if (
                    not os.environ.get("OPENAI_API_KEY")
                    and not probe.llm.api_key
                    and not probe.llm.api_base
                ):
                    display_welcome_message_once(probe)

                    probe.display_message(
                        """---
                    > OpenAI API key not found

                    To use `gpt-4o` (recommended) please provide an OpenAI API key.

                    To use another language model, run `probe --local` or consult the documentation at [GitHub docs](https://github.com/an0dev/probe/tree/main/docs/language-models/).
                    
                    ---
                    """
                    )

                    # Use centralized API key validation flow
                    try:
                        api_key = api_key_validation.validate_api_key_interactive(
                            provider="openai",
                            max_attempts=3,
                            display_message_func=probe.display_message,
                            show_setup_instructions=True,
                        )
                    except (KeyboardInterrupt, EOFError):
                        raise
                    except Exception:
                        api_key = None

                    if api_key == "probe --local":
                        print("\nType `probe --local` again to use a local language model.\n")
                        exit()

                    if api_key:
                        probe.display_message(
                            """

                    **Tip:** To save this key for later, run one of the following and then restart your terminal. 
                    MacOS: `echo 'export OPENAI_API_KEY=your_api_key' >> ~/.zshrc`
                    Linux: `echo 'export OPENAI_API_KEY=your_api_key' >> ~/.bashrc`
                    Windows: `setx OPENAI_API_KEY your_api_key`
                    
                    ---"""
                        )
                        probe.llm.api_key = api_key
                        time.sleep(1)
                        break
                    else:
                        # No valid key obtained, show instructions and continue the loop so user can try again
                        probe.display_message("No valid OpenAI API key provided.")
                        time.sleep(0.5)
                        # continue the while loop to allow retry

            # This is a model we don't have checks for yet.
            break

    # If we're here, we passed all the checks.

    # Auto-run is for fast, light usage -- no messages.
    # If offline, it's usually a bogus model name for LiteLLM since LM Studio doesn't require one.
    # If (len(probe.messages) == 1), they probably used the advanced "i {command}" entry, so no message should be displayed.
    if (
        not probe.auto_run
        and not probe.offline
        and not (len(probe.messages) == 1)
    ):
        probe.display_message(f"> Model set to `{probe.llm.model}`")
    if len(probe.messages) == 1:
        # Special message for "i {command}" usage
        # probe.display_message(f"\n*{probe.llm.model} via Probe:*")
        pass

    if probe.llm.model == "i":
        probe.display_message(
            "***Note:*** *Conversations with this model will be used to train our open-source model.*\n"
        )
    if "ollama" in probe.llm.model:
        probe.llm.load()
    return


def display_welcome_message_once(probe):
    """
    Displays a welcome message only on its first call.

    (Uses an internal attribute `_displayed` to track its state.)
    """
    if not hasattr(display_welcome_message_once, "_displayed"):
        probe.display_message(
            """
        ●

        Welcome **Prober**.
        """
        )
        time.sleep(1)

        display_welcome_message_once._displayed = True
