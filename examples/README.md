# Mind contract examples (PROPOSED, 0.1.0-draft)

Task: KOS-MIND-001. Examples for the proposed schemas in [contract/](../contract/README.md). They are synthetic: the identifiers, provider and model names, digests and times are made up and describe no real robot, provider or run. [manifest.json](manifest.json) records which schema each example is checked against and the expected outcome.

Valid examples must pass their schema; invalid examples must fail it, and each file demonstrates one rule.

## Valid

| File | Schema |
|---|---|
| [request.json](valid/request.json) | request |
| [context-active.json](valid/context-active.json) | context |
| [context-snapshot-only.json](valid/context-snapshot-only.json) | context |
| [result-completed.json](valid/result-completed.json) | result |
| [result-partial.json](valid/result-partial.json) | result |
| [result-cancelled.json](valid/result-cancelled.json) | result |
| [result-failed-provider-unavailable.json](valid/result-failed-provider-unavailable.json) | result |
| [result-replay-unavailable.json](valid/result-replay-unavailable.json) | result |
| [context-with-observations.json](valid/context-with-observations.json) | context |
| [request-with-freshness.json](valid/request-with-freshness.json) | request |
| [result-partial-stale-input.json](valid/result-partial-stale-input.json) | result |
| [result-two-proposals-with-constraints.json](valid/result-two-proposals-with-constraints.json) | result |
| [result-completed-edge-with-warning.json](valid/result-completed-edge-with-warning.json) | result |

## Invalid

| File | Schema | Why it fails |
|---|---|---|
| [request-missing-context-ref.json](invalid/request-missing-context-ref.json) | request | context_ref is required |
| [context-no-content-or-snapshot.json](invalid/context-no-content-or-snapshot.json) | context | content or snapshot_ref is required |
| [context-revision-zero.json](invalid/context-revision-zero.json) | context | revision starts at 1 |
| [result-authorized-field.json](invalid/result-authorized-field.json) | result | no authorization field exists; unknown fields are rejected |
| [result-failed-without-errors.json](invalid/result-failed-without-errors.json) | result | FAILED needs at least one error |
| [result-partial-without-missing.json](invalid/result-partial-without-missing.json) | result | PARTIAL needs missing[] |
| [result-completed-with-missing.json](invalid/result-completed-with-missing.json) | result | COMPLETED must not list missing |
| [result-score-without-scale.json](invalid/result-score-without-scale.json) | result | a score needs scale, source and calibration |
| [result-bad-digest.json](invalid/result-bad-digest.json) | result | digest must be sha256:<64 hex> |
| [result-missing-provenance.json](invalid/result-missing-provenance.json) | result | provenance is required |
| [result-completed-without-output.json](invalid/result-completed-without-output.json) | result | COMPLETED needs the full execution record, including output |
| [result-partial-attempt-only-provenance.json](invalid/result-partial-attempt-only-provenance.json) | result | PARTIAL needs the full execution record |
| [context-stale-observation-marked-usable.json](invalid/context-stale-observation-marked-usable.json) | context | a STALE, MISSING or INVALID observation must have usable false |
| [context-observation-no-clock.json](invalid/context-observation-no-clock.json) | context | an observation reference carries its clock |
| [request-freshness-now-without-clock.json](invalid/request-freshness-now-without-clock.json) | request | now_ns needs the clock it came from |
| [result-sense-error-code-as-mind-code.json](invalid/result-sense-error-code-as-mind-code.json) | result | a Sense code is not a Mind code; it goes in detail.sense_error_code |
| [result-proposal-without-id.json](invalid/result-proposal-without-id.json) | result | every proposal needs a proposal_id |
| [result-skill-id-uppercase.json](invalid/result-skill-id-uppercase.json) | result | skill_id must be a lowercase dotted name |
| [result-version-constraint-latest.json](invalid/result-version-constraint-latest.json) | result | version_constraint must follow the closed grammar; no tags |
| [result-version-constraint-wildcard.json](invalid/result-version-constraint-wildcard.json) | result | no wildcards in version_constraint |
| [result-version-constraint-prerelease.json](invalid/result-version-constraint-prerelease.json) | result | no pre-release versions in version_constraint |
| [result-negative-priority.json](invalid/result-negative-priority.json) | result | priority starts at 0 |
| [result-input-without-digest.json](invalid/result-input-without-digest.json) | result | the execution record input needs a digest |
| [result-output-without-digest.json](invalid/result-output-without-digest.json) | result | the execution record output needs a digest |
| [result-context-snapshot-without-digest.json](invalid/result-context-snapshot-without-digest.json) | result | a context snapshot needs a digest |
| [result-completed-without-context-snapshot.json](invalid/result-completed-without-context-snapshot.json) | result | COMPLETED needs a context snapshot for replay |
| [result-failed-with-only-warning.json](invalid/result-failed-with-only-warning.json) | result | FAILED needs at least one error of severity ERROR |
| [result-placement-unknown-value.json](invalid/result-placement-unknown-value.json) | result | placement is EDGE, NEXUS or CLOUD |

## What this is not

No validator is part of this repository and no test runs these examples, so `make test-unit` is still NOT_IMPLEMENTED and these files are not evidence for any criterion. On 2026-11-02 they were checked once, by hand, with a third-party JSON Schema validator: all valid examples passed and all invalid examples were rejected (re-checked after the digest, placement and error changes). `format` was not asserted, so timestamp formats are not covered. Automated checking belongs to KOS-MIND-002.
