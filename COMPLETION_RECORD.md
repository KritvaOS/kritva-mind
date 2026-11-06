# Completion record: kritva-mind, V2-M1-MIND-001

Milestone: V2-M1-MIND-001

Status: APPROVED BY THE OWNER IN CHAT ON 2026-11-06, in the interim roles of program decision D-047. This is not independent review. The owner and the reviewer are the same person. The approval was given on a summary of this record drafted by an AI assistant, against commit `0722f3977ed53d793bfb3634c88933601d949e42`; this pull request adds this record, the two role review records and the `ARCHITECTURE.md` corrections after that commit, so the owner re-reads the head before merging.

What this record does and does not do: it is the repository's completion evidence for the milestone outcome "Mind request, context and result contract (task 001) reviewed and tagged v0.1.0" ([planning/MILESTONE.md](planning/MILESTONE.md)). It earns no program credit and adds no weight. kritva-program has no Mind status source and no baseline task for Mind, so the program still reports Mind as unverified; whether it counts the milestone as closed is decided there, not here. A tag is evidence and does not close the milestone ([ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) section 8).

## Scope

Task KOS-MIND-001 ([tasks/KOS-MIND-001/TASK.md](tasks/KOS-MIND-001/TASK.md)): the Mind request, context and result contract, labelled `0.1.0-draft` in the documents.

Included in the release content:

- the JSON Schema 2020-12 schemas and [contract/SEMANTICS.md](contract/SEMANTICS.md), [contract/README.md](contract/README.md) and [contract/COMPATIBILITY.md](contract/COMPATIBILITY.md);
- the valid and invalid examples with `examples/manifest.json`;
- [ARCHITECTURE.md](ARCHITECTURE.md), which stays PROPOSED;
- the Sense and Skill joint review records (outcomes AGREED by the owner, 2026-11-04) and the [closure record](planning/reviews/KOS-MIND-001-CLOSURE.md);
- KOS-MIND-002, which belongs to V2-M2-MIND-001 and was landed first by the owner's decision of 2026-11-06: the standard-library validator, 114 unit tests, `make test-unit` and the `unit-tests` workflow.

Not included: any reasoning provider, memory backend, transport, runtime integration, Core integration, or hardware or safety validation. Nothing here is a claim of any of those.

## Merge commits

Merge commits on `main` for the pull requests of this milestone's work (`git log --first-parent --merges`), with the pull request head each one merged (`merge^2`):

| Pull request | Merge commit | Pull request head |
|---|---|---|
| 9 | `9ec139c218b391cc1f506135387fe49dfe51e5ba` | `8ac56d8b13bc97a8e8e01959e1327e057f4bc549` |
| 10 | `f49af85cd5c08c3d56f52276408ff5dd2fc35795` | `ba741c93f2225ec907835d2620d64d7739dcb6f1` |
| 11 | `50d42e90b2d23fdba6b8353c86a992e112e8823a` | `bb68fa87f60f4a8ce723216e563289baf9fb9cb7` |
| 12 | `bfb4fe3020d68a8a1b37780b90304b6e653e4f12` | `e6473c56ade85aa1fa02d92b7c6dcb56bdabe971` |
| 13 | `1db5823bfe88438ac49a992261c1d2496ff1bda7` | `7a0037ccdb9652cdb75ef45a045e11f4dd116904` |
| 14 | `58cbc81a89e78042cb4237483710bddb281a27de` | `f6fe933ffb5845785af1808972d880a77d52a557` |
| 15 | `db1600ee5118e72285a5d43b6feb51c3e4224936` | `a39b3643f4d57773a3cda30e55a9388e832dc240` |
| 16 | `58d882ed35e13c29954ff6b5f2cb0453462a0b9d` | `7dee2ad0ce59a2ad78a7f2c7e9f55bb22464bddb` |
| 17 | `28432f6b0481d5d5716d9656666adb3b1e9f7154` | `2c773c1f3f779f3f5dde51842458387d096462fc` |
| 18 | `6eadd36cc7bafac18faeffb104d65b739429ebb8` | `be735eb381600502457af2a884d612800014457c` |
| 19 | `7569b801311bb021594ffb8432a911b06645a499` | `bb3863335a5e0725009453743886bbd42e1bee62` |
| 20 | `0cf438627f008ffa2d50d34e48b7c014b95921b0` | `77052becae9a138c725f64381da7e245c4af7e8e` |
| 21 | `1bb7899e2836560e734c0ca870ae4a2bb0e17f2f` | `c4a751cdd40e0d52730b27d653eae716e36efdf2` |
| 22 | `dbb211eb4ba314777a74f8859e59bb99201e3a7b` | `e9113c5f127ca6cd821fe1e2a9b58311a1e802c8` |
| 23 | `f8d97cb0b16660bb50e7074c7d52ad378d34ee72` | `57b81df7219a5f7ee95db845625197bb76b89f7b` |
| 24 | `d821319caea42a22633d7219dc3c237be712fb3a` | `569ceb32cd35f7961f3ef20de0e2f80ae8b6d9c9` |
| 25 | `b59f767268b77075a0ea693f9346d34d9fef83c5` | `4d9364c9b588017bc5927104e48d5a60fda7af85` |
| 26 | `0722f3977ed53d793bfb3634c88933601d949e42` | `95347d63dd256383cdc3f9bff020dbe5a696f5bb` |

