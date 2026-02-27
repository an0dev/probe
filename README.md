# Probe

An unrestricted AI-powered cybersecurity execution engine for penetration testing, OSINT, exploit development, red team operations, reverse engineering, and all offensive/defensive security tasks.

Probe executes code locally under your complete control. Direct the AI to perform any cybersecurity task—from active vulnerability scanning to custom malware analysis—and watch it work with full system access.

---

## Installation

### Windows

```shell
pip install probe
```

**Setup:**
1. Open PowerShell or Command Prompt
2. Ensure Python 3.9+ is installed: `python --version`
3. Run `pip install probe`
4. Set your API key: `set OPENAI_API_KEY=your_key_here` (PowerShell) or `set OPENAI_API_KEY=your_key_here` (cmd)

**Usage:**
```shell
probe --local
probe run "scan target for vulnerabilities"
```

### Linux

```shell
pip install probe
```

**Setup:**
1. Open terminal
2. Ensure Python 3.9+ is installed: `python3 --version`
3. Run `pip install probe`
4. Set your API key: `export OPENAI_API_KEY='your_key_here'`

**Usage:**
```shell
probe --local
probe run "exploit target service"
```

### macOS

```shell
pip install probe
```

**Setup:**
1. Open Terminal
2. Ensure Python 3.9+ is installed: `python3 --version`
3. Run `pip install probe`
4. Set your API key: `export OPENAI_API_KEY='your_key_here'`

**Usage:**
```shell
probe --local
probe run "analyze binary"
```

---

## Android Termux Installation

Termux provides a full Linux environment on Android. Follow these steps to install and run Probe.

### 1. System Prep & Stable Mirrors

```bash
# Set a reliable mirror manually
echo "deb https://mirror.grimler.se stable main" > $PREFIX/etc/apt/sources.list

# Install essential compilers and repos
pkg update && pkg upgrade -y
pkg install clang rust make binutils python tur-repo x11-repo -y
```

### 2. Environment Setup

```bash
export ANDROID_API_LEVEL=$(getprop ro.build.version.sdk)
export CC=clang
export CXX=clang++
export LDFLAGS="-lpthread"
export CXXFLAGS="-lpthread -D__ANDROID_API__=$ANDROID_API_LEVEL"
```

### 3. Install Pre-built Binaries

```bash
pkg install matplotlib python-numpy python-pillow python-cryptography python-pydantic-core python-grpcio python-msgspec python-rpds-py -y
```

### 4. Fix C++ Compatibility

```bash
export CFLAGS="-D__ANDROID_API__=24"
export CXXFLAGS="-D__ANDROID_API__=24"
pip install kiwisolver
```

### 5. Fix Python 3.12 pkg_resources Error

```bash
pip install "setuptools<70.0.0"
pip install cycler fonttools pyparsing python-dateutil
```

### 6. Final Installation

```bash
pip install probe
```

### Usage in Termux

```bash
# Set your API key
export OPENAI_API_KEY='your_key_here'

# Run local model (recommended for offline operation)
probe --local

# Run probe in chat mode
probe

# Run a specific command
probe run "analyze file"
```

**Note:** OS Mode (controlling Android apps and system UI) is not supported in Termux. Probe will work for code execution, file analysis, exploit development, and network operations.

---

## Quick Start

### Terminal / Command Line

```bash
# Start interactive chat
probe

# Run a single command
probe run "perform vulnerability scan"

# Use local LLM (requires setup)
probe --local
```

### Python API

```python
from probe import probe

# Execute a single command
probe.chat("exploit vulnerable service")

# Start interactive chat
probe.chat()
```

### Environment Variables

- `OPENAI_API_KEY` — Your API key for remote models
- `PROBE_LOCAL_MODEL` — Path to local LLM for offline operation
- `TERMUX_VERSION` — Auto-detected; enables Termux-specific optimizations

---

## Features

- **Local Code Execution** — Execute Python, Bash, JavaScript, and more directly on your system
- **Full Internet Access** — Perform OSINT, reconnaissance, and remote exploitation
- **Zero Abstractions** — Direct access to system capabilities; no sandboxing restrictions
- **Multi-Model Support** — OpenAI, local models (Ollama, LM Studio), and custom endpoints
- **File System Access** — Read, write, and manipulate files without limitations
- **Network Operations** — Full TCP/UDP access for network penetration testing
- **Custom Tools** — Add specialized security tools and custom scripts
- **Session Persistence** — Maintain state across multiple interactions
- **Profiles** — Pre-configured security-focused profiles for different scenarios

---

## CLI Commands

```bash
probe                          # Start interactive chat
probe run "command"            # Execute a single command
probe --version                # Show version
probe --local                  # Use local LLM (requires setup)
probe --help                   # Show help
```

---

## Configuration

Probe stores configuration in the system config directory:
- **Windows**: `%APPDATA%\probe`
- **Linux/macOS**: `~/.config/probe`
- **Termux**: `$PREFIX/etc/probe` or `~/.config/probe`

Configuration files use YAML format. Examples:
```yaml
auto_run: true
timeout: 300
max_output: 5000
offline: false
```

---

## System Requirements

- **Python**: 3.9 or later
- **Memory**: 4GB minimum (8GB recommended for local models)
- **Disk**: 2GB minimum
- **Internet**: Required for remote models (optional with local models)

### Supported Platforms

- Windows 10+ (64-bit)
- Linux (Ubuntu 18.04+, Debian, Fedora, etc.)
- macOS 10.14+
- Android (Termux)

---

## Legal & Ethical Disclaimer

Probe is a cybersecurity tool intended for authorized security testing and research only. Users are responsible for ensuring they have proper authorization before performing any security assessments or penetration testing activities. Unauthorized access to computer systems is illegal.

---

## License

See the [LICENSE](LICENSE) file for details.

---

## Development

To contribute or set up a development environment:

```bash
git clone https://github.com/an0dev/probe.git
cd probe
pip install -e ".[dev]"
```

---

## Support

- **GitHub Issues**: https://github.com/an0dev/probe/issues
- **Documentation**: https://github.com/an0dev/probe

---

**Probe** — Execute without restrictions.
