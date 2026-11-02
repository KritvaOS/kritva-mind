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

## 3. Logical subsystems

These are logical components, not approved modules or folders.

| Subsystem | Responsibility | First needed |
|---|---|---|
| Mind Core | Request lifecycle, coordination, cancellation | contract (V2-M1) |
| Mind Context | Task and robot-state context, history, stable context identity | contract (V2-M1) |
| Mind Validation | Schema and semantic validation, uncertainty and error reporting | contract (V2-M1); implementation V2-M2 |
| Mind Reasoning | Inference behind an adapter interface; interpretation and proposals | V2-M2 to V2-M5 |
| Mind Planning | Goal decomposition into proposed skill invocations | V2-M5 |
| Mind Knowledge | Retrieval and memory behind an abstract interface; backend deferred | V2-M2 to V2-M5 |
| Mind Runtime | Adapters and deployment independent of execution | after the contract |

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
| Request | identity, schema version, task and constraints, time and units, optional deadline |
| Context | stable context identity, lifecycle (create, update, expire), source and version of each Sense input |
| Result | context identity, proposal, uncertainty fields, error fields, provenance, completeness (complete, partial, cancelled, failed) |
| Cancellation | who may cancel, when, what a partial result contains |
| Versioning | MAJOR.MINOR.PATCH, compatibility rules, deprecation |

Field names and encodings are not chosen here. The encoding (for example JSON Schema) is decision D-1 in section 8.

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
| D-1 | Contract encoding | JSON Schema; transport decided separately | owner decision |
| D-2 | Implementation language of validators | Python 3, standard library only, as the existing scripts | owner decision |
| D-3 | Stateless requests or persistent context | explicit context identity and lifecycle | KOS-MIND-001 review |
| D-4 | Memory backend | pluggable interface; defer backend | later task |
| D-5 | Core and Sense contract versions | pin when approved | approval in those repositories |
| D-6 | Mind to Skill interaction contract | design jointly with kritva-skill | kritva-skill review |

## 9. Out of scope

Sensing, motion control, skill orchestration and execution authority, platform foundation, a specific model or framework, ROS 2 as the primary framework (an adapter can be provided later), and any hardware or safety validation claim.
