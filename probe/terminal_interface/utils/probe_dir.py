import os
import platformdirs

# Auto-detect Termux environment
IS_TERMUX = bool(os.environ.get("TERMUX_VERSION") or os.path.exists("/data/data/com.termux"))

if IS_TERMUX:
    # Use Termux-specific config directory if PREFIX is set
    prefix = os.environ.get("PREFIX") or "/data/data/com.termux/files/usr"
    probe_dir = os.path.join(prefix, "etc", "probe")
else:
    probe_dir = platformdirs.user_config_dir("probe")

# Ensure directory exists
try:
    os.makedirs(probe_dir, exist_ok=True)
except Exception:
    pass