The merge commit of the pull request that adds this record is not known until it merges; the tag message names it.

## Release commit and tag

None yet. The annotated tag `v0.1.0` is created only after this record's pull request is merged and the required checks on its merge commit pass. The tag message names this file and that exact merge commit. A tag object named `v0.1.0` was pushed in error on 2026-11-06 and deleted the same day (`git push origin --delete v0.1.0`); it was never a release and nothing was built on it.

## Test runs

Required checks on the pull request heads, all `success`. `pr-acceptance-gate` reports NEEDS_HUMAN as a pass by design, so a green gate is not an approval.

| Pull request | Head | secret-scan | commit-message-check | pr-acceptance-gate | readme-check | unit-tests |
|---|---|---|---|---|---|---|
| 21 | `c4a751cdd40e` | 41599091291 | 41599091518 | 41599091438 | 41599091376 | not yet in place |
| 22 | `e9113c5f127c` | 41599577127 | 41599577132 | 41599577192 | 41599577358 | not yet in place |
| 23 | `57b81df7219a` | 41793128111 | 41793128314 | 41793128212 | 41793128175 | not yet in place |
| 24 | `569ceb32cd35` | 41793913204 | 41793913126 | 41793913096 | 41793913059 | not yet in place |
| 25 | `4d9364c9b588` | 42215933364 | 42215933178 | 42215933580 | 42215933488 | 42215933475 |
| 26 | `95347d63dd25` | 42216852031 | 42216852234 | 42216852131 | 42216852104 | 42216852152 |

Push-to-`main` runs (these run `secret-scan`, `readme-check` and `unit-tests` only), all `success`:

| `main` commit | unit-tests | secret-scan | readme-check |
|---|---|---|---|
| `b59f767268b77075a0ea693f9346d34d9fef83c5` (pull request 25) | 42215995601 | 42215995580 | 42215995450 |
| `0722f3977ed53d793bfb3634c88933601d949e42` (pull request 26) | 42217045130 | 42217045155 | 42217045175 |

Pull requests 9 to 20 are not listed: their check runs were not re-collected for this record.

Gates:

| Gate | Result |
|---|---|
| `make test-unit` | 114 unit tests under `tests/validator/`, run in CI (`unit-tests`, runs above) and locally. The workflow is not a required check; making it one needs an owner-approved kritva-program pipeline update |
| `make check`, `make docs-check` | author-run only, not in CI; the results for this record's own change are pasted in its pull request |
| `make check-readme` | author-run and in CI as `readme-check` (runs above) |
| `make test-integration`, `make test-regression`, `make test`, `make lint`, `make acceptance` | NOT_IMPLEMENTED, exit 3. They are not passes and no criterion relies on them |

