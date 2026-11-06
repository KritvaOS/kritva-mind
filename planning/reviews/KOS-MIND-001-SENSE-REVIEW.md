# Review record: Mind and Sense observation mapping (KOS-MIND-001)

Status: OUTCOME AGREED BY THE OWNER IN CHAT (2026-11-04), not an independent review. The cross-read findings below are an AI-assisted reading; each disposition records the owner's overall outcome, given in chat with no separate approval record. Nothing here is an acceptance of any criterion, and it earns no credit or weight. This record is evidence for task KOS-MIND-001 ([TASK.md](../../tasks/KOS-MIND-001/TASK.md)). It is kept in kritva-mind because it documents Mind's dependency; no change to kritva-sense is needed to record it.

## 1. Scope and revisions

| Item | Value |
|---|---|
| Reviewed | How the Mind contract refers to Sense data: `ObservationRef`, `FreshnessPolicy`, the validity and `usable` rule, the error mapping and the `sensor_id` pattern, against the pinned Sense contract. |
| Mind revision | kritva-mind `main`, commit `1bb7899e2836560e734c0ca870ae4a2bb0e17f2f`, read 2026-11-03: `contract/mind-common.schema.json`, `contract/mind-context.schema.json`, `contract/mind-request.schema.json`, `contract/COMPATIBILITY.md` |
| Sense contract | Sense contract 0.1.0 (`contract/SENSE_CONTRACT.md` and `contract/sense-sample.schema.json`) at tag `v0.2.0`, commit `543f5743d6ffd8fa1ed1ee5fdbf8295ae6a69a77`, as pinned in [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md) section 2. The contract is reported unchanged from tag `v0.1.0`, commit `07c48d5398bea19e58f7bd4c7a5af55041b28df5`. |
| Sections read | Sense contract sections 3 to 9: sample fields, time, frames, validity and stale data (including 6.1 checks that need context), errors, lifecycle, versioning |

The Sense contract is approved by the owner under the interim D-047 review and is a 0.x contract that Sense may change with a changelog entry and a decision. If the pinned commit or the Mind revision changes before the criteria review (PR-4), update this record and re-check.

Refresh, 2026-11-06 (AI-assisted; the owner is the only reviewer, D-047): the Mind side was re-read against kritva-mind `main` commit `b59f767268b77075a0ea693f9346d34d9fef83c5` (pull request 25 merged; `unit-tests` run 42215995601 succeeded on it). Pull request 25 changed nothing under `contract/` or `examples/`, so the contract text equals the text at `d821319caea42a22633d7219dc3c237be712fb3a` (pull request 24 merged), which already held the pull request 23 changes that answer SE-5 to SE-10: `sense_error_code`, `max_age_ns` minimum 0, the 1 to 128 character identifier pattern, and SEMANTICS.md sections 6 and 7. The schema definitions and the error-mapping table were checked against the positions in the closure record on that date and they still hold; no finding changed. The validator merged in pull request 25 has unit tests for the `usable` rule, an age equal to the limit, a zero `max_age_ns`, the error mapping and the pinned Sense version option (`tests/validator/test_semantics.py`, classes `ObservationUsable` and `ErrorMapping`); they test Mind's own rules only. Still true: nothing was run against a Sense validator or a real Sense sample, the Sense side has not reviewed the mapping, and the Sense pin in [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md) was not re-fetched from kritva-sense for this refresh.

## 2. Reviewer, method and independence

- **Reviewer:** Dinesh, as repository owner and interim architecture reviewer under program decision D-047, acting also in the interim Sense review role if that is the actual arrangement. This record is drafted for that review; the owner's reading and dispositions are still to be recorded. It is not "Sense independent approval".
- **Method:** AI-assisted cross-read of the identified public repository revisions, followed by owner examination and disposition of the findings. AI assistance is supporting analysis only; it is not an approver or independent reviewer.
- **Independence:** this is not an independent review and none is claimed.
- **Nothing was executed**, and no Sense validator was run. One mechanical comparison was made by script (the identifier pattern).

## 3. Review questions and findings

Cross-read result uses the labels CONFIRMED (Mind says the same as Sense), CHANGE REQUIRED, or NOT SPECIFIED (Sense or Mind does not say).

