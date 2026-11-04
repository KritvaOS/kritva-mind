# Mind contract semantics (PROPOSED, 0.1.0-draft)

Task: KOS-MIND-001. Rules that the JSON Schemas cannot express, written so that a validator and a consumer can implement them without guessing. Proposed, not accepted, not reviewed by anyone but the owner (interim D-047). Nothing here is implemented: no validator or runtime exists, and these rules are not hardware or safety validation. The schemas are in this folder; see [README.md](README.md).

## 1. Cancellation (AC-003)

Cancellation is an operation, independent of transport.

| Item | Rule |
|---|---|
| Operation | `cancel(request_id)`. It names one request. It does not stop other requests. |
| Who | Whoever the platform boundary authorizes to act on that request. Mind does not authenticate callers (decision C-5) and does not trust a caller identity in the payload. |
| Non-terminal request | Mind stops further work as soon as it can and the result ends with status CANCELLED and a non-empty `missing[]` saying what was not produced. Proposals produced before the cancellation are kept in the result but are not to be executed. |
| Terminal request | A request that already has a COMPLETED, PARTIAL, FAILED or CANCELLED result is unchanged. A late cancel never rewrites a result. |
| Repeated cancel | Idempotent: the same outcome as the first. |
| Provenance | If no inference ran, the result carries an attempt-only execution record (replay class and input). If inference had started, the record may be full or attempt-only according to what actually happened; nothing is invented. |
| No cloud dependency | Cancelling a request needs no cloud connection (AC-009 design constraint). |
| Not defined here | The wire format of the operation and its acknowledgement; a transport and API are decided separately. |

## 2. Context lifecycle (AC-008)

A context is a sequence of immutable revisions identified by `context_id` and `revision`. `lifecycle_state` is a property of one revision.

| From | To | Rule |
|---|---|---|
| (none) | CREATED | Revision 1. |
| CREATED | ACTIVE | The context is in use. |
| ACTIVE | ACTIVE | An update creates a new revision (previous plus 1) with new `updated_at`. The earlier revision is never changed. |
| ACTIVE | SNAPSHOTTED | A new revision recording a snapshot reference and digest. |
| SNAPSHOTTED | ACTIVE | A further update creates a new revision. |
| CREATED, ACTIVE, SNAPSHOTTED | CLOSED | Closed by its owner. Terminal. |
| CREATED, ACTIVE, SNAPSHOTTED | EXPIRED | `expires_at` has passed. Terminal. |

- `revision` increases by exactly 1 per change, and `created_at` never changes.
- A revision in CLOSED or EXPIRED is not usable as the context of a new request: Mind returns FAILED with `MIND_INPUT_INVALID`. A request that already ran keeps the revision it used, so provenance stays valid.
- Cancellation is an event of a request, never a context state.
- Which backend stores contexts is not defined here (decision D-3, D-4).

## 3. Version constraints (`VersionConstraint`)

- Exact `X.Y.Z` matches only that version.
- Caret `^X.Y.Z` matches versions at or above `X.Y.Z` with the same MAJOR when MAJOR is not 0, and with the same MINOR when MAJOR is 0.
- Range `>=A.B.C <D.E.F` matches versions at or above the lower bound and strictly below the upper bound. A range whose lower bound is not strictly below its upper bound is invalid and is rejected by the validator.
- Pre-release and build suffixes, wildcards and tags such as `latest` are not part of the grammar.
- These rules are defined by this contract and are not left to a SemVer library's default behaviour.

## 4. Proposal rules the validator must check

- `proposal_id` is unique within one result.
- Consumers order proposals by `priority` ascending (0 first), then by `proposal_id` ascending by code point. A proposal with no `priority` comes after every proposal that has one. The array order is not authoritative.
- The proposals of a PARTIAL result are advisory. A consumer must not execute them unless its own policy says so explicitly. Proposals of FAILED and CANCELLED results are not to be executed.

## 5. Replay evidence (AC-011)