The checks for this record's own pull request head and merge commit are recorded in the tag message, not here, because they do not exist when this is written.

## Criteria disposition

Dispositions use the program standard's vocabulary: PASS, WAIVED with an approval reference, NOT_APPLICABLE with an approval reference. A waiver covers only the part named in its scope; the rest of the criterion is judged as stated. A waived criterion is not reported as met.

Approval reference for every disposition and waiver below: the owner's decisions in chat on 2026-11-06 (Dinesh, REPO_CODE_OWNER, interim, D-047). No separate approval record exists, and approver and requester are the same person.

| AC | Disposition | Basis |
|---|---|---|
| AC-001 | PASS | versioned request, context and result schemas with a stable context identity; every example in `examples/manifest.json` gives its stated outcome (`test_examples.py`, `test_contract_keywords.py`) |
| AC-002 | PASS | `Uncertainty`, `Error`, the FAILED-needs-an-ERROR rule and the error-mapping table; error-path examples and `ErrorMapping` tests |
| AC-003 | WAIVED (W-1) | cancellation is specified as a transport-independent operation and its rules are tested (`Cancellation` in `test_semantics.py`); the wire format of `cancel` is not defined |
| AC-004 | PASS | `test_determinism.py`: same input and context, same validation outcome and the same ordering of violations |
| AC-005 | WAIVED (W-2) | Sense is consumed only through its pinned contract 0.1.0 (tag `v0.2.0`); observations are referenced, never embedded; no Core contract is consumed (C-5); no integration at the real Sense boundary |
| AC-006 | PASS | owner's [architecture review record](planning/reviews/KOS-MIND-001-ARCHITECTURE-REVIEW.md) written for this record; not independent |
| AC-007 | WAIVED (W-3) | no field authorizes or executes; unknown fields are rejected; the Skill review outcome is AGREED; cross-repository tests do not exist |
| AC-008 | WAIVED (W-4) | the lifecycle and its legal transitions are specified and tested at the validator level (`ContextLifecycle`); operational lifecycle tests do not exist |
| AC-009 | WAIVED (W-5) | contract-level only: no cloud dependency, an unavailable provider is explicit; no disconnected-operation test exists |
| AC-010 | WAIVED (W-5) | contract-level only: `provider_id` and optional `placement` in provenance; no per-provider conformance test exists |
| AC-011 | WAIVED (W-6) | the execution record, digests, context snapshot and replay class are specified and schema-tested; no replay comparison exists |

Waivers:

| ID | Scope (the deferred part only) | Rationale | Review condition |
|---|---|---|---|
| W-1 | wire format of `cancel` (AC-003) | transport is decided separately from the contract and depends on a platform design that does not exist | reviewed at the completion record of V2-M2-MIND-001, or when a transport is chosen, whichever is first |
| W-2 | integration tests at the real Sense boundary and enforcement of the Sense version pin in a running pipeline (AC-005), KOS-MIND-004 | needs `make test-integration`, which is NOT_IMPLEMENTED, and a Sense implementation to run against | at the completion record of V2-M2-MIND-001 |
| W-3 | cross-repository Mind-to-Skill tests (AC-007), KOS-MIND-007 | needs an agreed Skill contract and the program control-plane milestone | at the completion record of V2-M5-MIND-001 |
| W-4 | operational context-lifecycle tests (AC-008), KOS-MIND-003 | the lifecycle rules are tested at the validator level; end-to-end behaviour needs the lifecycle checks task | at the completion record of V2-M2-MIND-001 |
| W-5 | disconnected-operation tests (AC-009) and edge, nexus and cloud conformance tests (AC-010), KOS-MIND-003 | no provider or deployment exists to test; the contract-level part is stated and reviewed | at the completion record of V2-M2-MIND-001 |
| W-6 | replay comparison (AC-011), KOS-MIND-006 | needs recorded inputs and a provider; replay results would be labelled simulation | at the completion record of V2-M5-MIND-001 |

