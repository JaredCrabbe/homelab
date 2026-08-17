# Next Project: Automated Backups

## Status

Planned — not yet implemented.

## Reason for choosing this next

The NAS already provides storage under:

```text
/srv/nas/backups
```

The next logical project is therefore to turn that storage into a reliable automated backup system rather than rebuilding the NAS/Samba infrastructure.

## Goals

The backup project should eventually provide:

- Automated backups
- A defined backup source
- A defined backup destination
- Scheduled execution
- Logging
- Verification that backups completed
- Failure reporting
- Retention/cleanup rules
- Documentation and Git tracking

## Important principle

The backup system should be designed and tested before it is trusted with important data.

The project should begin with non-critical test data and only later be expanded to important files.

## Planned progression

1. Define exactly what needs to be backed up.
2. Decide where the backup data will live.
3. Choose the backup method.
4. Build a test backup.
5. Restore the test backup.
6. Automate the backup.
7. Add logging.
8. Add failure notifications.
9. Add retention rules.
10. Document the final system.
