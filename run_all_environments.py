"""
Master Test Suite Runner - Run tests across all environments
Executes tests sequentially for: Devtr, QA, Staging, (optional) Production
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Environment test runners
TEST_RUNNERS = {
    'devtr': {
        'name': 'Development/Test (Devtr)',
        'script': 'run_tests_devtr.py',
        'safe': True,
        'required': True
    },
    'qa': {
        'name': 'Quality Assurance (QA)',
        'script': 'run_tests_qa.py',
        'safe': True,
        'required': True
    },
    'staging': {
        'name': 'Staging (Pre-Production)',
        'script': 'run_tests_staging.py',
        'safe': True,
        'required': True
    },
    'prod': {
        'name': 'Production',
        'script': 'run_tests_prod.py',
        'safe': False,
        'required': False
    }
}


def print_banner(message, char='='):
    """Print formatted banner"""
    print(f"\n{char*80}")
    print(f"  {message}")
    print(f"{char*80}\n")


def print_master_header():
    """Print master execution header"""
    print_banner("MULTI-ENVIRONMENT TEST SUITE EXECUTION", '=')
    print(f"  Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total Environments: {len([e for e in TEST_RUNNERS.values() if e['required']])}")
    print(f"  Safe Environments: {len([e for e in TEST_RUNNERS.values() if e['safe']])}")
    print(f"\n  Environments to test:")
    for env_key, env_info in TEST_RUNNERS.items():
        status = "[REQUIRED]" if env_info['required'] else "[OPTIONAL]"
        safety = "[SAFE]" if env_info['safe'] else "[PRODUCTION]"
        print(f"    {status} {safety} {env_key.upper():<10} - {env_info['name']}")
    print(f"{'='*80}\n")


def ask_include_production():
    """Ask if production tests should be included"""
    print_banner("Production Environment Option", '-')
    print("  Do you want to include PRODUCTION environment in this test run?")
    print("  WARNING: This will run tests against production!")
    print("\n  Include Production? (yes/no): ", end='')

    response = input().strip().lower()
    return response in ['yes', 'y']


def run_environment_tests(env_key, env_info):
    """Run tests for a specific environment"""
    script_path = PROJECT_ROOT / env_info['script']

    if not script_path.exists():
        print(f"[ERROR] Test runner not found: {env_info['script']}")
        return False

    print_banner(f"Running {env_info['name']} Tests", '=')
    print(f"  Environment: {env_key.upper()}")
    print(f"  Script: {env_info['script']}")
    print(f"  Safe: {'Yes' if env_info['safe'] else 'No (PRODUCTION)'}")

    try:
        # Run the environment-specific test runner
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_ROOT
        )

        if result.returncode == 0:
            print(f"\n[SUCCESS] {env_info['name']} tests completed successfully")
            return True
        else:
            print(f"\n[WARNING] {env_info['name']} tests completed with failures")
            return False

    except Exception as e:
        print(f"\n[ERROR] Failed to run {env_info['name']} tests: {str(e)}")
        return False


def main():
    """Main entry point"""
    start_time = datetime.now()

    # Print header
    print_master_header()

    # Ask about production
    include_production = ask_include_production()

    # Results tracking
    results = {}
    environments_to_test = []

    # Build list of environments to test
    for env_key, env_info in TEST_RUNNERS.items():
        if env_info['required']:
            environments_to_test.append((env_key, env_info))
        elif env_key == 'prod' and include_production:
            environments_to_test.append((env_key, env_info))

    print(f"\n[INFO] Will test {len(environments_to_test)} environment(s)")

    # Run tests for each environment
    for idx, (env_key, env_info) in enumerate(environments_to_test, 1):
        print_banner(f"Environment {idx}/{len(environments_to_test)}: {env_info['name']}", '=')

        success = run_environment_tests(env_key, env_info)
        results[env_key] = success

        # Brief pause between environments
        if idx < len(environments_to_test):
            print("\n" + "-"*80)
            print("  Preparing next environment...")
            print("-"*80 + "\n")

    # Final summary
    end_time = datetime.now()
    duration = end_time - start_time

    print_banner("MULTI-ENVIRONMENT TEST EXECUTION SUMMARY", '=')
    print(f"  Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total Duration: {duration}")
    print(f"\n  Results by Environment:")

    all_passed = True
    for env_key, success in results.items():
        env_info = TEST_RUNNERS[env_key]
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"    [{env_key.upper():<10}] {env_info['name']:<30} {status}")
        if not success:
            all_passed = False

    print(f"\n  Overall Status: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    print(f"\n  Reports Location:")
    print(f"    reports/devtr/     - Devtr test reports")
    print(f"    reports/qa/        - QA test reports")
    print(f"    reports/staging/   - Staging test reports")
    if include_production:
        print(f"    reports/prod/      - Production test reports")

    print(f"{'='*80}\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[ABORT] Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {str(e)}")
        sys.exit(1)
