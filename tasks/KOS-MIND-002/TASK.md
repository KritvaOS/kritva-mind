# KOS-MIND-002: Mind contract validator

Status: IN_PROGRESS. The owner instructed the start in chat on 2026-11-03 ("Discuss your proposal and align and start implementing the task", after the ChatGPT alignment session named KOS-MIND-002 as the first implementation task); no separate approval record exists in this repository. The task carries no weight and earns no credit (see [planning/TASKS.md](../../planning/TASKS.md)). Milestone: V2-M2-MIND-001 (proposed).

Prerequisite not met: [planning/TASKS.md](../../planning/TASKS.md) listed "KOS-MIND-001 accepted" as the dependency. KOS-MIND-001 is still IN_PROGRESS, so this work validates the proposed contract 0.1.0-draft and is built to change with it. A contract change made while closing KOS-MIND-001 needs a validator change in the same pull request. On 2026-11-06 the owner decided in chat that this task lands before the KOS-MIND-001 completion record and the `v0.1.0` tag, so that the release includes the validator and `make test-unit` gives real evidence. Before that completion record is written, the texts that say no validator is included (limitation 2 in [the closure record](../../planning/reviews/KOS-MIND-001-CLOSURE.md) and the validation-limitation release-note text in [tasks/KOS-MIND-001/TASK.md](../KOS-MIND-001/TASK.md)) must be re-read against this change; this task does not edit them. Nothing here makes any KOS-MIND-001 criterion accepted.

Scope source: candidate row KOS-MIND-002 in the earlier version of [planning/TASKS.md](../../planning/TASKS.md); decision D-2 and the safeguards in [ARCHITECTURE.md](../../ARCHITECTURE.md) section 8.1.

## Deliverables

| Item | Where |
|---|---|
| Limited standard-library JSON Schema validator with a keyword allowlist that fails closed | `src/kritva_mind/jsonschema_lite.py` |
| Semantic rules from [contract/SEMANTICS.md](../../contract/SEMANTICS.md) | `src/kritva_mind/semantics.py` |
| Contract loader, strict JSON loading (duplicate keys, NaN and Infinity rejected), command line | `src/kritva_mind/contract.py`, `__main__.py` |
| Unit tests | `tests/validator/` |
| `make test-unit` implemented; `unit-tests` workflow | `Makefile`, `.github/workflows/unit-tests.yml` |

## Proposed acceptance criteria (not accepted; this task has no accepted criteria version)

| ID | Criterion | Verified by |
|---|---|---|
| V-001 | Unsupported schema keywords, unknown `format` values and unresolvable `$ref`s fail closed (D-2). | `test_jsonschema_lite.py`, `test_contract_keywords.py` |
| V-002 | `date-time` is asserted as RFC 3339; `pattern` anchors do not accept a trailing newline. | `test_jsonschema_lite.py` |
| V-003 | Every example in `examples/manifest.json` gives its expected outcome, for the stated reason, and no example file is missing from the manifest. | `test_examples.py` |
| V-004 | Validation is deterministic: repeated runs, key order and hash seed do not change the sorted violation list (AC-004). | `test_determinism.py` |
| V-005 | The rules of SEMANTICS.md that schemas cannot express are checked: unique `proposal_id`, proposal ordering, version-constraint range and semantics, Sense error mapping, `usable` against freshness, context lifecycle, request/context binding, cancellation outcomes (AC-002, AC-003, AC-008, AC-011). | `test_semantics.py` |
| V-006 | No result field can command an actuator or authorize execution (AC-007). | `test_strict_json_and_cli.py` |
| V-007 | An optional differential test against `jsonschema` agrees on every example when the package is installed, and is reported SKIPPED otherwise. | `test_differential.py` |

## Rule ids

`S-PROPOSAL-ID-UNIQUE`, `S-VERSION-RANGE`, `S-ERROR-MAPPING`, `S-OBSERVATION-USABLE`, `S-SENSE-CONTRACT-VERSION`, `S-CONTEXT-INITIAL`, `S-CONTEXT-TRANSITION`, `S-CONTEXT-UNUSABLE`, `S-BINDING`, `S-CANCEL`. Schema violations carry the failing keyword as their code.

## Findings for the contract review (KOS-MIND-001)

These came from implementing the rules and are for the owner's review; the validator follows the documents as they stand.

1. The schemas use `contains` (the FAILED-needs-an-ERROR rule), which the D-2 keyword list in ARCHITECTURE.md section 8.1 does not name. The validator implements it and a test pins the allowlist as "documented list plus `contains`". The list in section 8.1 should be updated.
2. SEMANTICS.md section 2 says revision 1 is CREATED and lists CREATED only as the first state, so the validator rejects CREATED on a later revision. It does not say whether CREATED to ACTIVE is a new revision; the validator treats every legal transition as a new revision (previous plus 1), as the text on revision numbering says.
3. Not implemented because the documents leave them open: `expires_at` against a clock (a clock source is not defined), whole-result digests, context retrieval, and the wire format of `cancel`. `updated_at` ordering is not checked.
4. A `SNAPSHOTTED` revision must carry a `snapshot_ref` with a digest (section 2); the schema alone does not require it.

## Out of scope

Reasoning providers, memory backends, transport, Core integration, integration and regression tests (KOS-MIND-004), disconnected-operation and per-provider conformance tests (KOS-MIND-003), replay comparison (KOS-MIND-006). Passing the unit tests is not hardware or safety validation and does not show the contract is correct.

## Evidence still to record

Commit SHA, CI run ID of `unit-tests` on that commit, `make test-unit` output, and the reviews. The `unit-tests` workflow is not a required check: adding it to `required_github_checks` needs an owner-approved kritva-program pipeline update.
