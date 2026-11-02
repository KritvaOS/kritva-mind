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
| Proposed skill | skill reference, compatible version or constraint, proposed parameters, known preconditions, rationale, proposal-level uncertainty, priority |
| Uncertainty | an optional score with a defined scale, source and calibration status, plus qualitative uncertainty and assumptions; never a single number standing in for uncertainty |
| Cancellation | who may cancel, when, what a partial result contains and which information is missing |
| Execution record (provenance) | input and context snapshot references with digests, provider, model and version, provider configuration and prompt template digests, inference parameters, seed if supported, output snapshot and digest, timestamp, tool versions, replay class |
| Versioning | MAJOR.MINOR.PATCH, compatibility rules, deprecation |

Execution authority is not granted by Mind: the result has no `authorized` or `execute` field that Skill must trust. Skill resolves the skill reference, validates its manifest, version and preconditions, and decides. Mind may validate parameters structurally against a skill's declared input schema; Skill stays authoritative at execution time.

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
| D-2 | Validator implementation | not decided in KOS-MIND-001. The Python standard library has no full JSON Schema validator, so the choice is a pinned third-party validator or a limited dependency-free validator that documents unsupported features | owner decision in the validation task |
| D-3 | Context persistence | identity and lifecycle in the contract; backend out of scope | KOS-MIND-001 review |
| D-4 | Memory backend | pluggable interface requirements only; backend deferred | later task |
| D-5 | Core and Sense contract versions | pin when approved; never invent or pin an unapproved version | approval in those repositories |
| D-6 | Mind to Skill interaction contract | design jointly with kritva-skill before accepting the interface part of KOS-MIND-001 | kritva-skill review |
| D-7 | Program authority record | see section 10 | owner |

## 9. Out of scope

Sensing, motion control, skill orchestration and execution authority, platform foundation, a specific model or framework, ROS 2 as the primary framework (an adapter can be provided later), and any hardware or safety validation claim.

## 10. Unverified claim about the program record

An outside discussion stated that `kritva-enterprise-program` (private) is the program record and `kritva-program` (public) is a projection of it, contrary to what this repository's documents say. That was not verified here. This repository keeps naming kritva-program as in [AGENTS.md](AGENTS.md) until the owner confirms the hierarchy; nothing in this repository is changed on that basis.