| ID | Topic | Cross-read result | Evidence | Mind action proposed | Owner disposition |
|---|---|---|---|---|---|
| SE-1 | `sensor_id` pattern | CONFIRMED | Mind `ObservationRef.sensor_id` and the keys of `per_sensor_max_age_ns` use the same regular expression as Sense section 3 (`^[a-z][a-z0-9_]{0,31}(\.[a-z0-9_]{1,32}){0,3}$`); compared by script | none | AGREED (owner, chat, 2026-11-04) |
| SE-2 | Identity fields | CONFIRMED | `sensor_id`, `sequence` (integer, at least 0) and `timestamp_ns` (integer, at least 0, nanoseconds) correspond to Sense `sensor_id`, `sequence` and `timestamp.value` with `unit` `ns` | none | AGREED (owner, chat, 2026-11-04) |
| SE-3 | Clock | CONFIRMED | Mind `clock` is `monotonic` or `utc`, as Sense section 4. Sense says samples and the consumer's now must come from the same clock; Mind's `FreshnessPolicy` requires `clock` whenever `now_ns` is given | none | AGREED (owner, chat, 2026-11-04) |
| SE-4 | Validity values | CONFIRMED | `VALID`, `STALE`, `MISSING`, `INVALID` are the same four values as Sense section 6 | none | AGREED (owner, chat, 2026-11-04) |
| SE-5 | `usable` rule | NOT SPECIFIED | The schema forces `usable` false when validity is STALE, MISSING or INVALID (Sense: such measurements are not usable as readings). It cannot force `usable` false for a `VALID` sample that is stale under the freshness policy, because that needs the consumer's now. No rule in `SEMANTICS.md` covers the observation `usable` flag | add a validator rule: `usable` must be false when the freshness policy was evaluated and the sample is older than allowed, or when a future timestamp or clock mismatch was found | AGREED (owner, chat, 2026-11-04) |
| SE-6 | Freshness | NOT SPECIFIED | Sense section 6.1: freshness needs the consumer's now, its clock and `max_age_ns`; without them it is not evaluated; an age equal to the limit is fresh; a sample newer than the consumer's clock is `INVALID_TIMESTAMP`. Mind mirrors the inputs but does not say whether it applies these edge rules unchanged | state in the contract that Mind applies Sense section 6.1 unchanged and does not redefine it | AGREED (owner, chat, 2026-11-04) |
| SE-7 | `max_age_ns` minimum | NOT SPECIFIED | Mind requires `max_age_ns` of at least 1. Sense states no minimum | keep, or drop the minimum to avoid being stricter than Sense | AGREED (owner, chat, 2026-11-04) |
| SE-8 | Sense error code | CHANGE REQUIRED | Sense requires an `error_code` on every sample that is not `VALID`. `ObservationRef` has no field for it, so it survives only in an error's `detail.sense_error_code`, which is not required | decide: add an optional `sense_error_code` to `ObservationRef`, or accept the loss and say so | AGREED (owner, chat, 2026-11-04) |
| SE-9 | Error mapping | NOT SPECIFIED | Sense defines 14 error codes (for example `SEQUENCE_REGRESSION`, `INVALID_TIMESTAMP`, `UNKNOWN_FRAME`, `STALE_DATA`). Mind has three input codes (`MIND_INPUT_STALE`, `MIND_INPUT_MISSING`, `MIND_INPUT_INVALID`) and no table saying which Sense code maps to which | write the mapping table, or state that only the three Sense data-state codes are mapped and others are `MIND_INPUT_INVALID` | AGREED (owner, chat, 2026-11-04) |
| SE-10 | Version enforcement | NOT SPECIFIED | `ObservationRef.source_contract` accepts any SemVer string. Sense's validator supports exactly the versions it lists, and a 0.x MINOR may break. The pin in the criteria is not enforced by the schemas | record as a limitation; the validator task may check the value against the pinned version | AGREED (owner, chat, 2026-11-04) |
| SE-11 | Reliance on public contract only | CONFIRMED | The Mind schemas refer to Sense by `sensor_id`, `sequence`, clock, timestamp, validity and contract version only. They do not use Sense internals, and measurement values inside a context `content` are opaque to Mind | none; measurement content is not checked by Mind | AGREED (owner, chat, 2026-11-04) |
| SE-12 | Assumptions stronger than Sense's guarantees | NOT SPECIFIED | The only candidates found are SE-5 and SE-7. The frame and unit conventions are not restated by Mind | none beyond SE-5 and SE-7 | AGREED (owner, chat, 2026-11-04) |

## 4. Outcome

Outcome: **AGREED** (owner, in chat, 2026-11-04; no separate approval record). The position of each finding is in [KOS-MIND-001-CLOSURE.md](KOS-MIND-001-CLOSURE.md). The revisions in section 1 are older than the closing commit and must be re-checked before the completion record.

For the owner's consideration: SE-1 to SE-4 and SE-11 are confirmed. SE-8 is the only finding that may need a schema change; SE-5, SE-6, SE-7, SE-9, SE-10 and SE-12 need a decision to either write a rule or record a limitation. A required change to the Sense contract itself would be tracked as a dependency issue for Sense and must not be reinterpreted inside Mind.

## 5. Not verified

- No Sense validator was run and no real Sense sample was read; the comparison is between documents and schemas.
- Whether the Sense side agrees with the mapping: nobody on that side has reviewed it, and the owner holds that role on an interim basis (D-047).
- Sense's history beyond the two tags was not inspected.
