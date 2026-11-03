# Architecture: kritva-mind

Status: PROPOSED. This document is a design proposal for task KOS-MIND-001. It is not approved, it is not an interface that other repositories may rely on, and it creates no baseline, weight or credit. The architecture reviewer role is held by the owner on an interim basis (program decision D-047), so a review of this document is not independent review.

Origin: an architecture discussion held outside this repository (a ChatGPT conversation, 2026-11-02) that the owner agreed with in chat. Statements about other repositories (kritva-core, kritva-sense, kritva-skill, kritva-motion) are assumptions to be checked against those repositories; nothing here has been verified against them.

## 1. Purpose

Kritva Mind is proposed as the cognitive layer of Kritva OS V2: it interprets a task request in its context and returns a result that proposes what should happen. It does not execute that result.

Mind owns the request, context and result contract (inputs, context identity, output schema, uncertainty and error reporting, cancellation and deterministic validation; see [AGENTS.md](AGENTS.md) section 1). The subsystems in section 3 are the logical design behind that contract. Which of them become code in this repository, and when, is decided task by task.

## 2. Principles

1. **Mind proposes; Skill authorizes and orchestrates; Motion controls.** A Mind result is a proposal. Mind never commands actuators.
2. **Contract-first.** Interfaces are versioned schemas, independent of program phases. A breaking change needs a new MAJOR version, a changelog entry and an approved decision.
3. **Three separate layers.** Reasoning produces a proposal. Validation checks it against the contract and constraints. Execution is decided by Skill. No layer's output stands in for another's.
4. **Deterministic validation.** Whatever a model produces must pass explicit validation before it is accepted as a result. The same input and context give the same validation outcome.
5. **No silent failure.** Uncertainty, errors, cancellation and partial results have defined fields.
6. **Model-independent and hardware-independent.** Reasoning sits behind an adapter interface. No model, framework or SoC is chosen here.
7. **Consume Sense only through its versioned contract**, never its internals.
8. **Observable.** Context identity, provenance, decisions and errors are preserved in the result.

Limits of what validation shows: schema validity is not safety, and a model's confidence value is not evidence of correctness. Nothing in this design is hardware or safety validation; such claims stay gated on program milestone V2-M6 (HOLD).

## 3. Components in scope

Scope is limited to the contract (see AGENTS.md section 1). These are logical components, not approved modules or folders.

| Component | Responsibility | In KOS-MIND-001 |
|---|---|---|
| Mind Core | Request lifecycle and coordination, cancellation | specified |
| Mind Context | Context identity and lifecycle (not the persistence backend) | specified |
| Mind Validation | Deterministic schema and semantic validation, uncertainty and error reporting | specified |
| Reasoning Adapter Interface | Abstract request and response interface to reasoning providers, result metadata | specified |

Not owned by this repository at this stage: reasoning engine implementations (model adapters, local serving, cloud integration), knowledge and memory backends, task planning and decomposition, and runtime or deployment orchestration. Where they live is decided when their requirements are concrete; no new repository is proposed now. The earlier seven-subsystem idea (adding Planning, Knowledge and Runtime) is deferred.

## 4. Data flow

```text
Request (task, goals, constraints)
   + Context (identity, state, history; Sense observations via the versioned Sense contract)
        |
        v
   Mind Core --> Reasoning / Planning / Knowledge --> proposal
        |
        v
   Mind Validation (schema, constraints, uncertainty, errors)
        |
        v
   Result (proposal, uncertainty, errors, provenance, context identity)
        |
        v
   kritva-skill: authorizes and orchestrates   -->   kritva-motion: real-time control
```

Cancellation can arrive at any point and yields a result that states what was completed, what is partial and what was discarded.

## 5. Contract elements (to be specified by KOS-MIND-001)

