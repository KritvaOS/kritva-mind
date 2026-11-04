# KOS-MIND-001 closure record

Task: KOS-MIND-001. Status: AGREED BY THE OWNER IN CHAT (2026-11-04); not a completion record. This record carries the owner's outcomes for the two joint reviews and the criteria dispositions. The owner read it and agreed it as written, including the dispositions in section 4 and the limitations in section 5, in chat on 2026-11-04; there is no separate approval record. It is not a completion record, does not close V2-M1, earns no credit and creates no tag. The owner and the reviewer are the same person on an interim basis (program decision D-047), so nothing here is independent review.

Owner outcomes below were given in chat on 2026-11-04 by the owner (Dinesh) and the whole record was then agreed by the owner in chat the same day; there is no separate approval record. The record was drafted by an AI assistant from the owner's answers.

## 1. Basis

| Item | Read |
|---|---|
| Sense review record | `planning/reviews/KOS-MIND-001-SENSE-REVIEW.md` as on kritva-mind `main` on 2026-11-04: findings SE-1 to SE-12, every owner disposition PENDING, reviewed against Mind commit `1bb7899` |
| Skill review record | `planning/reviews/KOS-MIND-001-SKILL-REVIEW.md` as on `main` on 2026-11-04: findings SK-1 to SK-15, every owner disposition PENDING, reviewed against Mind commit `1bb7899e2836` and Skill commit `c17192001f6c` |
| Contract text compared | the local checkout of `contract/` and `ARCHITECTURE.md` as read on 2026-11-03 |
| Skill design note | kritva-skill `docs/design/MIND_SKILL_INTERFACE.md` (proposed, not approved) as on `main` on 2026-11-04 |

Re-check before closure: the review records name an older Mind revision than the closing commit. The positions below must be re-read against the exact closing commit, and the two review records must be refreshed against it, before the owner signs. This record does not do that.

## 2. Sense review (SE-1 to SE-12)

Outcome: **AGREED** (owner, chat, 2026-11-04). The table gives where each finding stands in the contract text; it is not a separate owner decision per finding.

| ID | Finding | Position in the contract text |
|---|---|---|
| SE-1 to SE-4, SE-11 | identity, clock, validity values, public contract only | confirmed by the review; no Mind change |
| SE-5 | `usable` rule | [SEMANTICS.md](../../contract/SEMANTICS.md) section 6: `usable` is true only if VALID and, when freshness is evaluated, fresh and on the same clock; the schema forces false for STALE, MISSING, INVALID |
| SE-6 | Sense 6.1 edge rules | section 6: Sense rules apply unchanged; an age equal to the limit is fresh; a future or cross-clock sample is not usable |
| SE-7 | `max_age_ns` minimum | lowered to 0 in `FreshnessPolicy`, as Sense sets no minimum |
| SE-8 | Sense `error_code` | optional `sense_error_code` on `ObservationRef`, forbidden when VALID, upper-case Sense code |
| SE-9 | error mapping | table in section 6 (STALE_DATA, MISSING_DATA, all other codes to MIND_INPUT_INVALID) |
| SE-10 | version enforcement | `source_contract` accepts any SemVer string; the pin is in [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md) section 2 and is not enforced by the schemas (a validator may check it) |
| SE-12 | assumptions stronger than Sense | none beyond SE-5 and SE-7, both addressed above |

Fact still true after the outcome: nothing was run against a Sense validator or a real Sense sample, and the Sense side has not reviewed the mapping.

## 3. Skill review (SK-1 to SK-15)

Outcome: **AGREED** (owner, chat, 2026-11-04). Per-finding positions:

| ID | Finding | Position |
|---|---|---|
| SK-1 to SK-9 | proposal handle, `skill_id`, version constraint, status handling, authority, priority, preconditions, cancellation, disposition vocabulary | AGREES in the review; SK-4 and SK-6 are stated in [contract/README.md](../../contract/README.md) and SEMANTICS.md section 4 |
| SK-10 | identifier characters | answered in the contract: identifiers use 1 to 128 characters from `A-Z a-z 0-9 . _ : -`, Motion's set (SEMANTICS.md section 7) |
| SK-11 | digest of the result | answered in the contract: no whole-result digest is defined; if two parties compare one they use RFC 8785 canonical JSON, recommended not required (section 7) |
| SK-12 | freshness at execution time | not a Mind change; depends on the transport and platform design, which is not made |
| SK-13 | state machines | Skill and Motion decision; no Mind change |
| SK-14 | Skill-side decisions | owner decisions in kritva-skill (version approval registry, authorization policy, precondition vocabulary, who may cancel a run, whether PARTIAL may ever execute) |
| SK-15 | status of the Skill note | the note is proposed, not approved; this record does not call the interface agreed beyond the review outcome |

