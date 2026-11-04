# Mind contract (PROPOSED, 0.1.0-draft)

Task: KOS-MIND-001. These JSON Schemas (JSON Schema draft 2020-12) describe the Mind request, context and result. They are a proposed contract artifact: not accepted, not released, and not an interface other repositories may rely on. The design is in [ARCHITECTURE.md](../ARCHITECTURE.md); the criteria are in [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md).

| File | Describes |
|---|---|
| [mind-request.schema.json](mind-request.schema.json) | a request to interpret a task in a context |
| [mind-context.schema.json](mind-context.schema.json) | one immutable revision of a context |
| [mind-result.schema.json](mind-result.schema.json) | a proposal, with uncertainty, errors and provenance |
| [SEMANTICS.md](SEMANTICS.md) | rules JSON Schema cannot express: cancellation, context lifecycle, version-constraint semantics, proposal ordering, replay evidence |
| [mind-common.schema.json](mind-common.schema.json) | shared definitions (references, uncertainty, errors, proposed skill, execution record) |

## Rules the schemas encode

- **A result is a proposal.** There is no `authorized` or `execute` field and unknown fields are rejected. Skill resolves, validates and authorizes.
- **One completeness indicator.** The draft in the architecture document had both `status` and `completeness`; this version keeps `status` (COMPLETED, PARTIAL, FAILED, CANCELLED) and adds `missing[]`, required for PARTIAL and CANCELLED and forbidden for COMPLETED. FAILED requires at least one error. This is a proposal for review.
- **Context identity.** `context_id` and `revision` are immutable; an update is a new revision. A context carries `content` or a `snapshot_ref`. Cancellation is an event of a request, not a context state.
- **Uncertainty.** A `score` needs its `scale`, `source` and `calibration`.
- **Errors.** `errors[]` may appear with any status; a FAILED result carries at least one error of severity ERROR.
- **Provenance.** Always present. Only the replay class and the input are always required; a COMPLETED or PARTIAL result must also carry provider and model identity, the output reference with digest, the execution time and a context snapshot with digest. `input`, `output` and `context_snapshot` always carry a digest, and `placement` (EDGE, NEXUS or CLOUD) is optional. A FAILED or CANCELLED result that never reached inference carries an attempt-only record, so no model or output is invented. The record also holds configuration and prompt digests; `random_seed` is optional.
- **Sense observations.** A context may list `observations[]`: references to Sense samples by `sensor_id`, `sequence`, `clock`, `timestamp_ns` and `validity`, with the Sense contract version they follow and Mind's own `usable` decision. A STALE, MISSING or INVALID observation must have `usable` false, because Sense says such measurements are not readings. Clocks are never compared across `monotonic` and `utc`.
- **Freshness.** `constraints.freshness` in a request states `max_age_ns` (with an optional per-sensor override), and, when freshness is to be evaluated, the consumer's `now_ns` and its `clock`. Without them freshness is not evaluated, as in Sense section 6.1.
- **Error codes.** `errors[].code` is one of `MIND_INPUT_STALE`, `MIND_INPUT_MISSING`, `MIND_INPUT_INVALID`, `MIND_PROVIDER_UNAVAILABLE`, `MIND_TIMEOUT`, `MIND_CANCELLED`, `MIND_CONTRACT_VIOLATION`. A Sense code seen on an input goes in `detail.sense_error_code`. A new code is a contract change.
- **Proposals.** Each `proposed_skills[]` entry has a `proposal_id` that is unique within the result (a validator rule; JSON Schema cannot express it), a `skill_id` in the lowercase dotted shape also used for Sense sensor ids, and an optional `version_constraint` from a closed grammar: exact `1.2.3`, caret `^1.2.0`, or range `>=1.2.0 <2.0.0`; no wildcards, tags or pre-release versions. A constraint selects among versions the consumer already holds and is never a pin or an approval.
- **Priority.** A lower `priority` is preferred (0 first). Equal and absent priorities are ordered by ascending `proposal_id`, and a proposal with no priority comes after every proposal that has one. Priority orders candidates and grants no authority.
- **Preconditions.** A Mind precondition is an informational claim; `expression` is never evaluated by Mind or Skill. A consumer-defined precondition that must be resolved is named by `precondition_id`.
- **PARTIAL results.** Their proposals are advisory; `missing[]` says what Mind lacked, and a consumer must not execute them unless its own policy says so. Proposals of FAILED or CANCELLED results are not to be executed.
- **Observations.** `observations[]` may carry the Sense `error_code` as `sense_error_code` (never for a VALID observation); the rules for `usable`, the Sense-to-Mind error mapping and the version check are in [SEMANTICS.md](SEMANTICS.md) section 6. `max_age_ns` may be 0.
- **Identifiers.** All identifiers use 1 to 128 characters from `A-Z a-z 0-9 . _ : -`, matching Motion's. Whole-result digests and context retrieval are not defined ([SEMANTICS.md](SEMANTICS.md) section 7).
- **Time and units.** Timestamps are RFC 3339 date-time; durations carry their unit in the name (`_ms`).
- **Versioning.** `contract_version` is SemVer. A breaking change needs a new MAJOR version, a changelog entry and an approved decision. The `$id` values are URNs ending in the draft version; they are identifiers, not locations.

## Limits

- Ingress authentication is a recorded known limitation: Mind does not authenticate callers, the platform boundary is not yet specified, and Mind must not be exposed to untrusted callers until it is (see [COMPATIBILITY.md](COMPATIBILITY.md)).
- Schema validity is not safety, and a score is not evidence of correctness.
- `format` (for example `date-time`) is only an annotation unless the validator is configured to assert it. Which validator and settings are used is open decision D-2, for KOS-MIND-002.
- No validator exists in this repository, so `make test-unit` is still NOT_IMPLEMENTED. The schemas were checked once by hand with a third-party validator against throwaway samples; that is not a test gate and is not evidence for any criterion.
- Dependencies: the Sense contract 0.1.0 is pinned in [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) section 2 (tag `v0.2.0`); the draft schemas do not enforce that version. No Core contract is consumed or pinned: Core documents that it does not authenticate entities, and Mind needs no other Core interface so far (confirmed by the owner in chat, 2026-11-03). Sense observations are referenced through `observations[]` and `source_refs`, never embedded as Sense internals.
- Examples exist ([../examples/](../examples/README.md)) but were only checked by hand. The joint review with kritva-skill and kritva-sense is not complete: nobody but the owner has reviewed either side.
