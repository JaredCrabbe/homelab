import json
import os
import shutil
import time
from pathlib import Path



SOURCE = Path.home() / "homelab"
BACKUP_ROOT = Path("/srv/nas/backups/homelab")
RETENTION_COUNT = 7

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "homelab-backup",
}

EXCLUDED_SUFFIXES = {
    ".log",
}

def should_include(path):
    relative = path.relative_to(SOURCE)

    for part in relative.parts:
        if part in EXCLUDED_DIRS:
            return False

    if path.suffix in EXCLUDED_SUFFIXES:
        return False

    return True

def cleanup_old_backups():
    backups = [
        path
        for path in BACKUP_ROOT.iterdir()
        if path.is_dir()
    ]
    backups.sort(reverse=True)

    old_backups = backups[RETENTION_COUNT:]

    for backup in old_backups:
        shutil.rmtree(backup)
        print(f"[CLEANUP] Succesfully removed old backup: {backup.name}")

BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
backup_dir = BACKUP_ROOT / timestamp
backup_dir.mkdir(parents=True, exist_ok=True)

for path in SOURCE.rglob("*"):
    if path.is_file() and should_include(path):
        realtive_path = path.relative_to(SOURCE)
        destination = backup_dir / realtive_path

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)

cleanup_old_backups()