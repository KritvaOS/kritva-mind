# REV-006: kritva-mind governance baseline (V2-M0-MIND-001)

Status: APPROVED by the owner (D-114, 2026-11-07); ruleset and CODEOWNERS verified against GitHub on 2026-11-07 (D-115).
Reviewed commit: `564c4e002c19b09309093a47aab1c7a7eda12825` (kritva-mind `main`, recorded in the program review record)..
Program record: REV-006 in kritva-program `v2/planning/PENDING_REVIEWS.md`.
Related plan: kritva-program `v2/planning/M0_CLOSURE_PLAN.md` and `v2/planning/M0_TASK_DEFINITIONS.md`.

This record is evidence for the owner's review. It does not accept a task, award progress, or close V2-M0-MIND-001. Closure needs the owner's decision below and an approved completion record for the milestone.

## 1. Proposed M0 task (planning only)

Title: Mind governance baseline accepted. Weight: 3. Registered as a `KOS-MIND` task only after baseline v11 and owner approval; no placeholder row is added to `TASKS.md` before then.

| Criterion | Statement | Evidence in the working tree | Result |
|---|---|---|---|
| AC-M0-1 | Governance files exist: `AGENTS.md`, `ACCEPTANCE_CRITERIA.md`, `SECURITY.md`, `.github/CODEOWNERS`, `.github/kritva-gate.json` | All present; CODEOWNERS content verified against GitHub on 2026-11-07 | PRESENT |
| AC-M0-2 | Required checks are defined and named the same in workflows, `.github/kritva-gate.json` and the ruleset: `secret-scan`, `commit-message-check`, `pr-acceptance-gate`, `readme-check` | Workflow job names match. The ruleset requires `readme-check`; the gate file was aligned by PR #29. `unit-tests` runs but is not a required check | MATCH (PR #29 merged) |
| AC-M0-3 | The branch ruleset on `main` requires a pull request and the required checks. The approval roles `REPO_CODE_OWNER` and `ARCHITECTURE_REVIEWER` are held by the owner on an interim basis (D-047) and are not enforced by the ruleset (D-115) | Checked 2026-11-07 through the GitHub rulesets API: ruleset `protect-main` is active on the default branch, blocks deletion and force-push, requires a pull request with 0 approving reviews and no code-owner review, and requires pr-acceptance-gate, commit-message-check, readme-check, secret-scan. Bypass actors are not visible without admin access | PARTIAL: pull request and checks verified; approvals not enforced |
| AC-M0-4 | Commit policy is enforced by an automated check | `commit-message-check` workflow | PRESENT |
| AC-M0-5 | The program has a status source for Mind | `status/status.json` (schema 2.0) registers the workstream (PD-014, D-116) and reports KOS-MIND-M0-001 (baseline v11, D-117) | MET |
| AC-M0-6 | Planning records are consistent and no unimplemented gate is reported as passing | `planning/MILESTONE_STATUS.md` lists `make test-integration` and `make test-regression` as NOT_IMPLEMENTED | CONSISTENT |

## 2. Status source (PD-014, decided)

PD-014 was decided in D-116: Mind is registered on workstream MIND and publishes `status/status.json` in the program's schema 2.0. Baseline v11 (D-117) adds KOS-MIND-M0-001, which the status report now lists; KOS-MIND-001 and KOS-MIND-002 are still not baselined and are not reported.

## 3. CI evidence

Recorded 2026-11-07 from the GitHub check runs on the reviewed commit:

- unit-tests run id: 42385456931
- commit: `564c4e002c19b09309093a47aab1c7a7eda12825`
- result: success (push run on `main`; `secret-scan` run 42385456977 and `readme-check` run 42385456895 also succeeded). `commit-message-check` and `pr-acceptance-gate` run on pull requests, so they have no run on this commit.

## 4. Verification of ruleset and CODEOWNERS (2026-11-07)

- Ruleset: verified as stated in AC-M0-3. The approval requirement is not enforced; the owner merges under the interim reviewer roles of D-047.
- CODEOWNERS: verified. `*` and the protected files (`.github/`, `SECURITY.md`, `LICENSE`, `ACCEPTANCE_CRITERIA.md`) are owned by `@dineshannayya`. GitHub does not enforce code-owner review because the ruleset does not require it.
- Not verified: bypass actors (admin access needed).

## 5. Decision

Decision: APPROVED (owner, interim reviewer roles of D-047; recorded in D-114 on 2026-11-07; verification in D-115)
Decided by: Dinesh
Date: 2026-11-07
Notes: This is not independent review.
