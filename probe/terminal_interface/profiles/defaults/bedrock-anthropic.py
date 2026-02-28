"""
This is an Probe profile. It configures Probe to run Anthropic's `Claude 3 Sonnet` using Bedrock.
"""

"""
Recommended pip package:
pip install boto3

Recommended environment variables:
os.environ["AWS_ACCESS_KEY_ID"] = ""  # Access key
os.environ["AWS_SECRET_ACCESS_KEY"] = "" # Secret access key
os.environ["AWS_REGION_NAME"] = "" # us-east-1, us-east-2, us-west-1, us-west-2

More information can be found here: https://docs.litellm.ai/docs/providers/bedrock
"""

from probe import probe

probe.llm.model = "bedrock/anthropic.claude-3-sonnet-20240229-v1:0"

probe.computer.import_computer_api = True

probe.llm.supports_functions = False
probe.llm.supports_vision = False
probe.llm.context_window = 10000
probe.llm.max_tokens = 4096
