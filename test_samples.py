#!/usr/bin/env python3
"""Test script to verify parsing logic with sample files."""

import json
import sys
from check_url import parse_response

def test_sample(filename, expected_exit_code):
    """Test a sample file and verify it returns the expected exit code."""
    print(f"\n{'='*60}")
    print(f"Testing: {filename} (Expected exit code: {expected_exit_code})")
    print('='*60)

    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        try:
            found, message = parse_response(data)
            if found:
                exit_code = 0
                print(f"✓ SUCCESS: {message}")
            else:
                exit_code = 1
                print(f"✗ NOT FOUND: {message}")
        except ValueError as e:
            exit_code = 2
            print(f"✗ ERROR: {e}")

        if exit_code == expected_exit_code:
            print(f"✓ PASS: Got expected exit code {exit_code}")
            return True
        else:
            print(f"✗ FAIL: Expected {expected_exit_code}, got {exit_code}")
            return False

    except Exception as e:
        print(f"✗ FAIL: Exception during test: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Mama's Fish House Reservation Parser")

    tests = [
        ('sample0.json', 0),  # Has "book" type - should succeed
        ('sample1.json', 1),  # Only "request" type - not found
        ('sample2.json', 2),  # Status 400 - error
    ]

    results = []
    for filename, expected in tests:
        results.append(test_sample(filename, expected))

    print(f"\n{'='*60}")
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print('='*60)

    if all(results):
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