| Element | Must state |
|---|---|
| Request | request identity, schema version, task and constraints, time and units, optional deadline |
| Context | immutable context identity, revision number, timestamps, ownership, lifecycle (created, active, updated or snapshotted, closed, expired; cancellation is an explicit event, not deletion), source and version of each Sense input |
| Result | result and request identity, context identity, status (completed, partial, failed, cancelled), proposed skills, uncertainty, completeness, provenance, errors, contract version |
| Proposed skill | proposal identity (unique in the result), skill reference (lowercase dotted name), constraint (closed grammar: exact, caret or range; never a pin), compatible version or constraint, proposed parameters, known preconditions, rationale, proposal-level uncertainty, priority |
| Uncertainty | an optional score with a defined scale, source and calibration status, plus qualitative uncertainty and assumptions; never a single number standing in for uncertainty |
| Cancellation | who may cancel, when, what a partial result contains and which information is missing |
| Execution record (provenance) | input and context snapshot references with digests, provider, model and version, provider configuration and prompt template digests, inference parameters, seed if supported, output snapshot and digest, timestamp, tool versions, replay class |
| Versioning | MAJOR.MINOR.PATCH, compatibility rules, deprecation |

Execution authority is not granted by Mind: the result has no `authorized` or `execute` field that Skill must trust. Skill resolves the skill reference, validates its manifest, version and preconditions, and decides. Mind depends on no Skill code or version. It may validate parameters structurally against a skill's input schema only when that schema is handed to it as runtime data and uses the validator subset in section 8.1; otherwise Mind validates nothing against Skill. Skill always validates against its own manifest before execution, and treats uncertainty, rationale and priority as advisory. Proposals of a PARTIAL result are advisory: a consumer must not execute them unless its own policy says so, and Skill's proposed default is to reject them (see [contract/COMPATIBILITY.md](contract/COMPATIBILITY.md)).

Replay: validation is deterministic for identical inputs and validator version; inference may not be. The execution record lets a replay reconstruct the recorded conditions. The replay class is EXACT_REPLAY_SUPPORTED, CONDITION_REPLAY_ONLY or REPLAY_UNAVAILABLE. Exact equality is required only where the provider supports deterministic replay; otherwise a replay is labelled a comparison, not an exact reproduction. The original result stays immutable evidence.

Field names and encodings are proposals until KOS-MIND-001 is approved. The encoding (JSON Schema, a pinned draft such as 2020-12) is decision D-1 in section 8.

## 6. Interfaces with other repositories

| Repository | Direction | Intended relationship | Status |
|---|---|---|---|
| kritva-core | upstream | platform contract use | no approved version pinned |
| kritva-sense | upstream | observations enter context through the versioned Sense contract | Sense has no contract yet |
| kritva-skill | downstream | consumes the Mind result; owns execution authority | no consumer exists; the contract must be reviewed with Skill |
| kritva-motion | none direct | Mind has no interface to Motion | by design |

The Mind and Skill contracts depend on each other, so they are designed together rather than finalized separately.

## 7. Deployment placement (proposed, not decided)

The intended direction is hybrid: Edge, Nexus and Cloud. Not every subsystem runs in all three places. Placement follows latency, availability, compute, privacy and connectivity, and essential local cognitive functions should not depend on continuous cloud connectivity. Placement is decided in a later deployment document, after the contract exists; this architecture does not choose a runtime, service shape or container platform.

## 8. Open decisions

| ID | Decision | Recommendation | Needs |
|---|---|---|---|
| D-1 | Contract encoding | JSON Schema with a pinned draft (2020-12); transport decided separately | owner decision |
| D-2 | Validator implementation | DECIDED (owner instruction "Decide D2" in chat, 2026-11-03; no separate approval record): a limited, dependency-free validator in the Python 3 standard library, for KOS-MIND-002. It supports only the keywords the contract schemas use and refuses any other keyword, so it cannot silently ignore one. Reasons: the repository and its CI are standard-library only, kritva-sense does the same, the schemas use a small keyword set, and error ordering stays under our control (AC-004). Safeguards in section 8.1 | none |
| D-3 | Context persistence | identity and lifecycle in the contract; backend out of scope | KOS-MIND-001 review |
| D-4 | Memory backend | pluggable interface requirements only; backend deferred | later task |
| D-5 | Core and Sense contract versions | pin when approved; never invent or pin an unapproved version | Sense: pinned to contract 0.1.0 (tag `v0.2.0`) by the owner on 2026-11-02; Core: no Core contract is consumed (proposed, owner to confirm; see [contract/COMPATIBILITY.md](contract/COMPATIBILITY.md)) |
| D-6 | Mind to Skill interaction contract | design jointly with kritva-skill before accepting the interface part of KOS-MIND-001 | kritva-skill review |
| D-8 | Authentication of Mind callers | proposed: outside the Mind request schema; the platform boundary authenticates and Skill independently authorizes (see COMPATIBILITY.md) | owner |
| D-7 | Program authority record | resolved: kritva-program (owner statement in chat, 2026-11-02) | none |

