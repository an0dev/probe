from importlib.metadata import version, PackageNotFoundError
import requests



def check_for_update():
    # Fetch the latest version from the PyPI API
    response = requests.get(f"https://pypi.org/pypi/probe/json")
    latest_version = response.json()["info"]["version"]

    # Get the current version using importlib.metadata
    current_version = version("probe")

    return latest_version > current_version
