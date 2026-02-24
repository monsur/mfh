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
    Parse the Mama's Fish House reservation API response.

    Checks for bookable reservation slots in the response.

    Args:
        data: The parsed JSON response as a dictionary

    Returns:
        Tuple of (found: bool, message: str)
        - found: True if bookable slots are found, False otherwise
        - message: Description of what was found or not found

    Raises:
        ValueError: If status is not 200, indicating an API error
    """
    # Check if status is 200 (success)
    status = data.get('status')
    if status != 200:
        raise ValueError(f"API returned non-200 status: {status}")

    # Navigate to the times array
    # Structure: data.availability.<date>[0].times[]
    try:
        availability_data = data.get('data', {}).get('availability', {})

        # Get the first date's availability (there should only be one)
        if not availability_data:
            return False, "No availability data found"

        # Get the first date key
        dates = list(availability_data.keys())
        if not dates:
            return False, "No dates in availability data"

        first_date = dates[0]
        date_slots = availability_data[first_date]

        if not date_slots or len(date_slots) == 0:
            return False, "No slots for date"

        # Check the times array
        times = date_slots[0].get('times', [])
        if not times:
            return False, "No times array found"

        # Look for any time slot with type "book"
        bookable_times = []
        for time_slot in times:
            if time_slot.get('type') == 'book':
                bookable_times.append(time_slot.get('time', 'Unknown time'))

        if bookable_times:
            return True, f"Found {len(bookable_times)} bookable slot(s): {', '.join(bookable_times[:3])}{'...' if len(bookable_times) > 3 else ''}"
        else:
            return False, "No bookable slots available (only 'request' slots found)"

    except (KeyError, IndexError, TypeError) as e:
        return False, f"Error parsing response structure: {e}"


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
        try:
            found, message = parse_response(data)

            if found:
                print(f"\nSUCCESS: {message}")
                return 0
            else:
                print(f"\nNOT FOUND: {message}")
                return 1
        except ValueError as e:
            # Status was not 200 or other validation error
            print(f"ERROR: {e}", file=sys.stderr)
            return 2

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
