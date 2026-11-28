# Status report: kritva-mind

`status.json` is this repository's task-level report for the program (schema 2.0, `status.schema.json`). It reports facts only; acceptance and credit live in KritvaOS/kritva-program.

It lists only tasks that are in the program's approved baseline, because the program rejects any other task ID in a status report (D-116). Today that is KOS-MIND-M0-001 (accepted in the program) and KOS-MIND-001 (baselined in v13, D-125; accepted in the program, D-126). The other Mind tasks stay in planning inventory in `planning/TASKS.md`; each is added here, with its execution state and evidence, after a baseline version includes it. The file is maintained by hand: refresh `source.commit` and `updated_at` whenever it changes. The program does not expire a report on age (D-165): a task keeps its credit until this repository changes inside that task's scope, or in shared material, after `source.commit` (scopes are in `v2/planning/task_scopes.json` in KritvaOS/kritva-program). A report older than 60 days only raises a warning.

`STATUS.md` and `program_snapshot.json` are generated progress views taken from the program (D-120); do not edit them by hand. `python3 scripts/progress_report.py --check` verifies that they agree.
