# Status report: kritva-mind

`status.json` is this repository's task-level report for the program (schema 2.0, `status.schema.json`). It reports facts only; acceptance and credit live in KritvaOS/kritva-program.

It lists only tasks that are in the program's approved baseline, because the program rejects any other task ID in a status report (D-116). Today that is KOS-MIND-M0-001. The other Mind tasks stay in planning inventory in `planning/TASKS.md`; each is added here, with its execution state and evidence, after a baseline version includes it. The file is maintained by hand: refresh `source.commit` and `updated_at` whenever it changes. The program treats a report older than 14 days as stale.

`STATUS.md` and `program_snapshot.json` are generated progress views taken from the program (D-120); do not edit them by hand. `python3 scripts/progress_report.py --check` verifies that they agree.