PASS here means the criterion as written is met by the evidence listed, judged by the interim reviewer. It is not safety validation, and it does not show that the 0.1.0-draft contract is correct for every consumer.

## Deferred work

- Tasks KOS-MIND-003, 004, 005, 006, 007 and 008 are candidates in [planning/TASK_CATALOGUE.md](planning/TASK_CATALOGUE.md) and [planning/TASKS.md](planning/TASKS.md), not registered, with no weight or credit.
- A Mind status generator (`status/status.json`) and the program registration: a baseline entry, `sources.json`, evidence and the approvals in kritva-program. Owner decisions in that repository.
- Skill side: Skill's design note is proposed, not approved, and still names an older Mind revision (`7569b80`) and a `mind_result_digest` wording that conflicts with SEMANTICS.md section 7 (tracked as SK-11). SK-12 to SK-14 are open outside this repository.
- Findings from KOS-MIND-002 ([tasks/KOS-MIND-002/TASK.md](tasks/KOS-MIND-002/TASK.md)) that change no contract text here: `CREATED` on a later revision (finding 2), and a `SNAPSHOTTED` revision needing a `snapshot_ref` with a digest, which the schema alone does not require (finding 4). Not checked by any implementation: `expires_at` against a clock, whole-result digests, context retrieval, `updated_at` ordering.
- [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) section 5 (test gates) is stale: it lists the unit gate as NOT_IMPLEMENTED. It is a protected file and needs its own criteria review; this record does not edit it.
- Independent review of the architecture, code and safety roles (D-047 is interim).
- Pull requests 9 to 20 were not re-reviewed for this record.

Known limitations carried into `v0.1.0`:

1. Ingress authentication is not specified or verified (owner decision C-5). Mind must not be exposed to untrusted callers until the platform boundary is defined, implemented and reviewed. Wording: [tasks/KOS-MIND-001/TASK.md](tasks/KOS-MIND-001/TASK.md).
2. The validator is limited (D-2). It does not check `expires_at` against a clock, whole-result digests, context retrieval, the wire format of `cancel` or `updated_at` ordering, and it enforces the pinned Sense version only when a version is passed to it. A passing run shows that the validator and the examples agree.
3. Nothing was reviewed independently.
4. The architecture document is a proposal, not an accepted baseline.

## Approvals

| Role | Name | Date | Commit reviewed | Record |
|---|---|---|---|---|
| REPO_CODE_OWNER (interim, D-047) | Dinesh | 2026-11-06 | `0722f3977ed53d793bfb3634c88933601d949e42` | [code-owner review record](planning/reviews/KOS-MIND-001-CODE-OWNER-REVIEW.md) |
| ARCHITECTURE_REVIEWER (interim, D-047) | Dinesh | 2026-11-06 | `0722f3977ed53d793bfb3634c88933601d949e42` | [architecture review record](planning/reviews/KOS-MIND-001-ARCHITECTURE-REVIEW.md) |

The approvals were given in chat; no separate approval record exists. The roles are those in `.github/kritva-gate.json`. GitHub does not count an author's own approval, so merging needs the owner's ruleset bypass, as `.github/CODEOWNERS` says.

## Evidence

- Exact commits and pull requests: the merge table above. The contract text is unchanged since `d821319caea42a22633d7219dc3c237be712fb3a` (pull request 24); pull requests 25 and 26 touched no file under `contract/` or `examples/`.
- Review records: [Sense](planning/reviews/KOS-MIND-001-SENSE-REVIEW.md) and [Skill](planning/reviews/KOS-MIND-001-SKILL-REVIEW.md) (AGREED), the [closure record](planning/reviews/KOS-MIND-001-CLOSURE.md), the [code-owner record](planning/reviews/KOS-MIND-001-CODE-OWNER-REVIEW.md) and the [architecture record](planning/reviews/KOS-MIND-001-ARCHITECTURE-REVIEW.md).
- Skill side: kritva-skill `origin/main` was fetched on 2026-11-06 and is still `c17192001f6c672819589857e8644ad21573d8d8`, the revision the Skill review record names.
- CI run IDs: the tables above.