Decision D-6 (Mind-to-Skill interaction) is closed by this outcome, recorded here and on the Skill review record, which the same pull request updates from PENDING to AGREED. Facts still true: nothing was executed, the Skill side has no reviewer but the owner, and Motion's contract was not reviewed.

## 4. Criteria dispositions (AC-001 to AC-011)

Chosen approach (owner, chat, 2026-11-04), agreed with this table: contract-level review now; every test item stays NOT_IMPLEMENTED and deferred. A disposition here is not "met": none of the criteria is accepted by this record.

| AC | Disposition (agreed by the owner in chat) | Evidence at closure | Deferred |
|---|---|---|---|
| AC-001 | REVIEWED, contract level | schemas 0.1.0-draft, examples checked by hand once | schema tests: KOS-MIND-002 |
| AC-002 | REVIEWED, contract level | `Uncertainty`, `Error`, FAILED-needs-ERROR rule | error-path tests: KOS-MIND-002 |
| AC-003 | REVIEWED, contract level | SEMANTICS.md section 1 | cancellation tests: KOS-MIND-002; wire format not defined |
| AC-004 | REVIEWED, contract level | contract states validation is deterministic | determinism tests: KOS-MIND-002 |
| AC-005 | REVIEWED | Sense contract 0.1.0 pinned (tag `v0.2.0`); observations referenced, never embedded; no Core contract consumed (C-5) | version enforcement: KOS-MIND-002/004 |
| AC-006 | REVIEWED, subject to the owner's architecture review record | [ARCHITECTURE.md](../../ARCHITECTURE.md), open decisions D-1, D-2 and D-8 decided in chat; D-3 and D-4 deferred by design | independent review: none in place (D-047) |
| AC-007 | REVIEWED | no authorizing or executing field; unknown fields rejected; Skill review outcome AGREED | cross-repository tests: KOS-MIND-007 |
| AC-008 | REVIEWED, contract level | SEMANTICS.md section 2 | lifecycle tests: KOS-MIND-002 and KOS-MIND-003 |
| AC-009 | REVIEWED, contract level only | contract has no cloud dependency; unavailable provider is explicit | disconnected-operation tests: KOS-MIND-003 (NOT_IMPLEMENTED) |
| AC-010 | REVIEWED, contract level only | `provider_id`, optional `placement` | conformance tests: KOS-MIND-003 (NOT_IMPLEMENTED) |
| AC-011 | REVIEWED, contract level | execution record, digests, replay class | schema tests: KOS-MIND-002; replay comparison: KOS-MIND-006 |

Gates at closure: `make test-unit`, `make test-integration` and `make test-regression` are NOT_IMPLEMENTED and are never counted as passes.

## 5. Known limitations carried into `v0.1.0`

1. Ingress authentication is not specified or verified (owner decision C-5 and chat, 2026-11-03). Mind must not be exposed to untrusted callers until the platform boundary is defined, implemented and reviewed. Wording: [tasks/KOS-MIND-001/TASK.md](../../tasks/KOS-MIND-001/TASK.md).
2. No executable validator is included in the release; semantic rules JSON Schema cannot express are unchecked by any implementation (validation-limitation text in the same file).
3. The pinned Sense version is not enforced by the schemas (SE-10).
4. Nothing was reviewed independently: the owner holds the code-owner, architecture and both neighbouring-repository roles (D-047).
5. The Skill note is a proposal, and Skill-side decisions SK-12 to SK-14 are open outside this repository.

## 6. What this record cannot do

| Step | Needs |
|---|---|
| Update the two review records with the agreed outcomes (section 7) | done in the same pull request, by the script that opens it, on a checkout that has them (`planning/reviews/` is on `main`; the checkout read here did not have it) |
| Refresh both review records against the closing commit | the owner or a reviewer, after the last contract change merges |
| Code-owner and architecture-reviewer review records | the owner |
| Exact closing commit SHA, merge pull request, CI run IDs of `secret-scan`, `commit-message-check` and `pr-acceptance-gate` | a merge and CI; none exists for this change yet |
| `make check`, `make docs-check`, `make check-readme` results | run on the closing commit (they passed on a local working copy on 2026-11-04, which is not evidence) |
| Completion record | the owner; the program standard's template was not read for this record |
| Annotated tag `v0.1.0` | after the approved merge only; the tag does not close V2-M1 |

## 7. Text for the review records

Sense review outcome: `AGREED` by the owner in chat on 2026-11-04; no separate approval record; SE-1 to SE-12 positions as in the KOS-MIND-001 closure record.

Skill review outcome: `AGREED` by the owner in chat on 2026-11-04; no separate approval record; SK-1 to SK-15 positions as in the KOS-MIND-001 closure record; decision D-6 closes on this record.
