# Tasks: kritva-mind

Task IDs use the prefix `KOS-MIND` (proposed registry, program decision PD-004). Tasks here are planning inventory: no weight, no credit, until a separately approved baseline amendment. Status vocabulary: NOT_STARTED, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, CHANGES_REQUESTED, ACCEPTED, DEFERRED, CANCELLED.

| Task | Title | Status | Milestone | Acceptance |
|---|---|---|---|---|
| KOS-MIND-001 | Mind request, context and result contract | ACCEPTED (owner accepted in chat on 2026-11-10 against [COMPLETION_RECORD.md](../COMPLETION_RECORD.md): AC-001, AC-002, AC-004 and AC-006 PASS; seven criteria WAIVED with conditions that cover only their deferred parts; interim roles of D-047, not independent review; baselined in kritva-program v13, D-125; central approval and credit are decided in kritva-program; see [tasks/KOS-MIND-001/TASK.md](../tasks/KOS-MIND-001/TASK.md)) | V2-M1-MIND-001 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) section 3 |
| KOS-MIND-002 | Mind contract validator | IN_PROGRESS (owner instructed the start in chat, 2026-11-03; on 2026-11-06 the owner decided in chat to land it before the KOS-MIND-001 completion record and the `v0.1.0` tag; see [tasks/KOS-MIND-002/TASK.md](../tasks/KOS-MIND-002/TASK.md)) | V2-M2-MIND-001 | proposed criteria in [tasks/KOS-MIND-002/TASK.md](../tasks/KOS-MIND-002/TASK.md); none accepted |
| KOS-MIND-M0-001 | Mind governance and acceptance review | ACCEPTED (owner accepted 2026-11-07; governance baseline merged; review REV-006 approved by the owner under the interim roles of D-047, D-114, not independent; baselined in kritva-program v11, D-117; central approval pending; criteria AC-M0-1 to AC-M0-6 in the package, AC-M0-3 PARTIAL) | V2-M0-MIND-001 | [REV-006 evidence package](reviews/REV-006-GOVERNANCE-BASELINE.md) |

Task KOS-MIND-001 includes the architecture ([ARCHITECTURE.md](../ARCHITECTURE.md), proposed) as its first deliverable.

The closure record for KOS-MIND-001, agreed by the owner in chat on 2026-11-04 (not a completion record), is [reviews/KOS-MIND-001-CLOSURE.md](reviews/KOS-MIND-001-CLOSURE.md); the proposed scope, dependencies, boundaries and evidence of all eight tasks are in [TASK_CATALOGUE.md](TASK_CATALOGUE.md). The catalogue is proposed; neither registers a task or changes a baseline. The completion record for milestone V2-M1-MIND-001, approved by the owner in chat on 2026-11-06 under the interim roles of D-047, is [../COMPLETION_RECORD.md](../COMPLETION_RECORD.md). It does not change a task status, a baseline or program credit.

## Proposed later tasks (not registered)

KOS-MIND-002 left this list when it started (see the table above). The rest are candidates only. Each becomes a row above when its prerequisites and acceptance criteria are concrete and the owner approves it. None has a status, an owner or a date.

| Candidate | Scope | Depends on | Target milestone |
|---|---|---|---|
| KOS-MIND-003 | Context lifecycle checks and edge/hybrid conformance tests (AC-009, AC-010); implements no reasoning provider | KOS-MIND-001 accepted | V2-M2-MIND-001 |
| KOS-MIND-004 | Integration tests at the real Sense boundary; implement `make test-integration` and `make test-regression`. Core integration only if Mind consumes a defined, approved Core interface | KOS-MIND-002; approved Sense contract | V2-M2-MIND-001 |
| KOS-MIND-005 | Reasoning adapter and memory interface conformance (providers and backends live outside this repository unless decided otherwise) | KOS-MIND-001 accepted; decision D-4 | V2-M5-MIND-001 |
| KOS-MIND-006 | Replay of recorded Mind inputs and execution records (AC-011), labelled as simulation | KOS-MIND-002 | V2-M5-MIND-001 |
| KOS-MIND-007 | Mind-to-Skill integration tests | KOS-MIND-006; an agreed Skill contract; program milestone V2-M3 (control plane) | V2-M5-MIND-001 |
| KOS-MIND-008 | Security, resource limits and failure-recovery review; release evidence | earlier tasks | V2-M8-MIND-001 |

Task files are created when a task starts, not before.
