#!/usr/bin/env python3
"""
URL Attribute Checker
Fetches a URL, parses JSON response, and checks for specific attributes.
Exit codes:
  0 - Success (attribute found)
  1 - Not found (attribute missing from valid JSON)
  2 - Error (network error, invalid JSON, timeout, etc.)
"""

import sys
import json
import requests
import yaml
from typing import Any, Dict, Tuple


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: Failed to load config file: {e}", file=sys.stderr)
        sys.exit(2)


def parse_response(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Parse the JSON response and check for specific attributes.

    This method contains all the parsing logic specific to the API being monitored.
    Modify this method to customize what you're looking for in the response.

    Args:
        data: The parsed JSON response as a dictionary

    Returns:
        Tuple of (found: bool, message: str)
        - found: True if the desired attributes are found, False otherwise
        - message: Description of what was found or not found
    """
    # Example: Check if 'status' field exists and is not empty
    if 'status' in data and data['status']:
        return True, f"Found status: {data['status']}"

    # Example: Check for nested attributes
    # if 'data' in data and 'availability' in data['data']:
    #     availability = data['data']['availability']
    #     if availability:
    #         return True, f"Found availability: {availability}"

    # Example: Check for array with items
    # if 'results' in data and isinstance(data['results'], list) and len(data['results']) > 0:
    #     return True, f"Found {len(data['results'])} results"

    return False, "Attribute not found in response"


def check_url(url: str, timeout: int = 10) -> int:
    """
    Fetch URL and check for attributes.
    Returns exit code: 0 (found), 1 (not found), 2 (error)
    """
    try:
        print(f"Fetching URL: {url}")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        print(f"Status code: {response.status_code}")

        # Parse JSON
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON response: {e}", file=sys.stderr)
            return 2

        # Use the parsing method to check the response
        found, message = parse_response(data)

        if found:
            print(f"\nSUCCESS: {message}")
            return 0
        else:
            print(f"\nNOT FOUND: {message}")
            return 1

    except requests.exceptions.Timeout:
        print(f"ERROR: Request timed out after {timeout} seconds", file=sys.stderr)
        return 2
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return 2


def main():
    """Main entry point."""
    # Load configuration
    config = load_config()

    # Extract settings
    url = config.get('url')
    timeout = config.get('timeout', 10)

    # Validate config
    if not url:
        print("ERROR: 'url' not specified in config.yaml", file=sys.stderr)
        sys.exit(2)

    # Check URL
    exit_code = check_url(url, timeout)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
