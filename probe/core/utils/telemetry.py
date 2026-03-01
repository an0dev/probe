"""
Sends anonymous telemetry to posthog. This helps us know how people are using OI / what needs our focus.

Disable anonymous telemetry by execute one of below:
1. Running `probe --disable_telemetry` in command line.
2. Executing `probe.disable_telemetry = True` in Python.
3. Setting the `DISABLE_TELEMETRY` os var to `true`.

based on ChromaDB's telemetry: https://github.com/chroma-core/chroma/tree/main/chromadb/telemetry/product
"""

import contextlib
import json
import os
import threading
import uuid
import sys

from importlib.metadata import PackageNotFoundError
import requests


def get_or_create_uuid():
    try:
        uuid_file_path = os.path.join(
            os.path.expanduser("~"), ".cache", "probe", "telemetry_user_id"
        )
        os.makedirs(
            os.path.dirname(uuid_file_path), exist_ok=True
        )  # Ensure the directory exists

        if os.path.exists(uuid_file_path):
            with open(uuid_file_path, "r") as file:
                return file.read()
        else:
            new_uuid = str(uuid.uuid4())
            with open(uuid_file_path, "w") as file:
                file.write(new_uuid)
            return new_uuid
    except:
        # Non blocking
        return "idk"


user_id = get_or_create_uuid()


def _get_package_version():
    """
    Try multiple methods to get the package version.
    Returns "unknown" as last resort if all methods fail.
    This function ensures telemetry never crashes due to version detection.
    """
    # Method 1: Try importlib.metadata.version()
    try:
        from importlib.metadata import version
        return version("probe")
    except Exception:
        pass
    
    # Method 2: Try pkg_resources.get_distribution()
    try:
        import pkg_resources
        return pkg_resources.get_distribution("probe").version
    except Exception:
        pass
    
    # Method 3: Try reading package.__version__  
    try:
        import probe
        if hasattr(probe, '__version__'):
            return probe.__version__
    except Exception:
        pass
    
    # Method 4: Try reading VERSION or version.txt files
    try:
        probe_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        version_files = [
            os.path.join(probe_dir, "VERSION"),
            os.path.join(probe_dir, "version.txt"),
            os.path.join(probe_dir, "probe", "VERSION"),
            os.path.join(probe_dir, "probe", "version.txt"),
        ]
        for version_file in version_files:
            if os.path.exists(version_file):
                with open(version_file, 'r') as f:
                    version_str = f.read().strip()
                    if version_str:
                        return version_str
    except Exception:
        pass
    
    # Method 5: Try reading pyproject.toml for version
    try:
        probe_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pyproject_path = os.path.join(probe_dir, "pyproject.toml")
        if os.path.exists(pyproject_path):
            import re
            with open(pyproject_path, 'r') as f:
                content = f.read()
                match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
    except Exception:
        pass
    
    # Last resort: return "unknown"
    return "unknown"


def send_telemetry(event_name, properties=None):
    """
    Send anonymous telemetry event. This function should NEVER raise exceptions
    or crash the application. All errors are silently caught.
    """
    try:
        if properties is None:
            properties = {}
        
        # Get version with multiple fallback methods - this will never raise
        properties["oi_version"] = _get_package_version()
        
        url = "https://app.posthog.com/capture"
        headers = {"Content-Type": "application/json"}
        data = {
            "api_key": "phc_6cmXy4MEbLfNGezqGjuUTY8abLu0sAwtGzZFpQW97lc",
            "event": event_name,
            "properties": properties,
            "distinct_id": user_id,
        }
        requests.post(url, headers=headers, data=json.dumps(data), timeout=2)
    except Exception:
        # Telemetry should NEVER crash the application
        # Silently catch all exceptions
        pass
