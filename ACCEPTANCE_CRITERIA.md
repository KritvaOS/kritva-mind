# Acceptance Criteria: kritva-mind

Standard: kritva-program `v2/planning/ACCEPTANCE_STANDARD.md` (proposed; approval pending PD-005, PD-006). Criteria below are for task KOS-MIND-001 (Mind request, context and result contract) and are proposed until the owner approves the task. Nothing here is accepted, weighted or credited.

## 1. Purpose and scope

Owns: the Mind request, context and result contract: inputs, context identity, output schema, uncertainty and error reporting, cancellation and deterministic validation.

Does not own: sensing (kritva-sense), motion (kritva-motion), skill orchestration (kritva-skill), and the platform foundation (kritva-core).

## 2. Normative dependencies

kritva-sense (versioned Sense contract), pinned below. No Core contract is a normative dependency of this contract (decision C-5); kritva-core precedes Mind in the program's repository ordering, which is a separate matter. Exact versions or commit SHAs are recorded here when the contracts they refer to are approved.

| Dependency | Pinned version | Identified by | Recorded |
|---|---|---|---|
| kritva-sense | Sense contract 0.1.0 (`contract/SENSE_CONTRACT.md`) | tag `v0.2.0`, commit `543f5743d6ffd8fa1ed1ee5fdbf8295ae6a69a77` (the contract is unchanged from tag `v0.1.0`, commit `07c48d5398bea19e58f7bd4c7a5af55041b28df5`) | owner decision in chat, 2026-11-02; no separate approval record |
| kritva-core | none | no Core contract is consumed by the draft schemas; Core states it does not authenticate entities (confirmed by the owner in chat, 2026-11-03; no separate approval record) | |

The Sense contract is approved by the owner under the interim D-047 review and is still a 0.x contract that Sense may change with a changelog entry and a decision. A change to the pinned version here is a criteria change and needs its own review.

## 3. Functional criteria (KOS-MIND-001)

| ID | Criterion (testable) | Verified by |
|---|---|---|
| AC-001 | Request, context and result have versioned schemas; context carries a stable identity. | contract review, schema tests |
| AC-002 | Results report uncertainty and errors in defined fields; no failure is silent. `errors[]` may appear with any status; a FAILED result carries at least one error of severity ERROR. | contract review now; error-path tests in KOS-MIND-002 |
| AC-003 | Cancellation is specified as a transport-independent operation with defined outcomes for non-terminal and terminal requests, including partial results ([contract/SEMANTICS.md](contract/SEMANTICS.md) section 1). | contract review now; cancellation tests in KOS-MIND-002 |
| AC-004 | Validation is deterministic: the same input and context give the same validation outcome. | determinism tests |
| AC-005 | Mind consumes Sense only through the versioned Sense contract, never its internals. | dependency review |
| AC-006 | [ARCHITECTURE.md](ARCHITECTURE.md) is reviewed and states subsystem responsibilities, data flow and the open decisions it leaves; it is not an accepted baseline until the owner approves it. | architecture review |
| AC-007 | The result is a proposal: the contract has no field that commands an actuator, and execution authority is stated to belong to Skill, which independently authorizes. Proposals carry a stable correlation handle. Mind's JSON request does not authenticate its caller. The Mind-to-Skill interaction, including the changes Skill's design note requests, is reviewed with kritva-skill. | contract review, cross-repository review |
| AC-008 | Context identity has a defined lifecycle with legal transitions, revisions are immutable, and a result carries the context identity and provenance of its inputs ([contract/SEMANTICS.md](contract/SEMANTICS.md) section 2). | contract review now; schema and lifecycle tests in KOS-MIND-002 and KOS-MIND-003 |
| AC-009 | Edge resilience, contract level: the contract has no cloud dependency; an unavailable provider is reported explicitly; stale context is never silently substituted; cancelling a request needs no cloud connection. No claim of offline reasoning unless a local provider is deployed. The operational disconnected-operation tests (candidate profile: 30 minutes, not an availability commitment) are KOS-MIND-003 and are not part of this task. | contract review now; disconnected-operation tests in KOS-MIND-003 (NOT_IMPLEMENTED) |
| AC-010 | Hybrid compatibility, contract level: the contract is independent of whether a provider runs on Edge, Nexus or Cloud; a provider change is recorded in provenance (`provider_id`, and `placement` when known); context identity and revision are preserved across deployments. No latency threshold is set until system requirements exist; timestamps, timeouts and deadline outcomes are recorded. Conformance tests per provider kind are KOS-MIND-003 and are not part of this task. | contract review now; conformance tests in KOS-MIND-003 (NOT_IMPLEMENTED) |
| AC-011 | Provenance and replay: the execution record carries digests for input and output, a context snapshot with digest for COMPLETED and PARTIAL results, and a replay class; failures that never reached inference carry an attempt-only record ([contract/SEMANTICS.md](contract/SEMANTICS.md) section 5). | schema review now; schema tests in KOS-MIND-002; replay comparison in KOS-MIND-006 |

## 4. Interface and API compatibility

The contract defines inputs, outputs, error handling, versioning and lifecycle, with time and units stated. Contracts are versioned independently of program phases. Depends on the Sense contract version pinned in section 2; no Core contract is consumed (C-5); must not import sense internals.

## 5. Test gates

| Gate | Command | Required result | State |
|---|---|---|---|
| Unit | `make test-unit` | all pass | NOT_IMPLEMENTED until KOS-MIND-002 (Schema validation, cancellation and error-path tests) |
| Integration | `make test-integration` | all pass, real dependency boundaries | NOT_IMPLEMENTED |
| Regression | `make test-regression` | all pass, suite unchanged by the change | NOT_IMPLEMENTED |
| Structure | `make check` | planning files present, commit checker self-test passes | implemented |

An unimplemented gate is reported as NOT_IMPLEMENTED and is never counted as a pass. No coverage threshold is set; one needs an approved decision.

## 6. Specialised gates

Determinism and error-path behaviour apply to every criterion above. No hardware-in-loop or physical validation applies: any such claim stays gated on program milestone V2-M6 (HOLD).

## 7. Evidence requirements

Immutable commit SHAs, CI run IDs for secret-scan, commit-message-check and the test gates, and the review record against the closing commit.

## 8. Definition of Done

As in the program standard section 1: stable task ID, merged through the approved PR, required checks green on the exact closing commit, reviews recorded, documentation and changelog updated, immutable evidence, no blocker converted into a pass.

## 9. Known limitations and exclusions

- No implementation exists; criteria are not yet testable by automated gates (gates listed NOT_IMPLEMENTED).
- The architecture and safety reviewer roles are held by the owner on an interim basis (program decision D-047, resolving PD-007); independent review is not yet in place.
- Licence: Apache-2.0, confirmed by the owner (program decision D-064, closing PD-013).

## 10. Change control

Accepted criteria are never edited. A change is a new criteria version with its own review; accepted evidence keeps the version it was produced under.
