# Status report: kritva-mind

`status.json` is this repository's task-level report for the program (schema 2.0, `status.schema.json`). It reports facts only; acceptance and credit live in KritvaOS/kritva-program.

`tasks` is empty on purpose. The program accepts a task ID in a status report only after the task is in its approved baseline, and no `KOS-MIND` task is baselined yet (D-116). Planning inventory stays in `planning/TASKS.md`. When a task is baselined, add it here with its execution state and evidence, and refresh `source.commit` and `updated_at`.

The program treats a report older than 14 days as stale.
