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
| 4 | criteria review, approvals, evidence on the exact closing commit, then the annotated tag `v0.1.0` after the approved merge | not started |

Tag rule: no `v0.1.0` tag until the Mind and Skill interface is jointly reviewed and agreed. The tag does not wait for Motion if Mind does not consume it. A Mind tag is not V2-M1 completion: V2-M1 closes only through its program completion record.

## Out of scope

Validator implementation, reasoning providers, memory backends, planning, deployment, runtime integration with Skill.

## Open

Decision D-1 (encoding, proposed JSON Schema 2020-12), the joint review with kritva-skill (C-4), and a pin of an approved Core contract version if one is consumed (the Sense contract 0.1.0 is pinned in the criteria).
