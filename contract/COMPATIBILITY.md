# Compatibility and joint-review notes (PROPOSED)

Task: KOS-MIND-001. This records what was found about the neighbouring contracts and what is still open. It is a review input, not a review result: no reviewer other than the owner has seen it, and the owner holds the architecture review role on an interim basis (program decision D-047), so nothing here is independent review.

Checked on 2026-11-02 against the public repositories on GitHub; nothing was run.

## Sense (kritva-sense)

**State found.** Sense publishes `contract/SENSE_CONTRACT.md` (contract 0.1.0) with `contract/sense-sample.schema.json`. Its status line says the owner approved contract 0.1.0 under the interim D-047 review, and the repository has tags `v0.1.0` and `v0.2.0`. It states that it remains a 0.x contract that can change with a changelog entry and a decision. This contradicts the wording in this repository's README ("Sense has no contract yet"), which is out of date.

**Pin.** Not made here. [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) section 2 says a version is recorded when the contract it names is approved; the owner decides whether to record Sense contract 0.1.0 (and which tag or commit SHA identifies it) in a separate change.

**Compatibility with the draft Mind contract**

| Topic | Sense contract 0.1.0 | Mind draft | Finding |
|---|---|---|---|
| Time | integer nanoseconds with a `monotonic` or `utc` clock; comparing across clocks is undefined | RFC 3339 date-time strings | Different forms. A Mind context must not compare a Sense monotonic value with a Mind timestamp. A reference to an observation should keep its clock and value; the draft `Reference` carries only `ref`, `digest` and `source_contract`. Open: carry `clock` and `value` of the observation, or keep them behind the opaque `ref`. |
| Identity | `sensor_id` plus `sequence` per sensor | `source_refs[].ref` is an opaque string | A reference such as `sense://<sensor_id>/<sequence>` could be defined. Not defined yet. |
| Freshness | consumer declares `max_age_ns`; staleness is evaluated by the consumer | no freshness field | Mind, as a consumer, must decide `max_age_ns` per stream. Open: where it is declared (request `constraints`?) and how a stale observation is reported (a `MIND_INPUT_STALE` warning appears in an example, not in a defined code list). |
| Validity | `VALID`, `STALE`, `MISSING`, `INVALID`; measurements of a `STALE` or `INVALID` sample must not be used as readings | not represented | Mind must not copy such measurements into a proposal's basis. A rule and error code are needed. |
| Errors | fixed code list (for example `STALE_DATA`, `SEQUENCE_REGRESSION`) | free-form `code` strings | Open: whether Sense codes are passed through unchanged in `detail`. |
| Units and frames | SI units, frames `world`, `base`, `sensor`, no transforms | measurement content is opaque `content` | Mind does not re-define units or frames; any measurement inside `content` must follow the Sense contract. |
| Extensibility | unknown fields rejected | unknown fields rejected in all Mind schemas except `constraints` | `constraints` allows extra fields; decide whether that is intended. |

## Skill (kritva-skill)

**State found.** The Skill repository has a proposed task KOS-SKILL-001 (Skill manifest and execution contract) with status NOT_STARTED, awaiting owner approval, no contract folder and no tags. Its acceptance criteria list its normative dependency on versioned Mind and Motion contracts. So there is no Skill manifest or schema to check the Mind result against, and the joint review cannot be completed yet. The `ProposedSkill` fields in the Mind draft are unverified against any Skill definition.

**Questions to put to kritva-skill (from [ARCHITECTURE.md](../ARCHITECTURE.md) section 12)**

1. What is the canonical skill identity and version-reference format, and can Mind propose a version constraint without pinning an unapproved version?
2. What does Skill need to resolve a proposal against its manifest?
3. What parameter schema and precondition format does Skill expect (the Mind draft uses `parameters` as an object and `preconditions` as descriptions with an optional expression)?
4. Which validations are Mind's, and which does Skill repeat before execution?
5. How does Skill handle rejected proposals, unmet preconditions, cancellation, partial execution and failure?
6. What does Skill return to keep traceability from proposal to execution?
7. Does Skill confirm that Mind proposes and Skill independently validates and authorizes?

## Core (kritva-core)

No Core contract version is pinned or consumed by the draft schemas. Not reviewed beyond confirming that this repository does not import it.

## Decisions this review needs

| ID | Decision | Owner |
|---|---|---|
| C-1 | Record Sense contract 0.1.0 as a normative dependency, and the tag or SHA that identifies it | owner |
| C-2 | How observation references carry clock, value and validity | KOS-MIND-001 design, checked with Sense |
| C-3 | Where `max_age_ns` is declared and what error codes Mind defines for stale, missing and invalid input | KOS-MIND-001 design |
| C-4 | Start KOS-SKILL-001 so the joint review can happen | owner |
