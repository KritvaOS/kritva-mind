# Task catalogue: kritva-mind (PROPOSED)

Status: PROPOSED planning document. It describes what this repository builds; it does not register tasks, assign weights, change milestone records or claim any acceptance. kritva-program decides how the work is governed and accepted ([README.md](../README.md) section 2). Task registration and baseline changes go through the program's approved planning process, never through this file. Written on 2026-11-03, updated 2026-11-04, to align this repository with the kritva-program V2 plan as reviewed in the owner's alignment session; nothing here is owner-approved yet.

State words used below: IN_PROGRESS, PROPOSED (a design or draft exists, nothing accepted), NOT_IMPLEMENTED (no code or test exists), UNKNOWN (the documents do not say). An unimplemented gate is never a pass.

## 1. Alignment rules

1. kritva-program is the sole authority for baseline, weights, approvals, milestone acceptance and release gates. This repository reports facts.
2. Mind has no baselined weights (the repository is not baselined in the program pipeline), so no Mind progress is credited because a pull request merges.
3. The program pipeline lists kritva-core before Mind; that is repository ordering, not a Core interface. Mind's normative dependency is the pinned Sense contract 0.1.0; no Core contract is consumed (C-5).
4. No repository-milestone `depends_on` is introduced here. Cross-phase ordering belongs to the program plan; task dependencies belong to the task definitions below.
5. Mind proposes, Skill authorizes, Motion executes control. Mind never commands an actuator.
6. No ROS 2 dependency in Mind's contract or reasoning layers; an adapter may be provided at the integration boundary later.
7. V2-M6 (physical validation) stays on HOLD. Software acceptance (tests, simulation, mocks, versioned interfaces) is never described as hardware or safety validation.
8. Required GitHub checks stay `secret-scan`, `commit-message-check` and `pr-acceptance-gate`. A `unit-tests` workflow may exist; making it required needs an owner-approved kritva-program pipeline update.

## 2. KOS-MIND-001 closure review

The dispositions, the joint review outcomes and the list of steps that still need the owner are in [reviews/KOS-MIND-001-CLOSURE.md](reviews/KOS-MIND-001-CLOSURE.md). They are contract-level dispositions agreed by the owner in chat on 2026-11-04; no criterion is marked met, and every test item stays NOT_IMPLEMENTED until KOS-MIND-002, 003 and 006.

## 3. Task catalogue

Task IDs KOS-MIND-002 to KOS-MIND-008 are candidates except where [TASKS.md](TASKS.md) lists a row. Dependencies repeat TASKS.md; where the alignment session's order differs, it is noted.

### KOS-MIND-001 Request, context and result contract

| Item | Content |
|---|---|
| State | IN_PROGRESS (owner instruction in chat, 2026-11-02); closure record proposed ([reviews/KOS-MIND-001-CLOSURE.md](reviews/KOS-MIND-001-CLOSURE.md)); milestone V2-M1-MIND-001 |
| L1 scope | Contract, semantics, architecture, criteria AC-001 to AC-011 |
| L2 scope | Schemas under [contract/](../contract/README.md), SEMANTICS.md, COMPATIBILITY.md, examples, Sense pin |
| Inputs, outputs | In: Sense contract 0.1.0, Skill design note. Out: contract 0.1.0-draft, tag `v0.1.0` after approval |
| Dependencies | Upstream: kritva-sense contract (pinned). Downstream: kritva-skill (joint review) |
| Boundary | No validator in the release; no provider, memory, transport |
| Tests, evidence | Review records, AC dispositions (section 2), commit SHA, CI run IDs |
| Not implemented | Joint reviews, owner approvals, completion record |

### KOS-MIND-002 Schema and semantic validator

| Item | Content |
|---|---|
| State | work prepared on a separate branch, not part of the KOS-MIND-001 closure; to be opened as its own pull request after the `v0.1.0` tag, as the owner chose in chat on 2026-11-04; not registered in TASKS.md until then; milestone V2-M2-MIND-001 |
| L1 scope | Deterministic validation of request, context and result |
| L2 scope | Keyword-allowlist JSON Schema validator (D-2), semantic rules of SEMANTICS.md, strict JSON, CLI, `make test-unit`, `unit-tests` workflow |
| Inputs, outputs | In: JSON document and kind. Out: sorted violation list; exit 0, 1 or 2 |
| Dependencies | Upstream: KOS-MIND-001 draft contract. Downstream: 003, 004, 006 |
| Boundary | Not a complete JSON Schema implementation; no provider, no transport, no clock |
| Tests, evidence | criteria V-001 to V-007 in the task file prepared for that pull request; CI run of `unit-tests` on the closing commit |
| Not implemented | `expires_at` against a clock, whole-result digests, context retrieval, wire format of `cancel` |

