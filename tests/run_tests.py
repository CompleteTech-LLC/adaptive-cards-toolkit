#!/usr/bin/env python3
"""Test runner for all agent toolkit tests."""

import unittest
import sys
import os
import argparse

# Ensure we can import from the proper package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


def run_tests(verbosity=1, failfast=False, pattern="test_*.py"):
    """Run all tests.
    
    Args:
        verbosity: Verbosity level (1-3).
        failfast: Whether to stop on first failure.
        pattern: Pattern to match test files.
        
    Returns:
        True if all tests pass, False otherwise.
    """
    # Discover and run tests
    suite = unittest.defaultTestLoader.discover(
        start_dir=os.path.dirname(os.path.abspath(__file__)),
        pattern=pattern
    )
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=verbosity, failfast=failfast)
    result = runner.run(suite)
    
    # Return True if successful, False otherwise
    return result.wasSuccessful()


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run agent toolkit tests")
    parser.add_argument("-v", "--verbosity", type=int, choices=[1, 2, 3], default=2,
                        help="Verbosity level (1-3)")
    parser.add_argument("-f", "--failfast", action="store_true",
                        help="Stop on first failure")
    parser.add_argument("-p", "--pattern", type=str, default="test_*.py",
                        help="Pattern to match test files")
    
    args = parser.parse_args()
    
    # Run tests and set exit code based on success
    success = run_tests(
        verbosity=args.verbosity,
        failfast=args.failfast,
        pattern=args.pattern
    )
    
    sys.exit(0 if success else 1)