- The execution record's `input` and `output`, and a `context_snapshot` when present, carry a digest. A COMPLETED or PARTIAL result must carry a `context_snapshot`, so a replay can reconstruct the recorded context.
- `placement` (EDGE, NEXUS or CLOUD) is optional and records where the provider ran when that is known.
- Replay fidelity is stated by `replay_class`. Equality of outputs is required only for EXACT_REPLAY_SUPPORTED.

## 6. Observations from Sense (drafted after the Sense review)

Proposals answering the findings of the draft Sense review record `planning/reviews/KOS-MIND-001-SENSE-REVIEW.md` (kritva-mind pull request 22, not merged when this was written). Not accepted.

- **Sense rules apply unchanged.** Mind does not redefine Sense contract sections 6 and 6.1. Freshness is evaluated only when the consumer's now, its clock and `max_age_ns` are all given; an age equal to the limit is fresh; a sample newer than now, or from a different clock, is not usable (Sense `INVALID_TIMESTAMP`). Without a freshness policy, `usable` reflects validity only and Mind must not claim the observation is fresh.
- **`usable` (validator rule).** `usable` is true only if the validity is VALID and, when freshness was evaluated, the sample is fresh and from the same clock. The schema forces `usable` false for STALE, MISSING and INVALID; the rest needs the freshness inputs and belongs to the validator.
- **`sense_error_code`.** A STALE, MISSING or INVALID observation carries the Sense `error_code` unchanged in `sense_error_code` when it is known; a VALID observation never does. It is never used as a Mind error code.
- **Error mapping.** When an input prevents or limits a result, the Mind error code and the Sense code in `detail.sense_error_code` are:

| Sense error code | Mind code |
|---|---|
| `STALE_DATA` | `MIND_INPUT_STALE` |
| `MISSING_DATA` | `MIND_INPUT_MISSING` |
| `INVALID_DATA`, `INVALID_TIMESTAMP`, `SEQUENCE_REGRESSION`, `UNKNOWN_FRAME`, `INVALID_UNIT`, `NON_FINITE_VALUE`, `MISSING_FIELD`, `MALFORMED_FIELD`, `UNKNOWN_FIELD`, `INVALID_SENSOR_ID`, `INVALID_VALIDITY`, `UNSUPPORTED_CONTRACT_VERSION` | `MIND_INPUT_INVALID` |
| any code not listed (for example from a later Sense version) | `MIND_INPUT_INVALID` |

  When Mind itself finds an observation too old, it uses `MIND_INPUT_STALE` with `STALE_DATA`; a future or cross-clock timestamp is `MIND_INPUT_INVALID` with `INVALID_TIMESTAMP`.
- **Version.** `source_contract` is the Sense contract version the sample follows. The schemas accept any SemVer string; a validator may reject a value other than the Sense contract version this Mind release names. The pinned version is recorded in the criteria, not enforced by the schemas.
- **`max_age_ns`.** Sense states no minimum, so the schema imposes none above 0.

## 7. Identifiers and digests

- **Identifier character set.** Every identifier (`request_id`, `result_id`, `context_id`, `proposal_id`, `skill_id` parts excepted, `correlation_id`) uses 1 to 128 characters from `A-Z a-z 0-9 . _ : -`, the character set Motion uses, so a consumer can derive a Motion identifier without encoding.
- **Whole-result digests.** The contract defines digests inside the execution record only. It defines no digest of a whole result. A consumer that computes one (for example Skill's `mind_result_digest`) holds a local value; if two parties must compare such digests they must compute them over the RFC 8785 canonical JSON form of the result, which this contract recommends but does not require.
- **Retrieval.** How a consumer retrieves a context or snapshot from a reference (`context_ref`, `snapshot_ref`, `context_snapshot`) is not defined here; it depends on the transport and platform decisions that are not made.

## 8. What is not verified

No validator exists. The examples in [../examples/](../examples/README.md) were checked once, by hand, with a third-party validator that is not part of this repository. The rules above that JSON Schema cannot express are tested only when KOS-MIND-002 exists.
