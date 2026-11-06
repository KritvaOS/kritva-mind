# Review record: Mind and Skill interface (KOS-MIND-001)

Status: OUTCOME AGREED BY THE OWNER IN CHAT (2026-11-04), not an independent review. The cross-read findings below are an AI-assisted reading; each disposition records the owner's overall outcome, given in chat with no separate approval record. Nothing here is an acceptance of any criterion, and it earns no credit or weight. This record is evidence for task KOS-MIND-001 ([TASK.md](../../tasks/KOS-MIND-001/TASK.md)); the Skill-side proposal it reviews lives in the kritva-skill repository.

## 1. Scope and revisions

| Item | Value |
|---|---|
| Reviewed | The Mind proposal and result contract and Skill's proposed consumption, disposition and run interface. Decision D-6 (joint review of the Mind to Skill interaction) closes only when the owner records the outcome below. |
| Mind revision | kritva-mind `main`, commit `1bb7899e2836560e734c0ca870ae4a2bb0e17f2f` (pull request 21 merged), read 2026-11-03: `contract/*.schema.json`, `contract/SEMANTICS.md`, `contract/COMPATIBILITY.md`, `ARCHITECTURE.md`, `ACCEPTANCE_CRITERIA.md` |
| Skill revision | kritva-skill `main`, commit `c17192001f6c672819589857e8644ad21573d8d8` (pull request 11 merged): `docs/design/MIND_SKILL_INTERFACE.md`, a proposed note that is not an approved contract. Skill has no manifest or execution schema yet. |
| Motion | Not part of this review. Facts about Motion in the Skill note come from kritva-motion `main` at `d28611442a1d` (an untagged draft contract); nothing there was relied on beyond what the note states. |

If the Mind or Skill revision changes before the criteria review (PR-4), the revisions above must be updated and the affected findings re-checked.

Refresh, 2026-11-06 (AI-assisted; the owner is the only reviewer, D-047): the Mind side was re-read against kritva-mind `main` commit `b59f767268b77075a0ea693f9346d34d9fef83c5` (pull request 25 merged; `unit-tests` run 42215995601 succeeded on it). Nothing under `contract/` changed in pull request 25, so the contract text equals the text at `d821319caea42a22633d7219dc3c237be712fb3a`; the Mind-side positions for SK-1 to SK-11 in the closure record were checked against it and still hold, including the identifier set and the whole-result digest statement in SEMANTICS.md section 7. The validator tests the proposal rules (unique `proposal_id`, proposal ordering, version-constraint semantics) in `tests/validator/test_semantics.py`, classes `ProposalRules` and `VersionSemantics`. The Skill side was not refreshed: the Skill revision above is the last one this repository read (2026-11-03) and kritva-skill was not re-fetched for this refresh. As read then, Skill's note still names the older Mind revision `7569b80` and defines `mind_result_digest` as a digest 'in the Mind format', which SEMANTICS.md section 7 says Mind does not define; that is a Skill-side follow-up under KOS-SKILL-001. SK-12 to SK-14 stay open outside this repository.

## 2. Reviewer, method and independence

- **Reviewer:** Dinesh, as repository owner and interim architecture reviewer under program decision D-047. This record is drafted for that review; the owner's reading and dispositions are still to be recorded.
- **Method:** AI-assisted cross-read of the identified public repository revisions, followed by owner examination and disposition of the findings. AI assistance is supporting analysis only; it is not an approver or independent reviewer.
- **Independence:** this is not an independent review and none is claimed. The same person holds the Mind and Skill owner and reviewer roles.
- **Nothing was executed.** No validator, test or runtime exists on either side.

## 3. Findings

Cross-read result: AGREES (the two documents say the same thing), MISMATCH, or OPEN (neither side decides it yet).

