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

## 6. What is not verified

No validator exists. The examples in [../examples/](../examples/README.md) were checked once, by hand, with a third-party validator that is not part of this repository. The rules above that JSON Schema cannot express are tested only when KOS-MIND-002 exists.
