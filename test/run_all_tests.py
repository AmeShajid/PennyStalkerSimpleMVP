"""
Master test runner - Runs all tests for the PennyStalker project
This script discovers and runs all test files
"""

import sys
import os
import subprocess

# Get the tests directory
tests_dir = os.path.dirname(os.path.abspath(__file__))
test_files = [
    'test_hash_utils.py',
    'test_display.py',
    'test_database.py'
]

def run_test_file(test_file):
    """Run a single test file and return success status"""
    filepath = os.path.join(tests_dir, test_file)
    
    if not os.path.exists(filepath):
        print(f"✗ {test_file} not found at {filepath}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Running {test_file}...")
    print(f"{'='*60}\n")
    
    result = subprocess.run(
        [sys.executable, filepath],
        cwd=tests_dir,
        capture_output=False
    )
    
    return result.returncode == 0


def main():
    """Run all test files"""
    print("\n" + "="*60)
    print("PENNYSTALKER - MASTER TEST SUITE")
    print("="*60)
    
    results = {}
    
    for test_file in test_files:
        try:
            success = run_test_file(test_file)
            results[test_file] = success
        except Exception as e:
            print(f"✗ Error running {test_file}: {e}")
            results[test_file] = False
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    failed_tests = total_tests - passed_tests
    
    for test_file, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{test_file}: {status}")
    
    print("\n" + "-"*60)
    print(f"Total: {passed_tests}/{total_tests} test files passed")
    print("-"*60 + "\n")
    
    # Return success only if all tests passed
    return 0 if failed_tests == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)