### 8.1 Validator safeguards (D-2)

- A keyword allowlist: a schema that uses a keyword the validator does not implement is rejected, never skipped. At the time of the decision the contract schemas use `$ref`, `$defs`, `type`, `enum`, `const`, `properties`, `required`, `additionalProperties`, `items`, `minItems`, `uniqueItems`, `minimum`, `minLength`, `maxLength`, `pattern`, `propertyNames`, `dependentRequired`, `allOf`, `anyOf`, `not`, `if`/`then` and `format` (`date-time` only).
- Local resolution of the `urn:` schema identifiers; no network access.
- `format` is asserted for `date-time` (RFC 3339), which a default `jsonschema` run does not do.
- Reports every violation, sorted by path then code, so the same input gives the same outcome (AC-004).
- Every example in `examples/manifest.json` must give its expected outcome.
- An optional differential test against `jsonschema` when it is installed; without it the test is reported SKIPPED and never counted as a pass.
- Limit: this validator is not a complete JSON Schema implementation and does not show a result is correct or safe. A new keyword in a schema needs a validator change in the same PR.

## 9. Out of scope

Sensing, motion control, skill orchestration and execution authority, platform foundation, a specific model or framework, ROS 2 as the primary framework (an adapter can be provided later), and any hardware or safety validation claim.

## 10. Program authority

The owner stated in chat (2026-11-02) that kritva-program is the program authority, as [AGENTS.md](AGENTS.md) says. An outside discussion had claimed that `kritva-enterprise-program` is the program record; this repository does not rely on that claim. The statement is not yet recorded in kritva-program itself, so it is an owner statement and not a verified program decision.

## 11. Draft contract fields (for review before any schema is written)

Drafted in an outside discussion; not verified against kritva-sense or kritva-skill and not approved. Names and types may change in KOS-MIND-001.

| Schema | Required | Optional |
|---|---|---|
| mind-request | contract_version, request_id, intent, input (object), context_ref (context_id, revision) | constraints, requested_output, created_at, correlation_id |
| mind-context | context_id, revision (integer), lifecycle_state (CREATED, ACTIVE, SNAPSHOTTED, CLOSED, EXPIRED), created_at, updated_at; at least one of content or snapshot_ref | source_refs, metadata |
| mind-result | contract_version, result_id, request_id, context_ref, status (COMPLETED, PARTIAL, FAILED, CANCELLED), completeness (COMPLETE, PARTIAL, INCOMPLETE), proposed_skills (may be empty), uncertainty, provenance | errors |
| ProposedSkill | skill_id, parameters | version_constraint, preconditions, rationale, priority, uncertainty |

A context update creates a new revision and never overwrites the context an earlier request used. `random_seed` in the execution record is optional. The first schemas ([contract/](contract/README.md)) merge `status` and `completeness` into `status` plus `missing[]`; that is a proposal for review.

## 12. Questions for the joint reviews

**kritva-sense:** which Sense contract version and schema Mind consumes, and how compatibility is managed; which fields carry observations, timestamps, source identity and uncertainty; how stale, missing, partial, invalid and unavailable observations are represented; whether Mind can keep a reference and digest of the original input; ownership and lifecycle of data passed into context.

**kritva-skill:** the canonical skill identity and version-reference format, and whether Mind can propose a version constraint without pinning an unapproved version; what Skill needs to resolve a proposal against its manifest; the parameter schema and precondition format; which validations are Mind's and which Skill repeats before execution; how Skill handles rejected proposals, unmet preconditions, cancellation, partial execution and failure; what Skill returns to keep traceability from proposal to execution; and explicit confirmation that Mind proposes and Skill independently validates and authorizes.
