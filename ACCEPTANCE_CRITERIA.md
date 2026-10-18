# Acceptance Criteria: kritva-mind

Standard: kritva-program `v2/planning/ACCEPTANCE_STANDARD.md` (proposed; approval pending PD-005, PD-006). Criteria below are for task KOS-MIND-001 (Mind request, context and result contract) and are proposed until the owner approves the task. Nothing here is accepted, weighted or credited.

## 1. Purpose and scope

Owns: the Mind request, context and result contract: inputs, context identity, output schema, uncertainty and error reporting, cancellation and deterministic validation.

Does not own: sensing (kritva-sense), motion (kritva-motion), skill orchestration (kritva-skill), and the platform foundation (kritva-core).

## 2. Normative dependencies

kritva-core (approved contract), kritva-sense (versioned Sense contract). Exact versions or commit SHAs are recorded here when the contracts they refer to are approved; none are pinned yet.

## 3. Functional criteria (KOS-MIND-001)

| ID | Criterion (testable) | Verified by |
|---|---|---|
| AC-001 | Request, context and result have versioned schemas; context carries a stable identity. | contract review, schema tests |
| AC-002 | Results report uncertainty and errors in defined fields; no failure is silent. | error-path tests |
| AC-003 | Cancellation is specified and tested, including partial results. | cancellation tests |
| AC-004 | Validation is deterministic: the same input and context give the same validation outcome. | determinism tests |
| AC-005 | Mind consumes Sense only through the versioned Sense contract, never its internals. | dependency review |

## 4. Interface and API compatibility

The contract defines inputs, outputs, error handling, versioning and lifecycle, with time and units stated. Contracts are versioned independently of program phases. Depends on core and sense contract versions; must not import sense internals.

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
- No architecture or safety reviewer is assigned (program decision PD-007).
- Licence for this repository is undecided (program decision PD-013).

## 10. Change control

Accepted criteria are never edited. A change is a new criteria version with its own review; accepted evidence keeps the version it was produced under.
