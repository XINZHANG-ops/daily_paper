#!/usr/bin/env python3
"""
Migrate old notes from old_notes/ to the new dailies/ structure.

For each date folder in old_notes/:
1. Move the {date}.md file to dailies/notes/
2. Create a folder in dailies/images/{date}/
3. Move all .png files to dailies/images/{date}/
"""

import os
import shutil
from pathlib import Path
from loguru import logger


def migrate_date_folder(date_folder_path, dry_run=False):
    """
    Migrate a single date folder from old_notes to new structure.

    Args:
        date_folder_path: Path object for the date folder
        dry_run: If True, only show what would be done

    Returns:
        dict: Summary of actions taken
    """
    date_str = date_folder_path.name
    actions = {
        'date': date_str,
        'md_migrated': False,
        'images_migrated': 0,
        'errors': []
    }

    # Expected paths
    md_file_path = date_folder_path / f"{date_str}.md"
    target_md_path = Path('dailies/notes') / f"{date_str}.md"
    target_images_dir = Path('dailies/images') / date_str

    # Check if markdown file exists
    if md_file_path.exists():
        if target_md_path.exists():
            logger.warning(f"{date_str}: Markdown file already exists at {target_md_path}, skipping")
            actions['errors'].append("MD file already exists in target")
        else:
            if dry_run:
                logger.info(f"{date_str}: Would move {md_file_path} -> {target_md_path}")
            else:
                # Ensure target directory exists
                target_md_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(md_file_path), str(target_md_path))
                logger.success(f"{date_str}: Moved markdown file")
            actions['md_migrated'] = True
    else:
        logger.warning(f"{date_str}: No markdown file found at {md_file_path}")
        actions['errors'].append("No MD file found")

    # Find and migrate PNG files
    png_files = list(date_folder_path.glob('*.png'))

    if png_files:
        if dry_run:
            logger.info(f"{date_str}: Would create directory {target_images_dir}")
            for png_file in png_files:
                target_png = target_images_dir / png_file.name
                logger.info(f"{date_str}: Would move {png_file} -> {target_png}")
            actions['images_migrated'] = len(png_files)
        else:
            # Create images directory for this date
            target_images_dir.mkdir(parents=True, exist_ok=True)

            for png_file in png_files:
                target_png = target_images_dir / png_file.name
                if target_png.exists():
                    logger.warning(f"{date_str}: Image {png_file.name} already exists, skipping")
                    actions['errors'].append(f"Image {png_file.name} already exists")
                else:
                    shutil.move(str(png_file), str(target_png))
                    actions['images_migrated'] += 1

            if actions['images_migrated'] > 0:
                logger.success(f"{date_str}: Moved {actions['images_migrated']} image(s)")

    return actions


def main():
    """Main migration function."""
    old_notes_dir = Path('old_notes')

    if not old_notes_dir.exists():
        logger.error("old_notes directory not found!")
        return

    # Get all date folders
    date_folders = [f for f in old_notes_dir.iterdir() if f.is_dir()]
    date_folders.sort()

    logger.info(f"Found {len(date_folders)} date folders in old_notes/")

    # Dry run first
    logger.info("\n=== DRY RUN ===")
    dry_run_results = []
    for date_folder in date_folders:
        result = migrate_date_folder(date_folder, dry_run=True)
        dry_run_results.append(result)

    # Summary of dry run
    total_md = sum(1 for r in dry_run_results if r['md_migrated'])
    total_images = sum(r['images_migrated'] for r in dry_run_results)

    logger.info(f"\n=== DRY RUN SUMMARY ===")
    logger.info(f"Folders to process: {len(date_folders)}")
    logger.info(f"Markdown files to migrate: {total_md}")
    logger.info(f"Image files to migrate: {total_images}")

    # Show any issues
    issues = [r for r in dry_run_results if r['errors']]
    if issues:
        logger.warning(f"\nFound {len(issues)} folders with issues:")
        for issue in issues[:5]:  # Show first 5
            logger.warning(f"  {issue['date']}: {', '.join(issue['errors'])}")

    # Ask for confirmation
    print("\n" + "="*60)
    response = input(f"Proceed with migrating {total_md} markdown files and {total_images} images? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        logger.info("Migration cancelled")
        return

    # Actual migration
    logger.info("\n=== STARTING MIGRATION ===")
    results = []
    for date_folder in date_folders:
        result = migrate_date_folder(date_folder, dry_run=False)
        results.append(result)

    # Final summary
    total_md_migrated = sum(1 for r in results if r['md_migrated'])
    total_images_migrated = sum(r['images_migrated'] for r in results)
    total_errors = sum(len(r['errors']) for r in results)

    logger.info(f"\n=== MIGRATION COMPLETE ===")
    logger.success(f"✓ Migrated {total_md_migrated} markdown files")
    logger.success(f"✓ Migrated {total_images_migrated} image files")
    if total_errors > 0:
        logger.warning(f"⚠ Encountered {total_errors} issues (see logs above)")

    # Check for empty old_notes folders
    logger.info("\n=== CLEANUP CHECK ===")
    empty_folders = []
    for date_folder in date_folders:
        remaining_files = list(date_folder.glob('*'))
        if not remaining_files:
            empty_folders.append(date_folder)

    if empty_folders:
        logger.info(f"Found {len(empty_folders)} empty date folders in old_notes/")
        cleanup_response = input(f"Remove {len(empty_folders)} empty folders from old_notes/? (yes/no): ")
        if cleanup_response.lower() in ['yes', 'y']:
            for folder in empty_folders:
                folder.rmdir()
                logger.success(f"Removed empty folder: {folder.name}")
            logger.success(f"✓ Cleaned up {len(empty_folders)} empty folders")
    else:
        logger.info("No empty folders to clean up")

    # Final verification
    logger.info("\n=== VERIFICATION ===")
    notes_count = len(list(Path('dailies/notes').glob('*.md'))) if Path('dailies/notes').exists() else 0
    images_dirs = len(list(Path('dailies/images').iterdir())) if Path('dailies/images').exists() else 0

    logger.info(f"Total markdown files in dailies/notes/: {notes_count}")
    logger.info(f"Total date folders in dailies/images/: {images_dirs}")


if __name__ == "__main__":
    main()
