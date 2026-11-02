# Mind contract (PROPOSED, 0.1.0-draft)

Task: KOS-MIND-001. These JSON Schemas (JSON Schema draft 2020-12) describe the Mind request, context and result. They are a proposed contract artifact: not accepted, not released, and not an interface other repositories may rely on. The design is in [ARCHITECTURE.md](../ARCHITECTURE.md); the criteria are in [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md).

| File | Describes |
|---|---|
| [mind-request.schema.json](mind-request.schema.json) | a request to interpret a task in a context |
| [mind-context.schema.json](mind-context.schema.json) | one immutable revision of a context |
| [mind-result.schema.json](mind-result.schema.json) | a proposal, with uncertainty, errors and provenance |
| [mind-common.schema.json](mind-common.schema.json) | shared definitions (references, uncertainty, errors, proposed skill, execution record) |

## Rules the schemas encode

- **A result is a proposal.** There is no `authorized` or `execute` field and unknown fields are rejected. Skill resolves, validates and authorizes.
- **One completeness indicator.** The draft in the architecture document had both `status` and `completeness`; this version keeps `status` (COMPLETED, PARTIAL, FAILED, CANCELLED) and adds `missing[]`, required for PARTIAL and CANCELLED and forbidden for COMPLETED. FAILED requires at least one error. This is a proposal for review.
- **Context identity.** `context_id` and `revision` are immutable; an update is a new revision. A context carries `content` or a `snapshot_ref`. Cancellation is an event of a request, not a context state.
- **Uncertainty.** A `score` needs its `scale`, `source` and `calibration`.
- **Provenance.** Always present. Only the replay class and the input are always required; a COMPLETED or PARTIAL result must also carry provider and model identity, the output reference with digest and the execution time. A FAILED or CANCELLED result that never reached inference carries an attempt-only record, so no model or output is invented. The record also holds configuration and prompt digests; `random_seed` is optional.
- **Sense observations.** A context may list `observations[]`: references to Sense samples by `sensor_id`, `sequence`, `clock`, `timestamp_ns` and `validity`, with the Sense contract version they follow and Mind's own `usable` decision. A STALE, MISSING or INVALID observation must have `usable` false, because Sense says such measurements are not readings. Clocks are never compared across `monotonic` and `utc`.
- **Freshness.** `constraints.freshness` in a request states `max_age_ns` (with an optional per-sensor override), and, when freshness is to be evaluated, the consumer's `now_ns` and its `clock`. Without them freshness is not evaluated, as in Sense section 6.1.
- **Error codes.** `errors[].code` is one of `MIND_INPUT_STALE`, `MIND_INPUT_MISSING`, `MIND_INPUT_INVALID`, `MIND_PROVIDER_UNAVAILABLE`, `MIND_TIMEOUT`, `MIND_CANCELLED`, `MIND_CONTRACT_VIOLATION`. A Sense code seen on an input goes in `detail.sense_error_code`. A new code is a contract change.
- **Time and units.** Timestamps are RFC 3339 date-time; durations carry their unit in the name (`_ms`).
- **Versioning.** `contract_version` is SemVer. A breaking change needs a new MAJOR version, a changelog entry and an approved decision. The `$id` values are URNs ending in the draft version; they are identifiers, not locations.

## Limits

- Schema validity is not safety, and a score is not evidence of correctness.
- `format` (for example `date-time`) is only an annotation unless the validator is configured to assert it. Which validator and settings are used is open decision D-2, for KOS-MIND-002.
- No validator exists in this repository, so `make test-unit` is still NOT_IMPLEMENTED. The schemas were checked once by hand with a third-party validator against throwaway samples; that is not a test gate and is not evidence for any criterion.
- Dependencies on the Core and Sense contract versions are not pinned: those contracts are not approved. Sense observations are referenced through `source_refs` with `source_contract`, never embedded as Sense internals.
- Examples, and the joint review with kritva-skill and kritva-sense, are the next steps and are not done.
