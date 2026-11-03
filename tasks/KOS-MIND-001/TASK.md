# KOS-MIND-001: Mind request, context and result contract

Status: IN_PROGRESS. The owner approved starting the task in chat on 2026-11-02 ("Goahead with KOS-MIND-001 implementation"); no separate approval record exists in this repository. The task carries no weight and earns no credit (see [planning/TASKS.md](../../planning/TASKS.md)). Milestone: V2-M1-MIND-001 (proposed).

Acceptance: [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md) section 3, AC-001 to AC-011. None is accepted.

## Plan (PR sequence)

| PR | Content | State |
|---|---|---|
| 1 | [ARCHITECTURE.md](../../ARCHITECTURE.md), criteria, candidate tasks | merged (PR 9) |
| 2 | JSON Schemas and [contract/README.md](../../contract/README.md) | merged (PR 10) |
| 3 | [examples](../../examples/README.md); Sense compatibility notes and Skill review questions ([COMPATIBILITY.md](../../contract/COMPATIBILITY.md)) | this change; the Skill review cannot start until KOS-SKILL-001 does |
| 4 | criteria review, approvals, evidence, tag v0.1.0 after the approved merge | not started |

## Out of scope

Validator implementation, reasoning providers, memory backends, planning, deployment, runtime integration with Skill.

## Open

Decisions D-1 (encoding, proposed JSON Schema 2020-12), D-2 (validator), joint reviews, a pin of an approved Core contract version if one is consumed (the Sense contract 0.1.0 is pinned in the criteria).
