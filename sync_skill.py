#!/usr/bin/env python3
"""
Sync script to update the GitHub Pages deployment skill from project folder
to the actual Claude Code skill installation directory.

This script copies modified skill files from the project to the skill directory
and optionally repackages the skill.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


def get_paths():
    """Get source and destination paths."""
    # Current project directory
    project_dir = Path(__file__).parent.absolute()

    # Source skill directory in project
    source_skill = project_dir / "github-pages-deploy-skill"

    # Destination: Claude Code skill installation directory
    dest_skill = Path.home() / ".claude" / "plugins" / "cache" / \
                 "anthropic-agent-skills" / "example-skills" / \
                 "a5bcdd7e58cd" / "skills" / "github-pages-deploy"

    # Skills directory (for packaging)
    skills_dir = dest_skill.parent

    return project_dir, source_skill, dest_skill, skills_dir


def backup_skill(dest_skill):
    """Create a backup of the existing skill before overwriting."""
    if not dest_skill.exists():
        print("[INFO] No existing skill found, skipping backup")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = dest_skill.parent / f"{dest_skill.name}_backup_{timestamp}"

    try:
        shutil.copytree(dest_skill, backup_path)
        print(f"[OK] Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"[ERROR] Failed to create backup: {e}")
        return None


def sync_skill_files(source_skill, dest_skill):
    """Sync skill files from source to destination."""
    if not source_skill.exists():
        print(f"[ERROR] Source skill directory not found: {source_skill}")
        return False

    # Create destination directory if it doesn't exist
    dest_skill.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing destination directory
    if dest_skill.exists():
        print(f"[INFO] Removing existing skill directory: {dest_skill}")
        shutil.rmtree(dest_skill)

    # Copy entire skill directory
    try:
        shutil.copytree(source_skill, dest_skill)
        print(f"[OK] Synced skill files from {source_skill}")
        print(f"[OK] To {dest_skill}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to sync skill files: {e}")
        return False


def package_skill(skills_dir, dest_skill):
    """Package the skill into a .skill file."""
    try:
        # Remove old package if exists
        old_package = skills_dir / "github-pages-deploy.skill"
        if old_package.exists():
            old_package.unlink()
            print(f"[INFO] Removed old package: {old_package}")

        # Create new package using tar
        package_path = skills_dir / "github-pages-deploy.skill"

        # Change to skill directory for packaging
        import tarfile
        import tempfile

        # Create a temporary tar file
        with tarfile.open(package_path, "w") as tar:
            for item in dest_skill.rglob("*"):
                if item.is_file():
                    arcname = item.relative_to(dest_skill.parent / "github-pages-deploy")
                    tar.add(item, arcname=arcname)

        print(f"[OK] Packaged skill to: {package_path}")

        # Show file size
        size_kb = package_path.stat().st_size / 1024
        print(f"[OK] Package size: {size_kb:.1f} KB")

        return True
    except Exception as e:
        print(f"[ERROR] Failed to package skill: {e}")
        return False


def update_project_package(project_dir, skills_dir):
    """Update the .skill file in the project directory."""
    source_package = skills_dir / "github-pages-deploy.skill"
    dest_package = project_dir / "github-pages-deploy.skill"

    if not source_package.exists():
        print(f"[WARNING] Package not found: {source_package}")
        return False

    try:
        shutil.copy2(source_package, dest_package)
        print(f"[OK] Updated project package: {dest_package}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to update project package: {e}")
        return False


def show_summary(source_skill, dest_skill, success, packaged=False, updated_project=False):
    """Show sync summary."""
    print("\n" + "=" * 60)
    print("SYNC SUMMARY")
    print("=" * 60)
    print(f"Source:      {source_skill}")
    print(f"Destination: {dest_skill}")
    print(f"Status:      {'SUCCESS' if success else 'FAILED'}")
    if packaged:
        print(f"Packaged:    YES")
    if updated_project:
        print(f"Project:     UPDATED")
    print("=" * 60)


def main():
    """Main sync function."""
    print("\n" + "=" * 60)
    print("GitHub Pages Deployment Skill - Sync Tool")
    print("=" * 60 + "\n")

    # Get paths
    project_dir, source_skill, dest_skill, skills_dir = get_paths()

    print(f"Project directory: {project_dir}")
    print(f"Source skill:      {source_skill}")
    print(f"Destination:       {dest_skill}\n")

    # Check if source exists
    if not source_skill.exists():
        print("[ERROR] Source skill directory not found!")
        print("[ERROR] Make sure 'github-pages-deploy-skill' folder exists in your project.")
        sys.exit(1)

    # Ask for confirmation
    print("[WARNING] This will overwrite the installed skill with your project version.")
    print("[INFO] A backup will be created automatically.\n")

    response = input("Continue? (y/n): ").strip().lower()
    if response not in ['y', 'yes']:
        print("[INFO] Sync cancelled.")
        sys.exit(0)

    # Step 1: Backup existing skill
    print("\n[STEP 1] Creating backup...")
    backup = backup_skill(dest_skill)

    # Step 2: Sync skill files
    print("\n[STEP 2] Syncing skill files...")
    success = sync_skill_files(source_skill, dest_skill)

    if not success:
        print("\n[ERROR] Sync failed! Please check the error messages above.")
        sys.exit(1)

    # Step 3: Package skill
    print("\n[STEP 3] Packaging skill...")
    packaged = package_skill(skills_dir, dest_skill)

    # Step 4: Update project package
    print("\n[STEP 4] Updating project package...")
    updated_project = False
    if packaged:
        updated_project = update_project_package(project_dir, skills_dir)

    # Show summary
    show_summary(source_skill, dest_skill, success, packaged, updated_project)

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
