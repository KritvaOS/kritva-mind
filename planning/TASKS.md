# Tasks: kritva-mind

Task IDs use the prefix `KOS-MIND` (proposed registry, program decision PD-004). Tasks here are planning inventory: no weight, no credit, until a separately approved baseline amendment. Status vocabulary: NOT_STARTED, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, CHANGES_REQUESTED, ACCEPTED, DEFERRED, CANCELLED.

| Task | Title | Status | Milestone | Acceptance |
|---|---|---|---|---|
| KOS-MIND-001 | Mind request, context and result contract | NOT_STARTED (proposed, awaiting owner approval) | V2-M1-MIND-001 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) section 3 |

Task KOS-MIND-001 includes the architecture ([ARCHITECTURE.md](../ARCHITECTURE.md), proposed) as its first deliverable.

## Proposed later tasks (not registered)

These are candidates only. Each becomes a row above when its prerequisites and acceptance criteria are concrete and the owner approves it. None has a status, an owner or a date.

| Candidate | Scope | Depends on | Target milestone |
|---|---|---|---|
| KOS-MIND-002 | Schema validation, cancellation and error-path tests; implement `make test-unit` | KOS-MIND-001 accepted | V2-M2-MIND-001 |
| KOS-MIND-003 | Context identity and lifecycle implementation | KOS-MIND-001 accepted | V2-M2-MIND-001 |
| KOS-MIND-004 | Integration tests against the Core and Sense contract boundaries; implement `make test-integration` and `make test-regression` | approved Core and Sense contracts | V2-M2-MIND-001 |
| KOS-MIND-005 | Reasoning adapter interface and knowledge interface | KOS-MIND-001 accepted; decision D-4 | V2-M5-MIND-001 |
| KOS-MIND-006 | Replay and reproducibility of results in simulation; Mind-to-Skill integration tests | KOS-MIND-002, a Skill contract | V2-M5-MIND-001 |
| KOS-MIND-007 | Security, resource limits and failure-recovery review; release evidence | earlier tasks | V2-M8-MIND-001 |

`tasks/KOS-MIND-001/TASK.md` is created when the task starts, not before.
