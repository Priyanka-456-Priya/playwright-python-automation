"""
Run tests specifically for Devtr environment
This script ensures tests only run in Devtr environment with proper setup
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Project root
PROJECT_ROOT = Path(__file__).parent

def check_environment():
    """Check if Devtr environment is active"""
    env_file = PROJECT_ROOT / '.env'

    if not env_file.exists():
        print("\n[ERROR] No .env file found!")
        print("Switching to Devtr environment...")
        return False

    load_dotenv(env_file)
    current_env = os.getenv('TEST_ENVIRONMENT', '').lower()

    if current_env != 'devtr':
        print(f"\n[WARNING] Current environment is '{current_env}', not 'devtr'")
        return False

    return True

def switch_to_devtr():
    """Switch to Devtr environment"""
    print("\n[INFO] Switching to Devtr environment...")
    result = subprocess.run(
        ['python', 'env_manager.py', 'switch', 'devtr'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"\n[ERROR] Failed to switch to Devtr environment")
        print(result.stderr)
        sys.exit(1)

    print("[SUCCESS] Switched to Devtr environment")

def verify_authentication():
    """Verify authentication for Devtr"""
    print("\n[INFO] Verifying Devtr authentication...")
    result = subprocess.run(
        ['python', 'verify_auth.py'],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0 or 'FAILED' in result.stdout:
        print("\n[ERROR] Authentication verification failed!")
        sys.exit(1)

    print("[SUCCESS] Authentication verified")

def run_tests(pytest_args=None):
    """Run pytest with specified arguments"""
    print("\n[INFO] Running tests in Devtr environment...")
    print("="*70)

    cmd = ['pytest']

    # Add user-provided pytest arguments
    if pytest_args:
        cmd.extend(pytest_args)
    else:
        # Default arguments
        cmd.extend(['-v', '--tb=short'])

    # Run pytest
    result = subprocess.run(cmd)

    return result.returncode

def main():
    """Main execution"""
    print("="*70)
    print("  Devtr Environment Test Runner")
    print("="*70)

    # Check if Devtr is active
    if not check_environment():
        switch_to_devtr()
    else:
        print("\n[INFO] Devtr environment is active")

    # Verify authentication
    verify_authentication()

    # Get pytest arguments from command line
    pytest_args = sys.argv[1:] if len(sys.argv) > 1 else None

    # Run tests
    exit_code = run_tests(pytest_args)

    # Print summary
    print("\n" + "="*70)
    if exit_code == 0:
        print("  [SUCCESS] All Devtr tests passed!")
    else:
        print("  [FAILED] Some tests failed")
    print("="*70)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
