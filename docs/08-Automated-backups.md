# Automated Homelab Backups

## Overview

The homelab uses a custom Python backup system to automatically back up the homelab configuration to the NAS.

The backup system was built to provide:

- Automated daily backups
- Timestamped backup directories
- Backup retention
- Backup integrity verification
- Cleanup of incomplete backups
- systemd scheduling
- NAS mount dependency
- Failure detection
- ntfy failure notifications
- Tested restore procedures

The backup system protects the configuration required to rebuild the homelab rather than backing up large application data or media.

---

## Backup Architecture

```text
~/homelab
    |
    v
backup.py
    |
    v
/srv/nas/backups/homelab/
    |
    +-- YYYY-MM-DD_HH-MM-SS/
    |       |
    |       +-- compose/
    |       +-- docs/
    |       +-- .gitignore
    |       +-- checksums.sha256
    |
    +-- Previous backups...
```

The newest seven backups are retained.

---

## Source

The backup source is:

```text
/home/jared/homelab
```

This contains the configuration, documentation, scripts, and Compose files used by the homelab.

---

## Backup Destination

Backups are stored at:

```text
/srv/nas/backups/homelab
```

Each backup receives a timestamped directory:

```text
YYYY-MM-DD_HH-MM-SS
```

Example:

```text
/srv/nas/backups/homelab/2026-08-20_15-34-42
```

---

## Backup Script

The backup script is located at:

```text
~/homelab/scripts/homelab-backup/backup.py
```

The script is written in Python and uses standard library modules including:

- `pathlib`
- `shutil`
- `time`
- `hashlib`

The script performs the following process:

```text
Create backup directory
        |
        v
Copy selected homelab files
        |
        v
Generate SHA-256 checksums
        |
        v
Verify copied files
        |
        +---- Failure ----> Remove incomplete backup
        |                         |
        |                         v
        |                    Exit non-zero
        |
        v
Backup successful
        |
        v
Apply retention policy
```

---

## Backup Exclusions

The backup script excludes directories that should not be stored in the backup.

Current excluded directories include:

```text
.git
__pycache__
homelab-backup
```

Log files are also excluded:

```text
*.log
```

The backup script itself is excluded because it is already tracked through Git.

---

## Backup Retention

The backup system retains:

```text
7 backups
```

After a successful backup, existing backup directories are sorted and anything older than the newest seven backups is removed.

Example cleanup message:

```text
[CLEANUP] Successfully removed old backup: 2026-08-17_14-05-56
```

Retention only runs after the new backup has successfully completed.

---

## Integrity Verification

Every backup contains:

```text
checksums.sha256
```

SHA-256 hashes are calculated for the copied files after the backup has been created.

The script then recalculates each file's SHA-256 hash and compares it against the stored value.

A successful verification produces:

```text
[VERIFY] Created checksum file: checksums.sha256
[VERIFY] Backup integrity check passed.
```

Only after verification succeeds is the backup considered successful.

---

## Corruption Detection

Integrity verification was tested by deliberately modifying a backed-up file after the checksum manifest had been generated.

The verification correctly detected:

```text
Checksum mismatch: .gitignore
```

The backup was then treated as failed and automatically removed.

This confirmed that the integrity check detects file corruption rather than simply checking whether files exist.

---

## Incomplete Backup Protection

The backup operation is wrapped in exception handling.

If an error occurs while copying or verifying files:

1. The error is logged.
2. The incomplete timestamped backup directory is removed.
3. The Python exception is raised.
4. Python exits with a non-zero exit status.
5. systemd marks the backup service as failed.

Example:

```text
[ERROR] Backup failed: Permission denied
[CLEANUP] Removed incomplete backup: 2026-08-20_15-09-06
```

This prevents incomplete backups from being mistaken for valid backups.

---

## systemd Service

Backups are executed using:

```text
homelab-backup.service
```

Service file:

```text
/etc/systemd/system/homelab-backup.service
```

Important configuration:

```ini
[Unit]
Description=Homelab NAS Backup
RequiresMountsFor=/srv/nas
After=local-fs.target
OnFailure=homelab-backup-failure.service

[Service]
Type=oneshot
User=jared
ExecStart=/usr/bin/python3 /home/jared/homelab/scripts/homelab-backup/backup.py
```

`Type=oneshot` is used because the backup performs a single operation and then exits.

---

## NAS Mount Dependency

The service contains:

