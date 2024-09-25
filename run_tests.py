import unittest
import sys
import os

def run_tests():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the project root to sys.path
    sys.path.insert(0, script_dir)

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(script_dir, 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\nTest Summary:")
    print(f"Ran {result.testsRun} tests")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    # Return non-zero exit code if there were failures or errors
    return len(result.failures) + len(result.errors)

if __name__ == '__main__':
    sys.exit(run_tests())