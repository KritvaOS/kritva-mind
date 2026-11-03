# Compatibility and joint-review notes (PROPOSED)

Task: KOS-MIND-001. This records what was found about the neighbouring contracts and what is still open. It is a review input, not a review result: no reviewer other than the owner has seen it, and the owner holds the architecture review role on an interim basis (program decision D-047), so nothing here is independent review.

Checked on 2026-11-02 against the public repositories on GitHub; nothing was run.

## Sense (kritva-sense)

**State found.** Sense publishes `contract/SENSE_CONTRACT.md` (contract 0.1.0) with `contract/sense-sample.schema.json`. Its status line says the owner approved contract 0.1.0 under the interim D-047 review, and the repository has tags `v0.1.0` and `v0.2.0`. It states that it remains a 0.x contract that can change with a changelog entry and a decision. This contradicts the wording in this repository's README ("Sense has no contract yet"), which is out of date.

**Pin.** Made on the owner's instruction in chat, 2026-11-02: Sense contract 0.1.0 at tag `v0.2.0` (commit `543f5743d6ffd8fa1ed1ee5fdbf8295ae6a69a77`), recorded in [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) section 2. The draft schemas do not enforce the version.

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

**State found (2026-11-03).** Skill's pull request 9 is merged: KOS-SKILL-001 is IN_PROGRESS on the owner's chat instruction and `docs/design/MIND_SKILL_INTERFACE.md` is on its `main`. That note is a proposal, not an approved contract, and there is still no Skill manifest or execution schema to check a Mind result against. It answers the questions below as proposals and asked Mind for seven changes. Status of those changes in the Mind draft:

| Skill request | Mind draft now |
|---|---|
| `proposal_id` on a proposal | added, required, unique within a result (validator rule) |
| `skill_id` pattern and closed `version_constraint` grammar | added as `SkillId` and `VersionConstraint`; examples for each rule |
| optional `precondition_id`; `expression` not evaluated | added; stated in the schema and contract README |
| direction and tie-breaking of `priority` | lower first; ties and absent values by ascending `proposal_id`; absent after present |
| Mind validating against Skill's schema vs no dependency on Skill | only with a schema supplied as runtime data and within the validator subset; ARCHITECTURE.md section 5 corrected |
| handling of PARTIAL results | stated: advisory; consumers must not execute them unless their policy says so |
| compatibility notes | this section |

Open on the Skill side, not decided here: where skill-version approval is recorded, the authorization policy, the precondition check vocabulary, who may cancel a run, and the mapping between Skill's run lifecycle and Motion's public command states. The joint review is not complete: nobody but the owner has reviewed either side.

**Questions to put to kritva-skill (from [ARCHITECTURE.md](../ARCHITECTURE.md) section 12)**

1. What is the canonical skill identity and version-reference format, and can Mind propose a version constraint without pinning an unapproved version?
2. What does Skill need to resolve a proposal against its manifest?
3. What parameter schema and precondition format does Skill expect (the Mind draft uses `parameters` as an object and `preconditions` as descriptions with an optional expression)?
4. Which validations are Mind's, and which does Skill repeat before execution?
5. How does Skill handle rejected proposals, unmet preconditions, cancellation, partial execution and failure?
6. What does Skill return to keep traceability from proposal to execution?
7. Does Skill confirm that Mind proposes and Skill independently validates and authorizes?

## Core (kritva-core)

No Core contract version is pinned or consumed by the draft schemas, and this repository does not import Core. The program pipeline lists Core as a Mind dependency in program ordering; that does not by itself mean Mind consumes a Core contract. Core's `docs/security/TRUST_BOUNDARIES.md` states that Core does not authenticate entities, so there is no Core authentication contract to consume (read 2026-11-03). Confirmed by the owner in chat on 2026-11-03 (C-5): no Core contract pin is needed for this interface. The program's pipeline still lists Core as a dependency in program ordering; amending that entry is the owner's decision in kritva-program and is not done here.

## Drafted after the first review

The schemas now draft answers to the open points in the Sense table above: an `ObservationRef` carrying sensor identity, sequence, clock, timestamp in nanoseconds, validity, a `usable` flag and the Sense contract version; a `FreshnessPolicy` in request constraints; and a closed list of Mind error codes with Sense codes kept in `detail.sense_error_code`. These are proposals. Nobody on the Sense side has reviewed them, and the Sense contract was read, not run.

## Authentication boundary (decided by the owner, C-5)

The Mind request JSON carries no caller identity and does not authenticate its caller. Authentication belongs to the transport, gateway or platform security boundary, which may pass the authenticated principal as trusted envelope metadata for audit, never as a claim in the request payload. Mind does not trust caller-supplied identity fields. Skill independently authorizes a proposal and its target before execution. Motion's draft refers to a provisional identity assertion that Core has not defined; Mind does not invent it. Risk of the alternative: an identity field in Mind's schema would accept spoofable data and couple Mind to a format nobody has defined. Risk of this choice: Mind ingress must be authenticated by the platform, which is outside this repository and not yet specified.

## Decisions this review needs

| ID | Decision | Owner |
|---|---|---|
| C-1 | Record Sense contract 0.1.0 as a normative dependency, and the tag or SHA that identifies it | DECIDED by the owner in chat, 2026-11-02: contract 0.1.0 at tag `v0.2.0` (commit `543f574`); recorded in [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) section 2 |
| C-2 | How observation references carry clock, value and validity | DRAFTED in the schemas (`observations[]`); needs a check by the Sense owner |
| C-3 | Where `max_age_ns` is declared and what error codes Mind defines for stale, missing and invalid input | DRAFTED in the schemas (`constraints.freshness`, error code enum); needs review |
| C-4 | Start KOS-SKILL-001 so the joint review can happen | DECIDED by the owner in chat, 2026-11-03: started on a local branch in kritva-skill (not yet pushed or reviewed here) |
| C-5 | Confirm that Mind consumes no Core contract and that authentication stays outside the Mind request | DECIDED by the owner in chat, 2026-11-03; no separate approval record. Ingress authentication is still unspecified and sits with the platform security boundary |