### KOS-MIND-003 Context lifecycle and Edge/Hybrid conformance

| Item | Content |
|---|---|
| State | NOT_IMPLEMENTED; candidate; V2-M2-MIND-001 |
| L1 scope | Operational checks for AC-009 and AC-010 |
| L2 scope | Lifecycle conformance beyond the pure rules in 002; disconnected-operation tests (candidate profile 30 minutes, not an availability commitment); per-provider-kind conformance without implementing a provider |
| Inputs, outputs | In: recorded contexts and provider stubs. Out: conformance results |
| Dependencies | TASKS.md: KOS-MIND-001 accepted. The alignment session would order it after the validator; the repository's recorded dependency stays authoritative until the owner changes it |
| Boundary | Implements no reasoning provider; no offline-reasoning claim unless a local provider is deployed |
| Tests, evidence | Disconnected-operation and conformance tests; no latency threshold until system requirements exist (UNKNOWN) |

### KOS-MIND-004 Sense integration and regression tests

| Item | Content |
|---|---|
| State | NOT_IMPLEMENTED; candidate; V2-M2-MIND-001 |
| L1 scope | Integration at the real Sense boundary; `make test-integration`, `make test-regression` |
| L2 scope | Observation mapping, freshness and clock handling, error-code mapping, version check against the pinned Sense contract |
| Inputs, outputs | In: Sense samples as the Sense contract defines them. Out: context observation references, usability decisions |
| Dependencies | KOS-MIND-002; an approved Sense contract. Core integration only if Mind consumes a defined, approved Core interface (none today) |
| Boundary | Never imports Sense internals |
| Tests, evidence | Integration and regression suites; a fixed defect adds a regression test |

### KOS-MIND-005 Reasoning adapter and memory interface conformance

| Item | Content |
|---|---|
| State | NOT_IMPLEMENTED; candidate; V2-M5-MIND-001 |
| L1 scope | Provider-independent interface conformance |
| L2 scope | Adapter and memory interface requirements; providers and backends live outside this repository unless decided otherwise |
| Dependencies | KOS-MIND-001 accepted; decision D-4 (memory backend) is open |
| Boundary | No model serving, planning engine or memory persistence inside Mind prematurely; no ROS 2 dependency |
| Tests, evidence | Interface conformance tests; scope UNKNOWN until D-4 |

### KOS-MIND-006 Deterministic replay and execution records

| Item | Content |
|---|---|
| State | NOT_IMPLEMENTED; candidate; V2-M5-MIND-001 |
| L1 scope | AC-011 replay of recorded Mind inputs |
| L2 scope | Replay by replay class; exact equality only for EXACT_REPLAY_SUPPORTED; otherwise a labelled comparison |
| Dependencies | KOS-MIND-002 |
| Boundary | Labelled simulation; the original result stays immutable evidence |
| Tests, evidence | Replay comparison reports; no physical or safety claim |

### KOS-MIND-007 Mind-to-Skill integration

| Item | Content |
|---|---|
| State | NOT_IMPLEMENTED; candidate; V2-M5-MIND-001 |
| L1 scope | Joint capability validation with kritva-skill |
| L2 scope | Proposal resolution, PARTIAL-result handling, cancellation ownership, independent authorization by Skill |
| Dependencies | KOS-MIND-006; an agreed Skill contract; program milestone V2-M3 (control plane) |
| Boundary | Skill authorizes; Mind never executes |
| Tests, evidence | Software-only integration evidence recorded for program acceptance |

### KOS-MIND-008 Security, resource limits and release evidence

| Item | Content |
|---|---|
| State | NOT_IMPLEMENTED; candidate; V2-M8-MIND-001 |
| L1 scope | Release readiness |
| L2 scope | Security review, resource limits, failure recovery, release documentation |
| Dependencies | Earlier tasks; platform authentication boundary (UNKNOWN, not specified) |
| Boundary | Ingress authentication is outside the Mind request schema (C-5) and stays a deployment precondition |
| Tests, evidence | Release evidence on exact commits; independent review is not in place (interim D-047) |

## 4. Open items for the owner

1. KOS-MIND-002 follows KOS-MIND-001 closure (owner choice, chat, 2026-11-04); the validator work is held out of the closure pull request.
2. Whether the local dependency of KOS-MIND-003 on "KOS-MIND-001 accepted" or the alignment session's "after the validator" order applies.
3. Whether the program tasks for V2-M0-MIND-001 and V2-M1-MIND-001 (currently empty in the program plan) are reconciled with TASKS.md through the program process.
4. Whether `unit-tests` should become a required check (program pipeline update).