```ini
RequiresMountsFor=/srv/nas
```

This ensures systemd treats the NAS mount as a dependency of the backup service.

This is important because `/srv/nas/backups/homelab` must refer to the mounted NAS filesystem rather than an ordinary directory on the Fedora root filesystem.

---

## Automatic Scheduling

The backup is scheduled using:

```text
homelab-backup.timer
```

Timer file:

```text
/etc/systemd/system/homelab-backup.timer
```

Configuration:

```ini
[Unit]
Description=Daily Homelab NAS Backup

[Timer]
OnCalendar=*-*-* 13:00:00
Persistent=true
Unit=homelab-backup.service

[Install]
WantedBy=timers.target
```

The backup runs every day at:

```text
13:00
```

`Persistent=true` allows systemd to account for a missed timer while the machine was powered off.

---

## Failure Notifications

Backup failures are handled by:

```text
homelab-backup-failure.service
```

The backup service contains:

```ini
OnFailure=homelab-backup-failure.service
```

When the backup service enters a failed state, systemd starts the failure notification service.

The notification service sends an alert to the existing local ntfy server.

Notification endpoint:

```text
http://192.168.10.151:8082/homelab
```

The alert tells the administrator that the homelab backup failed and directs troubleshooting toward:

```bash
journalctl -u homelab-backup.service
```

The complete failure notification chain was tested successfully.

---

## Monitoring the Backup

Check the timer:

```bash
systemctl status homelab-backup.timer
```

List scheduled timers:

```bash
systemctl list-timers --all
```

Check the most recent backup service result:

```bash
systemctl show homelab-backup.service \
    -p Result \
    -p ExecMainStatus \
    -p ActiveState \
    -p SubState
```

Successful result:

```text
ActiveState=inactive
SubState=dead
Result=success
ExecMainStatus=0
```

View backup logs:

```bash
journalctl -u homelab-backup.service
```

---

## Restore Procedure

Backups can be restored manually.

First select the newest backup:

```bash
LATEST=$(find /srv/nas/backups/homelab \
    -mindepth 1 -maxdepth 1 -type d \
    -printf '%p\n' | sort | tail -n1)
```

Verify the selected backup:

```bash
echo "$LATEST"
```

For a safe restore test, create a temporary directory:

```bash
rm -rf /tmp/homelab-restore-test
mkdir -p /tmp/homelab-restore-test
```

Restore the backup:

```bash
cp -a "$LATEST"/. /tmp/homelab-restore-test/
```

Verify the restored files:

```bash
cd /tmp/homelab-restore-test
sha256sum -c checksums.sha256
```

Every file should report:

```text
OK
```

After testing:

```bash
rm -rf /tmp/homelab-restore-test
```

---

## Restore Test

A complete restore test was performed using a verified backup.

The backup was copied from the NAS into:

```text
/tmp/homelab-restore-test
```

The restored directory contained the expected:

- Compose configurations
- Homepage configuration
- Environment files
- Samba configuration
- Monitoring code and state
- Documentation
- `.gitignore`
- SHA-256 manifest

The restored files were then checked with:

```bash
sha256sum -c checksums.sha256
```

Every file returned:

```text
OK
```

This verified that the backup could be successfully restored and that the restored files matched the original backup data.

---

## Failure Testing

Several failure scenarios were deliberately tested.

### Missing Backup Script

The backup script was temporarily renamed.

Result:

```text
ActiveState=failed
SubState=failed
Result=exit-code
ExecMainStatus=2
```

systemd correctly detected the failure.

### Permission Failure

A documentation file was temporarily made unreadable.

The backup failed with a permission error and the incomplete backup directory was automatically removed.

### Checksum Corruption

A backed-up `.gitignore` file was deliberately modified after checksum generation.

Verification produced:

```text
Checksum mismatch: .gitignore
```

The corrupted backup was automatically removed.

### Failure Notification

A backup failure was triggered through systemd.

`OnFailure=` successfully started:

```text
homelab-backup-failure.service
```

and an ntfy notification was received.

---

## Result

The automated backup system now provides:

```text
Daily scheduling
        +
NAS mount dependency
        +
Timestamped backups
        +
7-backup retention
        +
SHA-256 integrity verification
        +
Incomplete backup cleanup
        +
systemd failure detection
        +
ntfy failure notifications
        +
Tested restore procedure
```

The backup system has been tested for both successful and failed backup scenarios as well as an actual restore and integrity verification.
