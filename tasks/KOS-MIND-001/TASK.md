# KOS-MIND-001: Mind request, context and result contract

Status: IN_PROGRESS. The owner approved starting the task in chat on 2026-11-02 ("Goahead with KOS-MIND-001 implementation"); no separate approval record exists in this repository. The task carries no weight and earns no credit (see [planning/TASKS.md](../../planning/TASKS.md)). Milestone: V2-M1-MIND-001 (proposed).

Acceptance: [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md) section 3, AC-001 to AC-011. None is accepted.

## Plan (PR sequence)

| PR | Content | State |
|---|---|---|
| 1 | [ARCHITECTURE.md](../../ARCHITECTURE.md), criteria, candidate tasks | merged (PR 9) |
| 2 | JSON Schemas and [contract/README.md](../../contract/README.md) | merged (PR 10) |
| 3 | [examples](../../examples/README.md); Sense compatibility notes and Skill review questions ([COMPATIBILITY.md](../../contract/COMPATIBILITY.md)) | merged (PR 11); later schema and doc fixes merged (PRs 12 to 15) |
| 3a | align the plan with the program plan, fix stale notes, record the authentication boundary (proposed) | this change |
| 3b | one schema PR for the Skill-requested changes (`proposal_id`, `skill_id` pattern and closed `version_constraint` grammar, `precondition_id`, `priority` direction, runtime-supplied schema rule, PARTIAL handling), with examples and a matching COMPATIBILITY.md; the Skill design note is merged in kritva-skill (PR 9) | this change (stacked on 3a) |
| 3c | contract and criteria sync after the external review: digests and context snapshot required for replay, optional `placement`, FAILED needs an ERROR, new `contract/SEMANTICS.md` (cancellation, context lifecycle, version-constraint semantics, ordering), AC-003, AC-008 to AC-011 reworded, stale documents refreshed | this change |
| 3d | contract changes answering the review findings (`sense_error_code`, `max_age_ns` minimum, identifier character set, SEMANTICS sections 6 and 7); the two review records must be refreshed against the merged result | this change |
| 4 | criteria review, approvals, evidence on the exact closing commit, then the annotated tag `v0.1.0` after the approved merge | not started |

Tag rule: no `v0.1.0` tag until the Mind and Skill interface is jointly reviewed and agreed. The tag does not wait for Motion if Mind does not consume it. A Mind tag is not V2-M1 completion: V2-M1 closes only through its program completion record.

## PR-4 checklist (proposed)

1. Skill side updated against the current Mind contract in kritva-skill (its note still lists fields Mind has since added, and uses two names for one rejection code).
2. Joint review recorded with kritva-skill (the proposal interface) and kritva-sense (observation and freshness mapping); decision D-6 closed only after it. Drafts, with every owner disposition PENDING: [Skill record](../../planning/reviews/KOS-MIND-001-SKILL-REVIEW.md) and [Sense record](../../planning/reviews/KOS-MIND-001-SENSE-REVIEW.md); both must be refreshed against the final merged revisions.
3. D-1 (JSON Schema 2020-12) is decided by the owner in chat, 2026-11-03, with no separate approval record; the owner may record it more formally at closure.
4. Review records from the code owner and the architecture reviewer (both the owner on an interim basis, D-047, not independent).
5. Criteria review: each of AC-001 to AC-011 given a disposition with evidence. None is marked met by a document review alone; criteria that need KOS-MIND-002 or later tasks stay NOT_IMPLEMENTED.
6. The ingress-authentication gap (no platform boundary is specified) is recorded as a known limitation of `v0.1.0`, not a blocker: decided by the owner in chat, 2026-11-03, with no separate approval record. It permits a contract release, not unrestricted deployment. Wording below.
7. Exact closing commit SHA, the merge pull request and the CI run IDs of `secret-scan`, `commit-message-check` and `pr-acceptance-gate` on that commit.
8. `make check`, `make docs-check` and `make check-readme` results recorded; `make test-unit`, `make test-integration` and `make test-regression` reported as NOT_IMPLEMENTED, never as passes.
9. Completion record drafted and approved by the owner; the annotated tag created only after the approved merge. A tag does not close V2-M1.

## Known limitation and release-note text (draft)

Known limitation — ingress authentication: Mind v0.1.0 does not authenticate request callers and does not carry caller identity or authentication assertions in its request schema. Authentication and authorization are the responsibility of the platform or transport boundary, consistent with owner decision C-5. That boundary, including trusted-principal propagation and enforcement, is not yet specified or verified by KOS-MIND-001. Deployments MUST NOT expose Mind ingress to untrusted callers until the platform boundary is defined, implemented and reviewed. Skill's independent authorization of execution does not replace authentication and authorization at Mind ingress.

Validation limitation (for the release notes): kritva-mind v0.1.0 is a contract release. It defines JSON Schema 2020-12 request, context and result schemas and the associated semantic rules. No executable Mind contract validator is included in this release. Semantic rules that JSON Schema cannot express, including cancellation, context lifecycle transitions, version-constraint semantics, proposal ordering and uniqueness, have not been checked by an implementation. Validator implementation and automated schema and semantic tests are deferred to KOS-MIND-002. Integration, provider conformance, disconnected-operation and replay-comparison testing are deferred to later tasks. This tag does not claim runtime, provider, Skill execution, hardware or safety validation, independent review or V2-M1 completion.

## Out of scope

Validator implementation, reasoning providers, memory backends, planning, deployment, runtime integration with Skill.

## Open

The joint review with kritva-skill (C-4), and a pin of an approved Core contract version if one is consumed (the Sense contract 0.1.0 is pinned in the criteria).