| ID | Topic | Cross-read result | Evidence | Proposed handling | Owner disposition |
|---|---|---|---|---|---|
| SK-1 | Proposal handle | AGREES | Mind requires `proposal_id`, unique per result; Skill uses `proposal_id` to link its report back (note, report fields table) | none | AGREED (owner, chat, 2026-11-04) |
| SK-2 | `skill_id` shape | AGREES | Mind `SkillId` and the Skill note use the identical pattern `^[a-z][a-z0-9_]{0,31}(\.[a-z0-9_]{1,32}){0,3}$` | none | AGREED (owner, chat, 2026-11-04) |
| SK-3 | Version constraint | AGREES | Mind `VersionConstraint` and `SEMANTICS.md` section 3 (exact, caret, range; no pre-release, wildcards or tags; caret same MAJOR, same MINOR when MAJOR is 0) match the Skill note, which resolves only among approved versions and never lets a constraint pin or approve | none | AGREED (owner, chat, 2026-11-04) |
| SK-4 | Result status handling | AGREES | Mind: PARTIAL proposals advisory, FAILED and CANCELLED proposals not to be executed. Skill: FAILED and CANCELLED declined, PARTIAL declined by default unless its policy says otherwise | keep the Skill default explicit | AGREED (owner, chat, 2026-11-04) |
| SK-5 | Authority | AGREES | Mind has no authorization or execute field and rejects unknown fields; Skill independently resolves, validates and authorizes and treats uncertainty, rationale and priority as advisory | none | AGREED (owner, chat, 2026-11-04) |
| SK-6 | Priority | AGREES | Mind states the rule in the proposal schema and `SEMANTICS.md` section 4 (lower first, ties and absent values by ascending `proposal_id`, absent after present, array order not authoritative); the Skill note records the same rule and treats `priority` as ordering only | validator task must implement the order | AGREED (owner, chat, 2026-11-04) |
| SK-7 | Preconditions | AGREES | Mind `expression` is never evaluated by Mind or Skill; `precondition_id` names a Skill-defined precondition | none | AGREED (owner, chat, 2026-11-04) |
| SK-8 | Cancellation | AGREES | Mind `cancel(request_id)` leaves a CANCELLED result whose proposals are not executed; Skill declines them. Cancelling a Skill run is a separate matter not yet decided | Skill-side decision pending | AGREED (owner, chat, 2026-11-04) |
| SK-9 | Disposition vocabulary | AGREES | Skill uses RECEIVED, then CLEARED or DECLINED, so it does not reuse Motion's ACCEPTED and REJECTED | none | AGREED (owner, chat, 2026-11-04) |
| SK-10 | Identifier characters | OPEN | Mind `Id` allows any string of 1 to 128 characters. Motion limits identifiers to 1 to 128 characters from `A-Z a-z 0-9 . _ : -`. Skill proposes deriving Motion's `client_request_id` from `result_id` and `proposal_id`, and marks the encoding open | Mind may restrict the `Id` charset, or Skill must encode; decide before either is released | AGREED (owner, chat, 2026-11-04) |
| SK-11 | Digest of the result | OPEN | The Skill report carries `mind_result_digest` ("the result as received"). Mind defines digests inside the execution record but no canonical form for a whole result, so two parties could compute different digests | define a canonical form in the contract, or state that Skill's digest is Skill-local | AGREED (owner, chat, 2026-11-04) |
| SK-12 | Freshness at execution time | OPEN | Skill's table says context and observations are re-evaluated at execution time. A Mind result carries `context_ref` and a snapshot reference with digest, but no mechanism for Skill to retrieve that context is defined (transport is undecided) | record as a dependency of the transport and platform design | AGREED (owner, chat, 2026-11-04) |
| SK-13 | State machines | OPEN | Skill's run lifecycle and Motion's public command states are separate and no mapping exists. Mind has no Motion interface | Skill and Motion decision; no Mind change | AGREED (owner, chat, 2026-11-04) |
| SK-14 | Skill-side decisions | OPEN | Approval state of skill versions, authorization policy, precondition check vocabulary, who may cancel a run, whether PARTIAL may ever execute, and decomposition of a skill into joint-level Motion commands are listed as undecided in the Skill note | owner decisions in kritva-skill | AGREED (owner, chat, 2026-11-04) |
| SK-15 | Status of the Skill note | NOTED | The note is a proposal, reviewed only by the owner, with no schema | do not describe the interface as agreed beyond this record | AGREED (owner, chat, 2026-11-04) |

## 4. Outcome

Outcome: **AGREED** (owner, in chat, 2026-11-04; no separate approval record). The position of each finding is in [KOS-MIND-001-CLOSURE.md](KOS-MIND-001-CLOSURE.md). The revisions in section 1 are older than the closing commit and must be re-checked before the completion record. Decision D-6 closes on this record.

For the owner's consideration: findings SK-10 to SK-14 are open and none contradicts the other side; SK-1 to SK-9 agree. If the owner records AGREED WITH LIMITATIONS, SK-10 to SK-14 should be named as the limitations, and D-6 closes only on that record.

## 5. Not verified

- No executable validator exists; the Mind examples were checked once, by hand, with a third-party validator, and `format` was not asserted.
- Skill's note was compared with Mind's schemas by reading; no code consumed a Mind result.
- Motion's contract is an untagged draft and was not reviewed here.
- The Skill side has not been reviewed by anyone other than the owner.
