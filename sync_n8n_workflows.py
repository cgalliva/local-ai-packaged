#!/usr/bin/env python3
"""
sync_n8n_workflows.py

This script exports workflows (and optionally credentials) from your running n8n instance
back to the /n8n/backup/ folder so they're saved in your repo.

Usage:
    python sync_n8n_workflows.py                  # Export workflows only
    python sync_n8n_workflows.py --with-credentials  # Export workflows + credentials
"""

import subprocess
import argparse
import sys
import os

def run_command(cmd, cwd=None, capture_output=False):
    """Run a shell command and optionally capture output."""
    print(f"Running: {' '.join(cmd)}")
    try:
        if capture_output:
            result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, cwd=cwd, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if capture_output and e.stderr:
            print(f"Error output: {e.stderr}")
        return None

def check_n8n_running():
    """Check if n8n container is running."""
    print("Checking if n8n container is running...")
    result = run_command(
        ["docker", "ps", "--filter", "name=n8n", "--filter", "status=running", "--format", "{{.Names}}"],
        capture_output=True
    )
    
    if result and "n8n" in result:
        print(f"✓ Found running n8n container: {result}")
        return True
    else:
        print("✗ n8n container is not running!")
        print("  Start it with: python start_services.py --profile none")
        return False

def export_workflows():
    """Export all workflows from n8n to the backup folder."""
    print("\n📥 Exporting workflows from n8n...")
    
    # Export workflows using n8n CLI inside the container
    # The /backup volume is already mounted, so we export directly there
    cmd = [
        "docker", "exec", "n8n",
        "n8n", "export:workflow",
        "--all",
        "--separate",
        "--output=/backup/workflows"
    ]
    
    result = run_command(cmd)
    if result is not None:
        print("✓ Workflows exported successfully to /n8n/backup/workflows/")
        return True
    else:
        print("✗ Failed to export workflows")
        return False

def export_credentials():
    """Export all credentials from n8n to the backup folder."""
    print("\n🔐 Exporting credentials from n8n...")
    print("⚠️  WARNING: Credential files may contain sensitive data!")
    
    cmd = [
        "docker", "exec", "n8n",
        "n8n", "export:credentials",
        "--all",
        "--separate",
        "--output=/backup/credentials"
    ]
    
    result = run_command(cmd)
    if result is not None:
        print("✓ Credentials exported successfully to /n8n/backup/credentials/")
        print("⚠️  Remember: Don't commit sensitive credentials to git!")
        return True
    else:
        print("✗ Failed to export credentials")
        return False

def list_exported_files():
    """List the exported workflow files."""
    print("\n📋 Exported files:")
    workflows_path = "n8n/backup/workflows"
    
    if os.path.exists(workflows_path):
        workflow_files = [f for f in os.listdir(workflows_path) if f.endswith('.json')]
        if workflow_files:
            print(f"\n  Workflows ({len(workflow_files)}):")
            for f in sorted(workflow_files):
                print(f"    - {f}")
        else:
            print("  No workflow files found")
    
    credentials_path = "n8n/backup/credentials"
    if os.path.exists(credentials_path):
        cred_files = [f for f in os.listdir(credentials_path) if f.endswith('.json')]
        if cred_files:
            print(f"\n  Credentials ({len(cred_files)}):")
            for f in sorted(cred_files):
                print(f"    - {f}")

def main():
    parser = argparse.ArgumentParser(
        description='Export n8n workflows and credentials back to your repo.'
    )
    parser.add_argument(
        '--with-credentials',
        action='store_true',
        help='Also export credentials (use with caution - may contain sensitive data)'
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("N8N Workflow Sync Script")
    print("=" * 60)
    
    # Check if n8n is running
    if not check_n8n_running():
        sys.exit(1)
    
    # Export workflows
    success = export_workflows()
    
    # Export credentials if requested
    if args.with_credentials:
        cred_success = export_credentials()
        success = success and cred_success
    
    # List exported files
    list_exported_files()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ Sync completed successfully!")
        print("\n💡 Next steps:")
        print("  1. Review the exported files in /n8n/backup/")
        print("  2. Commit to git: git add n8n/backup/ && git commit -m 'Update workflows'")
        if args.with_credentials:
            print("  3. ⚠️  Check credentials don't contain sensitive data before committing!")
    else:
        print("✗ Sync completed with errors")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()

