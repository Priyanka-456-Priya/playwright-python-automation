"""
Test Suite Runner for DEVTR Environment
Automatically switches to devtr environment and runs the full test suite
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Environment configuration
ENVIRONMENT = 'devtr'
ENV_NAME = 'Development/Test (Devtr)'
ENV_FILE = '.env.devtr'
ENV_URL = 'https://devtr-api-iscrum.sureprep.com'


def print_banner(message, char='='):
    """Print formatted banner"""
    print(f"\n{char*80}")
    print(f"  {message}")
    print(f"{char*80}\n")


def switch_environment():
    """Switch to devtr environment"""
    source_file = PROJECT_ROOT / ENV_FILE
    target_file = PROJECT_ROOT / '.env'

    if not source_file.exists():
        print(f"[ERROR] Environment file not found: {ENV_FILE}")
        print("Please create the environment configuration file first.")
        return False

    try:
        # Backup current .env if it exists
        if target_file.exists():
            backup_file = PROJECT_ROOT / f'.env.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
            shutil.copy2(target_file, backup_file)
            print(f"[BACKUP] Current .env backed up to: {backup_file.name}")

        # Copy environment file to .env
        shutil.copy2(source_file, target_file)
        print(f"[SUCCESS] Switched to {ENV_NAME} environment")
        print(f"  Environment: {ENVIRONMENT.upper()}")
        print(f"  Base URL: {ENV_URL}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to switch environment: {str(e)}")
        return False


def run_tests():
    """Run pytest with environment-specific configuration"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create reports directory if it doesn't exist
    reports_dir = PROJECT_ROOT / 'reports' / ENVIRONMENT
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Define report paths
    html_report = reports_dir / f'test_report_{ENVIRONMENT}_{timestamp}.html'
    junit_report = reports_dir / f'test_results_{ENVIRONMENT}_{timestamp}.xml'
    log_file = reports_dir / f'test_log_{ENVIRONMENT}_{timestamp}.log'

    print(f"\n[INFO] Starting test execution for {ENV_NAME}")
    print(f"  Test file: tests/test_TY2025_swagger_apis.py")
    print(f"  HTML Report: {html_report}")
    print(f"  JUnit XML: {junit_report}")
    print(f"  Log File: {log_file}")

    # Pytest command with environment-specific reports
    pytest_cmd = [
        'pytest',
        'tests/test_TY2025_swagger_apis.py',
        '-v',  # Verbose output
        '--tb=short',  # Short traceback format
        f'--html={html_report}',
        '--self-contained-html',
        f'--junit-xml={junit_report}',
        '-s',  # Show print statements
    ]

    # Run pytest
    try:
        print_banner(f"RUNNING TESTS - {ENV_NAME}", '=')

        # Run tests and capture output
        with open(log_file, 'w', encoding='utf-8') as log:
            result = subprocess.run(
                pytest_cmd,
                cwd=PROJECT_ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8'
            )

            # Write to log file and print to console
            output = result.stdout
            log.write(output)
            print(output)

        print_banner("TEST EXECUTION COMPLETED", '=')
        print(f"[INFO] Test results saved to: {reports_dir}")
        print(f"[INFO] HTML Report: {html_report.name}")
        print(f"[INFO] JUnit XML: {junit_report.name}")
        print(f"[INFO] Log File: {log_file.name}")

        # Print summary
        if result.returncode == 0:
            print(f"\n[SUCCESS] All tests passed for {ENV_NAME}!")
        else:
            print(f"\n[WARNING] Some tests failed. Check the reports for details.")

        return result.returncode

    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        return 1


def main():
    """Main entry point"""
    print_banner(f"DEVTR Environment Test Suite Runner", '=')
    print(f"  Environment: {ENVIRONMENT.upper()}")
    print(f"  Name: {ENV_NAME}")
    print(f"  URL: {ENV_URL}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 1: Switch environment
    print_banner("Step 1: Switching Environment", '-')
    if not switch_environment():
        print("\n[ABORT] Failed to switch environment. Exiting.")
        return 1

    # Step 2: Run tests
    print_banner("Step 2: Running Tests", '-')
    return_code = run_tests()

    # Final summary
    print_banner("TEST SUITE EXECUTION SUMMARY", '=')
    if return_code == 0:
        print(f"  Status: SUCCESS ✓")
    else:
        print(f"  Status: FAILED ✗")
    print(f"  Environment: {ENVIRONMENT.upper()}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    return return_code


if __name__ == "__main__":
    sys.exit(main())
