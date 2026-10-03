# Automated NAS Backups

## Status

**Implemented and tested.** This project is no longer a future task.

## Purpose

The backup system creates timestamped backups of the configured homelab files and stores them on the NAS under:

```text
/srv/nas/backups/homelab
```

The script is located at `~/homelab/scripts/homelab-backup/backup.py`.

## Automation

The job runs as `homelab-backup.service`, a systemd `oneshot` service running as user `jared`. The unit includes `RequiresMountsFor=/srv/nas` so the backup job depends on the NAS mount being available.

The `homelab-backup.timer` schedules the job daily at 13:00 and uses `Persistent=true` so a missed run can be considered after the system comes back online.

## Backup safeguards

The implemented workflow includes:

- Timestamped backup snapshots
- Retention of the seven most recent backups
- SHA-256 checksum generation
- Checksum verification
- Cleanup of incomplete backup runs
- Failure notification through ntfy
- systemd scheduling and mount dependency

## Verification and restore test

The backup process was tested rather than treated as complete based only on a successful run. The checksum verification command:

```bash
sha256sum -c checksums.sha256
```

reported `OK` for the backed-up files during the restore/verification test. The backup-failure notification service was also tested successfully through ntfy.

## Operational checks

Useful commands:

```bash
systemctl status homelab-backup.timer
systemctl list-timers | grep homelab-backup
journalctl -u homelab-backup.service -n 50 --no-pager
```

Check that `/srv/nas` is mounted before relying on a backup, and periodically perform restore tests. A backup should not be considered reliable until its contents can be verified and restored.

## Skills demonstrated

Python automation, file handling, checksums, retention logic, error handling, systemd services and timers, mount dependencies, ntfy failure alerts, restore verification, and operational documentation.
