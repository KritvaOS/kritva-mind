# REV-006: kritva-mind governance baseline (V2-M0-MIND-001)

Status: PREPARED, OWNER DECISION PENDING.
Reviewed commit: ____ (record the `main` commit current when the owner reviews; prepared from the working tree of `main` on 2026-11-07).
Program record: REV-006 in kritva-program `v2/planning/PENDING_REVIEWS.md`.
Related plan: kritva-program `v2/planning/M0_CLOSURE_PLAN.md` and `v2/planning/M0_TASK_DEFINITIONS.md`.

This record is evidence for the owner's review. It does not accept a task, award progress, or close V2-M0-MIND-001. Closure needs the owner's decision below and an approved completion record for the milestone.

## 1. Proposed M0 task (planning only)

Title: Mind governance baseline accepted. Weight: 3. Registered as a `KOS-MIND` task only after baseline v11 and owner approval; no placeholder row is added to `TASKS.md` before then.

| Criterion | Statement | Evidence in the working tree | Result |
|---|---|---|---|
| AC-M0-1 | Governance files exist: `AGENTS.md`, `ACCEPTANCE_CRITERIA.md`, `SECURITY.md`, `.github/CODEOWNERS`, `.github/kritva-gate.json` | Present, except CODEOWNERS not re-checked in this pass | VERIFY CODEOWNERS |
| AC-M0-2 | Required checks are defined and named the same in workflows and `.github/kritva-gate.json` | `kritva-gate.json` lists `secret-scan`, `commit-message-check`, `pr-acceptance-gate`; each has a workflow job of the same name. `unit-tests` and `readme-check` workflows also exist; `unit-tests` is not a required check (see `planning/MILESTONE_STATUS.md`) | MATCH |
| AC-M0-3 | The branch ruleset on `main` requires those checks, a pull request, and the approvals `REPO_CODE_OWNER` and `ARCHITECTURE_REVIEWER` | GitHub settings, not visible from the repository | OWNER TO ATTEST |
| AC-M0-4 | Commit policy is enforced by an automated check | `commit-message-check` workflow | PRESENT |
| AC-M0-5 | The program has a status source for Mind | None: Mind has no `status/` directory and is not registered on a program workstream (PD-014) | NOT MET until PD-014 is decided |
| AC-M0-6 | Planning records are consistent and no unimplemented gate is reported as passing | `planning/MILESTONE_STATUS.md` lists `make test-integration` and `make test-regression` as NOT_IMPLEMENTED | CONSISTENT |

## 2. Open item: Mind status source (PD-014)

The program cannot read Mind state because no status file exists. Two options for the owner:

1. Add a `status/status.json` in this repository in the same schema as kritva-sense (schema 2.0), with KOS-MIND-001 and KOS-MIND-002 as they stand in `planning/TASKS.md`, and register Mind in the program (PD-014).
2. Register Mind in the program from `planning/TASKS.md` only, with no status file.

Until PD-014 is decided, AC-M0-5 stays open and this repository adds no status file.

## 3. CI evidence

Record a `unit-tests` run on the reviewed commit:

- unit-tests run id: ____
- commit: ____
- result: ____

## 4. Owner attestations

- [ ] Ruleset on `main` requires pull request, the three required checks, and both approval roles (AC-M0-3).
- [ ] CODEOWNERS entries are the intended approvers.

## 5. Decision

Decision: PENDING
Decided by: ____
Date: ____
Notes: ____
