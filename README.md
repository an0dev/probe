<p align="center">
  <h1>Probe</h1>

  [![PyPI Version](https://img.shields.io/pypi/v/probers?color=green)](https://pypi.org/project/probers/)
  [![PyPI Downloads](https://img.shields.io/pypi/dm/probers?color=blue)](https://pypi.org/project/probers/)
  [![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
  [![Python Version](https://img.shields.io/pypi/pyversions/probers?color=informational)](https://pypi.org/project/probers/)
  [![GitHub Release](https://img.shields.io/github/v/release/an0dev/probe?color=orange)](https://github.com/an0dev/probe/releases)
  [![Downloads](https://img.shields.io/github/downloads/an0dev/probe/total?color=yellow)](https://github.com/an0dev/probe/releases)
</p>


Probe is an AI-powered cybersecurity execution engine built for penetration testing, vulnerability assessment, red team operations, OSINT, exploit development, reverse engineering, and comprehensive offensive/defensive security workflows. It is designed to operate in both online and completely offline environments, allowing you to run local language models or disconnect from the network when required.

Based on [AIDE CLI](https://github.com/denisidoro/aide) – Leveraging best practices from open-source AI infrastructure.

## Features

Probe exposes a rich set of capabilities aimed at making offensive and defensive security workflows more efficient. The bullets below summarize the core functionality; each item has a corresponding example or detailed explanation later in this README or in the `docs/` directory. Every feature listed here is available from the command line interface, Python API, or by running a local server.

- **Automated Security Testing** – Execute security scans, reconnaissance, and assessments via natural language commands. The agent translates your prompts into actionable tools (nmap, curl, etc.) and aggregates results.

- **Penetration Testing Framework** – Streamline port scanning, service enumeration, and vulnerability research with one-off commands or scripted sessions.

- **Exploit Development** – Generate, test, and refine exploits with interactive LLM guidance; run shelled code snippets, craft PoCs, and debug in tight loops.

- **OSINT & Reconnaissance** – Gather open-source intelligence, enumerate targets, scrape websites, and build attack surface maps entirely from the CLI.

- **Reverse Engineering** – Analyze binaries, decode protocols, and research malware by feeding files or hex dumps into the model and executing helper tools.

- **Lateral Movement & Pivoting** – Simulate post‑exploitation network traversal by automating SSH, SMB, and other toolchains.

- **Offline/Local Mode** – Probe works without an internet connection. Set `--local` to force use of locally hosted or on‑device language models; all logic still executes and code runs against your filesystem in the same way.

- **Multi-LLM Support** – Use OpenAI, local models (Ollama, LLaMA, etc.), or any provider supported by LiteLLM.

- **Cross‑Platform** – Fully supported on Linux, macOS, Windows, and Termux (Android). The Termux guide above explains manual dependency installation.

- **Extensible Language Execution** – Execute code in a variety of languages directly from the chat interface. Supported languages include:

  - Python
  - Shell (bash, sh, zsh)
  - JavaScript/Node.js
  - PowerShell (Windows)
  - Ruby
  - PHP
  - Go (via `go run` if installed)
  - And any interpreter available on the PATH

Each feature is described in more detail throughout this README; refer to the Quick Start and Examples sections for usage patterns.

## Installation

### Prerequisites

Ensure you have Python 3.9+ installed on your system.

### Via PyPI (Recommended)

```shell
pip install probers
```

### From Source

```shell
git clone https://github.com/an0dev/probe.git
# note: package name is prober for pip
cd probe
pip install -e .
```

### Termux / Android (Manual Installation)

Termux install requires some manual steps due to Android toolchain quirks.

## Offline Mode

Probe is designed to function completely offline once installed. The core engine runs entirely in‑process; only the choice of language model may require network access. To operate offline:

- Install a local model or use `--local`: many users run Ollama, LLaMA, or another server on localhost and invoke Probe with `--model` pointing at the local endpoint.

- Disable telemetry and network checks: set `export PROBE_OFFLINE=true` or run `probe --offline` to suppress any outbound traffic. By default Probe only contacts telemetry endpoints if you explicitly opt in.

- Code execution, file analysis, and toolcalls all work without internet; commands like `probe "run python"` or `probe "scan"` still execute on your machine with no external dependencies.

This makes Probe suitable for air‑gapped labs and sensitive environments. Just install the package (or copy the wheel) onto the offline host and run the CLI as usual.

## System Prep & Stable Mirrors

First, ensure you are on a stable mirror and have the necessary build tools:

```bash
# Set a reliable mirror manually
echo "deb https://mirror.grimler.se stable main" > $PREFIX/etc/apt/sources.list

# Install essential compilers and repos
pkg update && pkg upgrade -y
pkg install clang rust make binutils python tur-repo x11-repo -y
```

### Environment "Hand-Holding"

This tells the Rust and C++ compilers exactly how to talk to your Android system:

```bash
export ANDROID_API_LEVEL=$(getprop ro.build.version.sdk)
export CC=clang
export CXX=clang++
export LDFLAGS="-lpthread"
export CXXFLAGS="-lpthread -D__ANDROID_API__=$ANDROID_API_LEVEL"
```

### Install Pre-built Binaries (The Shortcut)

We skipped the failing "metadata generation" by using pre-compiled versions from the Termux User Repository (TUR) and X11 repo:

```bash
pkg install matplotlib python-numpy python-pillow python-cryptography python-pydantic-core python-grpcio python-msgspec python-rpds-py -y
```

### Fix C++ Compatibility (The Kiwisolver Fix)

For packages that still insist on compiling, we force a lower API level to avoid the `pthread_cond_clockwait` error:

```bash
export CFLAGS="-D__ANDROID_API__=24"
export CXXFLAGS="-D__ANDROID_API__=24"
pip install kiwisolver
```

### Fix the Python 3.12 "pkg_resources" Error

Python 3.12 removed a module that some dependencies need. Work around this by downgrading setuptools:

```bash
pip install "setuptools<70.0.0"
pip install cycler fonttools pyparsing python-dateutil
```

### Final Installation & Launch

```bash
pip install probers
```

### How to Use It Now

```bash
# Set your API key
export OPENAI_API_KEY='your_key_here'

# Run local models
probe --local   # to use models without a paid API
```

OS Mode (controlling Android apps) is not currently supported in Termux; stick to code execution and file analysis.

Use all commands with caution when copying from this guide.

(see the Offline Mode section above if you are running without network access; everything except the chosen LLM can operate locally)

## Quick Start

### CLI Usage

```bash
# Start interactive session
probe

# Run with specific model
probe --model gpt-4 --auto-run

# One-off command
probe "Scan 192.168.1.1 for open ports"

# View help
probe --help
```

### OS-specific Package Installation

**Windows**

```bash
pip install probers
# run in cmd or Powershell: probe
```

**Linux / macOS**

```bash
pip install probers
# run: probe
```

**Termux** (see Termux guide above for manual package prep)

```bash
pip install probers
```

### Python API

```python
from probe import probe
# Interactive chat
probe.chat()
# Execute single task
probe.chat("Enumerate services on target.com")
# Custom instance
from probe import Probe
custom = Probe()
custom.llm.model = "gpt-4o"
custom.chat("Perform DNS enumeration on example.com")
```

## Configuration

### LLM Setup

**OpenAI:**

```bash
export OPENAI_API_KEY="sk-..."
probe --model gpt-4o
```

**Local Model (Ollama/LM Studio):**

```bash
# Start your local server first
probe --model openai/llama2 --api-base http://localhost:1234/v1 --api-key fake-key
```

**Other Providers:** Probe uses LiteLLM for multi-provider support. See LiteLLM docs for configuration.

### Profile System

Profiles allow you to save configurations:

```bash
probe --profile custom --model gpt-4
```

Profiles are stored in `~/.config/probe/profiles/` and use YAML format.

## Security & Disclaimers

⚠️ IMPORTANT

Probe is designed for authorized security testing only. Unauthorized access to computer systems is illegal.

- Only use Probe on systems you own or have explicit written permission to test
- Obey all applicable laws and regulations
- Be aware that LLM-generated code may have unintended consequences
- Always review and validate code before execution

## Examples

### Network Reconnaissance

```python
from probe import probe
probe.chat("Scan 10.0.0.0/24 and report open ports")
```

### Vulnerability Research

```python
probe.chat("Research CVE-2024-XXXXX and suggest exploitation approach")
```

### Reverse Engineering

```python
probe.chat("Analyze this binary and identify its functionality")
# (provide binary file or hex dump)
```

### Report Generation

```python
probe.chat("Generate a penetration test report summarizing findings, risks, and remediation steps")
```

## Troubleshooting

### Import Errors

Ensure the package is installed in your Python environment:

```bash
pip list | grep probe
python3 -c "from probe import probe; print('OK')"
```

### API Key Issues

Check that your LLM provider API key is set:

```bash
echo $OPENAI_API_KEY
# for OpenAI
```

### Termux-Specific

Some GUI/audio features may not work in Termux. Text-based functionality is fully supported.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Submit a pull request

## License

GNU Affero General Public License v3.0 (AGPL-3.0) with Additional Restrictions

This software is provided as-is for authorized security testing and educational purposes only.

You are expressly PROHIBITED from:

- Selling, reselling, or commercializing Probe or any derivative work
- Tampering with, modifying, or obscuring copyright notices and author attributions
- Using this software for unauthorized access or illegal activities

See `LICENSE` for full terms.

## Support

- GitHub Issues: Report bugs or request features
- Discussions: Ask questions and share ideas

## Disclaimer

This project is provided for authorized security testing, research, and educational purposes. Users are responsible for ensuring they have proper authorization before testing any system. Unauthorized access is illegal.

The developers are not responsible for misuse or damage caused by this software.

**Project Status:** Active Development
**License:** AGPL-3.0 with restrictions
**Last Updated:** February 2026

