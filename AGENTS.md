# AGENTS.md: kritva-mind

Guidance for AI coding agents and contributors. The program rules live in kritva-program (`AGENTS.md`, `v2/planning/ACCEPTANCE_STANDARD.md`); this file adds the rules for this repository.

## 1. Scope

Kritva Mind owns: the Mind request, context and result contract: inputs, context identity, output schema, uncertainty and error reporting, cancellation and deterministic validation. It does not own: sensing (kritva-sense), motion (kritva-motion), skill orchestration (kritva-skill), and the platform foundation (kritva-core). Respect these boundaries: depends on Core and Sense contract versions; must not import Sense internals.

## 2. Program rules that apply here

1. This repository reports facts; the program repository decides baseline, weights, approvals and gates. A commit here never creates credit.
2. Software acceptance (tests, simulation, mocks, versioned interfaces) is never described as hardware or safety validation.
3. No empty folders, no placeholder tasks, no invented owners or dates. Add `src/` and other folders only when a real task needs them.
4. Interfaces are contract-first and versioned. A breaking change needs a new MAJOR version, a changelog entry and an approved decision.

## 3. Commits and pull requests

- Commit header: `type(scope): summary` (feat, fix, docs, refactor, test, build, ci, chore, perf, revert), at most 72 characters.
- Exactly one footer `Task: KOS-MIND-NNN`. Check with `python3 scripts/security/check_commit_format.py --range origin/main..HEAD`.
- Never add a `Claude-Session:` trailer or a claude.ai session link to a commit. `commit-message-check` blocks them.
- Open a PR; do not push to `main`. Required checks: secret-scan, commit-message-check.

## 4. Secrets

Never commit credentials, tokens, keys or production data. If one is committed by mistake, tell the Security Owner at once; removing it later does not make it safe.

## 5. Tests

`make check`, `make test-unit`, `make test-integration`, `make test-regression`, `make docs-check`. An unimplemented target exits 3 (NOT_IMPLEMENTED); do not edit a target to exit 0 to make a gate pass. A fixed defect adds a regression test.

## 6. Tags and milestones

Release tags are annotated SemVer (`vMAJOR.MINOR.PATCH`), created only after the approved merge. A milestone closes only through an approved `COMPLETION_RECORD.md`; a tag or a merge does not close it.
