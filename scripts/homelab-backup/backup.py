import json
import os
import shutil
import time
from pathlib import Path
import hashlib


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


def sha256_file(path):
    hasher = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            hasher.update(chunk)

    return hasher.hexdigest()

def write_checksums(backup_dir):
    checksum_file = backup_dir / "checksums.sha256"

    with checksum_file.open("w", encoding="utf-8") as output:
        for path in sorted(backup_dir.rglob("*")):
            if not path.is_file():
                continue

            if path == checksum_file:
                continue

            relative_path = path.relative_to(backup_dir)
            checksum = sha256_file(path)

            output.write(f"{checksum}  {relative_path}\n")

    print(f"[VERIFY] Created checksum file: {checksum_file.name}")


def verify_checksums(backup_dir):
    checksum_file = backup_dir / "checksums.sha256"

    with checksum_file.open("r", encoding="utf-8") as file:
        for line in file:
            expected_hash, relative_path = line.strip().split("  ", 1)

            path = backup_dir / relative_path
            actual_hash = sha256_file(path)

            if actual_hash != expected_hash:
                raise ValueError(
                    f"Checksum mismatch: {relative_path}"
                )

    print("[VERIFY] Backup integrity check passed.")


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

try:
    backup_dir.mkdir(parents=True, exist_ok=False)

    for path in SOURCE.rglob("*"):
        if path.is_file() and should_include(path):
            relative_path = path.relative_to(SOURCE)
            destination = backup_dir / relative_path

            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)

    write_checksums(backup_dir)
    verify_checksums(backup_dir)
    


    print(f"[BACKUP] Successfully created backup: {backup_dir.name}")

    cleanup_old_backups()

except Exception as error:
    print(f"[ERROR] Backup failed: {error}")

    if backup_dir.exists():
        shutil.rmtree(backup_dir)
        print(
            f"[CLEANUP] Removed incomplete backup: "
            f"{backup_dir.name}"
        )

    raise