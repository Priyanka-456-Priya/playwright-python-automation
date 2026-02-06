"""
Environment Manager Script
Manages switching between different test environments (devtr, qa, staging, prod)
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Available environments
ENVIRONMENTS = {
    'devtr': {
        'name': 'Development/Test (Devtr)',
        'file': '.env.devtr',
        'url': 'https://devtr-api-iscrum.sureprep.com',
        'color': 'green'
    },
    'qa': {
        'name': 'Quality Assurance (QA)',
        'file': '.env.qa',
        'url': 'https://qa-api-iscrum.sureprep.com',
        'color': 'blue'
    },
    'staging': {
        'name': 'Staging (Pre-Production)',
        'file': '.env.staging',
        'url': 'https://staging-api-iscrum.sureprep.com',
        'color': 'yellow'
    },
    'prod': {
        'name': 'Production',
        'file': '.env.prod',
        'url': 'https://api-iscrum.sureprep.com',
        'color': 'red'
    }
}


def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_environment_info(env_key):
    """Print information about an environment"""
    env = ENVIRONMENTS[env_key]
    print(f"\n  [{env_key.upper()}] {env['name']}")
    print(f"  URL: {env['url']}")
    print(f"  Config File: {env['file']}")


def get_current_environment():
    """Get the currently active environment"""
    env_file = PROJECT_ROOT / '.env'
    if not env_file.exists():
        return None

    # Read the TEST_ENVIRONMENT value from .env
    try:
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('TEST_ENVIRONMENT='):
                    return line.split('=')[1].strip().lower()
    except Exception:
        pass

    return None


def list_environments():
    """List all available environments"""
    print_header("Available Test Environments")

    current_env = get_current_environment()

    for env_key, env_info in ENVIRONMENTS.items():
        env_file = PROJECT_ROOT / env_info['file']
        status = "[ACTIVE]" if env_key == current_env else "        "
        exists = "[CONFIGURED]" if env_file.exists() else "[NOT CONFIGURED]"

        print(f"\n{status} {env_key.upper():<10} {exists}")
        print(f"         Name: {env_info['name']}")
        print(f"         URL:  {env_info['url']}")
        print(f"         File: {env_info['file']}")

    if current_env:
        print(f"\n  Currently active environment: {current_env.upper()}")
    else:
        print("\n  No environment currently active (.env file not found)")


def switch_environment(target_env):
    """Switch to a different environment"""
    if target_env not in ENVIRONMENTS:
        print(f"\n[ERROR] Invalid environment: {target_env}")
        print(f"Available environments: {', '.join(ENVIRONMENTS.keys())}")
        return False

    env_info = ENVIRONMENTS[target_env]
    source_file = PROJECT_ROOT / env_info['file']
    target_file = PROJECT_ROOT / '.env'

    # Check if source environment file exists
    if not source_file.exists():
        print(f"\n[ERROR] Environment file not found: {env_info['file']}")
        print(f"Please create this file with the appropriate credentials.")
        return False

    # Backup current .env if it exists
    if target_file.exists():
        backup_file = PROJECT_ROOT / f'.env.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        shutil.copy2(target_file, backup_file)
        print(f"\n[BACKUP] Current .env backed up to: {backup_file.name}")

    # Copy environment file to .env
    try:
        shutil.copy2(source_file, target_file)
        print(f"\n[SUCCESS] Switched to {env_info['name']} environment")
        print(f"  Environment: {target_env.upper()}")
        print(f"  Base URL: {env_info['url']}")
        print(f"  Config File: {env_info['file']}")
        return True
    except Exception as e:
        print(f"\n[ERROR] Failed to switch environment: {str(e)}")
        return False


def verify_environment(env_key):
    """Verify if an environment is properly configured"""
    if env_key not in ENVIRONMENTS:
        print(f"\n[ERROR] Invalid environment: {env_key}")
        return False

    env_info = ENVIRONMENTS[env_key]
    env_file = PROJECT_ROOT / env_info['file']

    print_header(f"Verifying {env_info['name']} Configuration")

    if not env_file.exists():
        print(f"\n[ERROR] Configuration file not found: {env_info['file']}")
        return False

    # Check for required variables
    required_vars = [
        'SUREPREP_BASE_URL',
        'SUREPREP_V5_USERNAME',
        'SUREPREP_V5_PASSWORD',
        'SUREPREP_V5_API_KEY',
        'SUREPREP_V7_CLIENT_ID',
        'SUREPREP_V7_CLIENT_SECRET'
    ]

    found_vars = {}
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    if key in required_vars:
                        found_vars[key] = value.strip()
    except Exception as e:
        print(f"\n[ERROR] Failed to read configuration: {str(e)}")
        return False

    # Check each required variable
    all_configured = True
    print(f"\nConfiguration Status:")
    for var in required_vars:
        if var in found_vars and found_vars[var] and not found_vars[var].startswith('your_'):
            print(f"  [OK] {var}")
        else:
            print(f"  [MISSING] {var}")
            all_configured = False

    if all_configured:
        print(f"\n[SUCCESS] Environment is properly configured!")
        return True
    else:
        print(f"\n[WARNING] Some credentials are missing or use placeholder values")
        return False


def show_usage():
    """Display usage information"""
    print_header("Environment Manager - Usage")
    print("""
Usage: python env_manager.py [command] [environment]

Commands:
  list              List all available environments and their status
  switch <env>      Switch to specified environment (devtr/qa/staging/prod)
  verify <env>      Verify environment configuration
  current           Show currently active environment

Examples:
  python env_manager.py list
  python env_manager.py switch devtr
  python env_manager.py switch qa
  python env_manager.py verify staging
  python env_manager.py current

Environments:
  devtr      - Development/Test environment
  qa         - Quality Assurance environment
  staging    - Staging/Pre-Production environment
  prod       - Production environment
    """)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_usage()
        return

    command = sys.argv[1].lower()

    if command == 'list':
        list_environments()

    elif command == 'current':
        current_env = get_current_environment()
        if current_env:
            print(f"\nCurrently active environment: {current_env.upper()}")
            print_environment_info(current_env)
        else:
            print("\nNo environment currently active (.env file not found)")

    elif command == 'switch':
        if len(sys.argv) < 3:
            print("\n[ERROR] Please specify an environment to switch to")
            print("Usage: python env_manager.py switch <environment>")
            print(f"Available: {', '.join(ENVIRONMENTS.keys())}")
            return

        target_env = sys.argv[2].lower()
        success = switch_environment(target_env)

        if success:
            print("\n[INFO] You can now run tests with: pytest")
            print("[INFO] Or verify authentication with: python verify_auth.py")

    elif command == 'verify':
        if len(sys.argv) < 3:
            print("\n[ERROR] Please specify an environment to verify")
            print("Usage: python env_manager.py verify <environment>")
            print(f"Available: {', '.join(ENVIRONMENTS.keys())}")
            return

        target_env = sys.argv[2].lower()
        verify_environment(target_env)

    elif command in ['help', '-h', '--help']:
        show_usage()

    else:
        print(f"\n[ERROR] Unknown command: {command}")
        show_usage()


if __name__ == "__main__":
    main()
