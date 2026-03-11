#!/usr/bin/env python3
"""
Sync script to copy the github-pages-deploy-skill folder to .claude/skills directory.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime


def get_paths():
    """Get source and destination paths."""
    project_dir = Path(__file__).parent.absolute()
    source_folder = project_dir / "github-pages-deploy-skill"
    skills_dir = Path.home() / ".claude" / "skills"
    dest_folder = skills_dir / "github-pages-deploy-skill"

    return project_dir, source_folder, dest_folder, skills_dir


def backup_skill(dest_folder):
    """Create a backup of the existing skill folder before overwriting."""
    if not dest_folder.exists():
        print("[INFO] No existing skill folder found, skipping backup")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = dest_folder.parent / f"{dest_folder.name}_backup_{timestamp}"

    try:
        shutil.copytree(dest_folder, backup_path)
        print(f"[OK] Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"[ERROR] Failed to create backup: {e}")
        return None


def sync_skill_folder(source_folder, dest_folder):
    """Copy skill folder to destination."""
    if not source_folder.exists():
        print(f"[ERROR] Source folder not found: {source_folder}")
        return False

    # Create destination directory if it doesn't exist
    dest_folder.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing destination folder
    if dest_folder.exists():
        print(f"[INFO] Removing existing skill folder: {dest_folder}")
        shutil.rmtree(dest_folder)

    # Copy the folder
    try:
        shutil.copytree(source_folder, dest_folder)
        print(f"[OK] Copied {source_folder}")
        print(f"[OK] To {dest_folder}")

        # Show skill info
        total_size = sum(f.stat().st_size for f in dest_folder.rglob("*") if f.is_file())
        print(f"[OK] Total size: {total_size / 1024:.1f} KB")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to copy skill folder: {e}")
        return False


def show_summary(project_dir, skills_dir, success):
    """Show sync summary."""
    print("\n" + "=" * 60)
    print("SYNC SUMMARY")
    print("=" * 60)
    print(f"Project directory: {project_dir}")
    print(f"Skills directory:  {skills_dir}")
    print(f"Status:            {'SUCCESS' if success else 'FAILED'}")
    print("=" * 60)


def main():
    """Main sync function."""
    print("\n" + "=" * 60)
    print("GitHub Pages Deployment Skill - Sync Tool")
    print("Copying to .claude/skills directory")
    print("=" * 60 + "\n")

    # Get paths
    project_dir, source_folder, dest_folder, skills_dir = get_paths()

    print(f"Project directory: {project_dir}")
    print(f"Source folder:     {source_folder}")
    print(f"Skills directory:  {skills_dir}\n")

    # Check if source exists
    if not source_folder.exists():
        print(f"[ERROR] Source folder not found: {source_folder}")
        sys.exit(1)

    # Ask for confirmation
    print("[WARNING] This will copy skill folder to .claude/skills directory")
    print("[INFO] A backup will be created automatically.\n")

    response = input("Continue? (y/n): ").strip().lower()
    if response not in ['y', 'yes']:
        print("[INFO] Sync cancelled.")
        sys.exit(0)

    # Step 1: Backup existing skill
    print("\n[STEP 1] Creating backup...")
    backup = backup_skill(dest_folder)

    # Step 2: Copy skill folder
    print("\n[STEP 2] Copying skill folder...")
    success = sync_skill_folder(source_folder, dest_folder)

    if not success:
        print("\n[ERROR] Sync failed! Please check the error messages above.")
        sys.exit(1)

    # Show summary
    show_summary(project_dir, skills_dir, success)

    if backup:
        print(f"\n[INFO] Backup saved to: {backup}")
        print("[INFO] You can restore it if something goes wrong.")

    print("\n[NEXT STEPS]")
    print("1. Restart Claude Code to reload the skill")
    print("2. Test the skill by asking: 'deploy to GitHub Pages'")
    print("3. If something is wrong, restore from backup\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Sync cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
