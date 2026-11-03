# Tasks: kritva-mind

Task IDs use the prefix `KOS-MIND` (proposed registry, program decision PD-004). Tasks here are planning inventory: no weight, no credit, until a separately approved baseline amendment. Status vocabulary: NOT_STARTED, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, CHANGES_REQUESTED, ACCEPTED, DEFERRED, CANCELLED.

| Task | Title | Status | Milestone | Acceptance |
|---|---|---|---|---|
| KOS-MIND-001 | Mind request, context and result contract | IN_PROGRESS (owner approved the start in chat, 2026-11-02; see [tasks/KOS-MIND-001/TASK.md](../tasks/KOS-MIND-001/TASK.md)) | V2-M1-MIND-001 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) section 3 |

Task KOS-MIND-001 includes the architecture ([ARCHITECTURE.md](../ARCHITECTURE.md), proposed) as its first deliverable.

## Proposed later tasks (not registered)

These are candidates only. Each becomes a row above when its prerequisites and acceptance criteria are concrete and the owner approves it. None has a status, an owner or a date.

| Candidate | Scope | Depends on | Target milestone |
|---|---|---|---|
| KOS-MIND-002 | Standard-library validator under the D-2 safeguards ([ARCHITECTURE.md](../ARCHITECTURE.md) section 8.1): keyword allowlist that fails closed, local `$ref` resolution, asserted `date-time`, deterministic error order, example-manifest tests; schema validation, cancellation and error-path tests; implement `make test-unit` and a `unit-tests` workflow (adding it to the required checks needs an owner-approved kritva-program pipeline update) | KOS-MIND-001 accepted | V2-M2-MIND-001 |
| KOS-MIND-003 | Context lifecycle checks and edge/hybrid conformance tests (AC-009, AC-010); implements no reasoning provider | KOS-MIND-001 accepted | V2-M2-MIND-001 |
| KOS-MIND-004 | Integration tests at the real Sense boundary; implement `make test-integration` and `make test-regression`. Core integration only if Mind consumes a defined, approved Core interface | KOS-MIND-002; approved Sense contract | V2-M2-MIND-001 |
| KOS-MIND-005 | Reasoning adapter and memory interface conformance (providers and backends live outside this repository unless decided otherwise) | KOS-MIND-001 accepted; decision D-4 | V2-M5-MIND-001 |
| KOS-MIND-006 | Replay of recorded Mind inputs and execution records (AC-011), labelled as simulation | KOS-MIND-002 | V2-M5-MIND-001 |
| KOS-MIND-007 | Mind-to-Skill integration tests | KOS-MIND-006; an agreed Skill contract; program milestone V2-M3 (control plane) | V2-M5-MIND-001 |
| KOS-MIND-008 | Security, resource limits and failure-recovery review; release evidence | earlier tasks | V2-M8-MIND-001 |

Task files are created when a task starts, not before.
