"""Semantic rules JSON Schema cannot express (contract/SEMANTICS.md).

Every rule here cites the SEMANTICS.md section it implements. Nothing is
invented: a rule that SEMANTICS.md leaves open is not implemented, and is
listed in tasks/KOS-MIND-002/TASK.md instead.

Functions are pure and deterministic: no clock, no I/O, no randomness. Callers
that need "now" pass it in (the Sense rule, section 6, requires the consumer's
own now and clock). All functions tolerate documents that are not structurally
valid, so they can run alongside schema validation and report everything.

Rule ids (Violation.code):
  S-PROPOSAL-ID-UNIQUE        SEMANTICS.md section 4
  S-VERSION-RANGE             section 3
  S-ERROR-MAPPING             section 6 (error mapping table)
  S-OBSERVATION-USABLE        section 6 (`usable`)
  S-SENSE-CONTRACT-VERSION    section 6 (Version), only when a version is pinned
  S-CONTEXT-INITIAL           section 2 (first revision is CREATED)
  S-CONTEXT-TRANSITION        section 2 (legal transitions, revision +1)
  S-CONTEXT-UNUSABLE          section 2 (CLOSED or EXPIRED)
  S-BINDING                   a result or request names the context it ran in
  S-CANCEL                    section 1 (cancel outcomes)
"""

from __future__ import annotations

import re
from typing import Any, Optional

from .jsonschema_lite import Violation, sort_violations

_RANGE = re.compile(
    r"\A>=([0-9]+)\.([0-9]+)\.([0-9]+) <([0-9]+)\.([0-9]+)\.([0-9]+)\Z"
)

MIND_INPUT_CODES = ("MIND_INPUT_STALE", "MIND_INPUT_MISSING", "MIND_INPUT_INVALID")

# SEMANTICS.md section 6: Sense error code -> Mind error code. Any Sense code
# not listed (for example from a later Sense version) maps to MIND_INPUT_INVALID.
SENSE_TO_MIND = {
    "STALE_DATA": "MIND_INPUT_STALE",
    "MISSING_DATA": "MIND_INPUT_MISSING",
}
_DEFAULT_MIND_CODE = "MIND_INPUT_INVALID"

TERMINAL_STATUSES = ("COMPLETED", "PARTIAL", "FAILED", "CANCELLED")

# SEMANTICS.md section 2, from -> allowed next states (each is a new revision).
_ALLOWED_TRANSITIONS = {
    "CREATED": ("ACTIVE", "CLOSED", "EXPIRED"),
    "ACTIVE": ("ACTIVE", "SNAPSHOTTED", "CLOSED", "EXPIRED"),
    "SNAPSHOTTED": ("ACTIVE", "CLOSED", "EXPIRED"),
    "CLOSED": (),
    "EXPIRED": (),
}


def expected_mind_code(sense_error_code: str) -> str:
    return SENSE_TO_MIND.get(sense_error_code, _DEFAULT_MIND_CODE)


# --------------------------------------------------------------------------
# Version constraints (section 3)
# --------------------------------------------------------------------------


def parse_version(text: str) -> tuple:
    m = re.fullmatch(r"([0-9]+)\.([0-9]+)\.([0-9]+)", text)
    if not m:
        raise ValueError(f"not a MAJOR.MINOR.PATCH version: {text!r}")
    return tuple(int(x) for x in m.groups())


def version_satisfies(constraint: str, version: str) -> bool:
    """Contract semantics of a VersionConstraint, not a SemVer library default.

    exact X.Y.Z   matches only that version.
    caret ^X.Y.Z  matches >= X.Y.Z with the same MAJOR (MAJOR != 0), or the
                  same MINOR when MAJOR is 0.
    range         matches >= lower and strictly < upper; an invalid range
                  (lower not strictly below upper) matches nothing here and is
                  reported by check_version_constraint.
    """
    v = parse_version(version)
    if constraint.startswith("^"):
        c = parse_version(constraint[1:])
        if v < c:
            return False
        return v[0] == c[0] if c[0] != 0 else (v[0] == 0 and v[1] == c[1])
    m = _RANGE.match(constraint)
    if m:
        lower = tuple(int(x) for x in m.groups()[:3])
        upper = tuple(int(x) for x in m.groups()[3:])
        return lower < upper and lower <= v < upper
    return v == parse_version(constraint)


def check_version_constraint(constraint: Any, path: tuple = ()) -> list:
    """A range whose lower bound is not strictly below its upper bound is invalid."""
    if not isinstance(constraint, str):
        return []
    m = _RANGE.match(constraint)
    if not m:
        return []
    lower = tuple(int(x) for x in m.groups()[:3])
    upper = tuple(int(x) for x in m.groups()[3:])
    if not lower < upper:
        return [Violation(path, "S-VERSION-RANGE", f"range {constraint!r}: lower bound must be strictly below the upper bound")]
    return []


# --------------------------------------------------------------------------
# Proposals (section 4)
# --------------------------------------------------------------------------


def order_proposals(proposals: list) -> list:
    """Consumer order: priority ascending (0 first), a missing priority after
    every proposal that has one, ties by proposal_id ascending by code point.
    The array order is not authoritative."""
    def key(p):
        prio = p.get("priority")
        has = isinstance(prio, int) and not isinstance(prio, bool)
        return (0, prio, p.get("proposal_id", "")) if has else (1, 0, p.get("proposal_id", ""))

    return sorted(proposals, key=key)


# --------------------------------------------------------------------------
# Result rules
# --------------------------------------------------------------------------


def check_result(result: Any) -> list:
    """Rules a single result document must satisfy beyond its schema."""
    out: list = []
    if not isinstance(result, dict):
        return out

    proposals = result.get("proposed_skills")
    if isinstance(proposals, list):
        first_seen: dict = {}
        for i, p in enumerate(proposals):
            if not isinstance(p, dict):
                continue
            pid = p.get("proposal_id")
            if isinstance(pid, str):
                if pid in first_seen:
                    out.append(
                        Violation(
                            ("proposed_skills", i, "proposal_id"),
                            "S-PROPOSAL-ID-UNIQUE",
                            f"proposal_id {pid!r} already used by proposed_skills[{first_seen[pid]}]",
                        )
                    )
                else:
                    first_seen[pid] = i
            out += check_version_constraint(p.get("version_constraint"), ("proposed_skills", i, "version_constraint"))

    errors = result.get("errors")
    if isinstance(errors, list):
        for i, e in enumerate(errors):
            if not isinstance(e, dict):
                continue
            detail = e.get("detail")
            sense = detail.get("sense_error_code") if isinstance(detail, dict) else None
            if e.get("code") in MIND_INPUT_CODES and isinstance(sense, str):
                want = expected_mind_code(sense)
                if e["code"] != want:
                    out.append(
                        Violation(
                            ("errors", i, "code"),
                            "S-ERROR-MAPPING",
                            f"Sense code {sense} maps to {want}, not {e['code']}",
                        )
                    )
    return sort_violations(out)


# --------------------------------------------------------------------------
# Context and observation rules
# --------------------------------------------------------------------------


def _evaluates_freshness(policy: Any) -> bool:
    # Sense 6.1: freshness is evaluated only when the consumer's now, its clock
    # and max_age_ns are all given.
    return (
        isinstance(policy, dict)
        and isinstance(policy.get("max_age_ns"), int)
        and isinstance(policy.get("now_ns"), int)
        and policy.get("clock") in ("monotonic", "utc")
    )


def observation_usable_ceiling(obs: dict, policy: Optional[dict]) -> tuple:
    """(may_be_usable, reason). `usable` may be true only if this is true."""
    if obs.get("validity") != "VALID":
        return False, f"validity is {obs.get('validity')}"
    if not _evaluates_freshness(policy):
        return True, ""
    if obs.get("clock") != policy["clock"]:
        return False, "observation clock differs from the consumer clock (INVALID_TIMESTAMP)"
    ts = obs.get("timestamp_ns")
    if not isinstance(ts, int):
        return True, ""
    if ts > policy["now_ns"]:
        return False, "observation is newer than the consumer's now (INVALID_TIMESTAMP)"
    per_sensor = policy.get("per_sensor_max_age_ns") or {}
    limit = per_sensor.get(obs.get("sensor_id"), policy["max_age_ns"])
    if isinstance(limit, int) and policy["now_ns"] - ts > limit:  # equal to the limit is fresh
        return False, f"age {policy['now_ns'] - ts} ns exceeds max_age_ns {limit} (STALE_DATA)"
    return True, ""


def check_observations(context: Any, freshness: Optional[dict] = None, sense_contract_version: Optional[str] = None) -> list:
    """`usable` is true only if validity is VALID and, when freshness was
    evaluated, the sample is fresh and from the same clock (section 6)."""
    out: list = []
    obs_list = context.get("observations") if isinstance(context, dict) else None
    if not isinstance(obs_list, list):
        return out
    for i, obs in enumerate(obs_list):
        if not isinstance(obs, dict):
            continue
        ok, why = observation_usable_ceiling(obs, freshness)
        if obs.get("usable") is True and not ok:
            out.append(Violation(("observations", i, "usable"), "S-OBSERVATION-USABLE", f"usable must be false: {why}"))
        if sense_contract_version is not None and obs.get("source_contract") != sense_contract_version:
            out.append(
                Violation(
                    ("observations", i, "source_contract"),
                    "S-SENSE-CONTRACT-VERSION",
                    f"expected the pinned Sense contract version {sense_contract_version}, got {obs.get('source_contract')!r}",
                )
            )
    return sort_violations(out)


def check_context(context: Any, freshness: Optional[dict] = None, sense_contract_version: Optional[str] = None) -> list:
    out = list(check_observations(context, freshness, sense_contract_version))
    if isinstance(context, dict):
        rev, state = context.get("revision"), context.get("lifecycle_state")
        if rev == 1 and state is not None and state != "CREATED":
            out.append(Violation(("lifecycle_state",), "S-CONTEXT-INITIAL", "revision 1 is the CREATED revision"))
        if isinstance(rev, int) and rev > 1 and state == "CREATED":
            out.append(Violation(("lifecycle_state",), "S-CONTEXT-INITIAL", "CREATED is only the first revision"))
    return sort_violations(out)


def check_context_transition(prev: Any, nxt: Any) -> list:
    """`nxt` must be a legal next revision of `prev` (section 2)."""
    out: list = []
    if not (isinstance(prev, dict) and isinstance(nxt, dict)):
        return out
    if prev.get("context_id") != nxt.get("context_id"):
        out.append(Violation(("context_id",), "S-CONTEXT-TRANSITION", "context_id is immutable"))
    if prev.get("created_at") != nxt.get("created_at"):
        out.append(Violation(("created_at",), "S-CONTEXT-TRANSITION", "created_at never changes"))
    pr, nr = prev.get("revision"), nxt.get("revision")
    if isinstance(pr, int) and nr != pr + 1:
        out.append(Violation(("revision",), "S-CONTEXT-TRANSITION", f"revision must be {pr + 1}, got {nr!r}"))
    ps, ns = prev.get("lifecycle_state"), nxt.get("lifecycle_state")
    if ps in _ALLOWED_TRANSITIONS and ns not in _ALLOWED_TRANSITIONS[ps]:
        out.append(Violation(("lifecycle_state",), "S-CONTEXT-TRANSITION", f"{ps} -> {ns} is not a legal transition"))
    if ps == "ACTIVE" and ns == "SNAPSHOTTED":
        ref = nxt.get("snapshot_ref")
        if not (isinstance(ref, dict) and "ref" in ref and "digest" in ref):
            out.append(Violation(("snapshot_ref",), "S-CONTEXT-TRANSITION", "a SNAPSHOTTED revision records a snapshot reference and digest"))
    return sort_violations(out)


# --------------------------------------------------------------------------
# Request, context and result together
# --------------------------------------------------------------------------


def check_request_context(request: Any, context: Any, sense_contract_version: Optional[str] = None) -> list:
    """The context a request names must exist as that revision, be usable, and
    its observations must respect the request's freshness policy."""
    out: list = []
    if not (isinstance(request, dict) and isinstance(context, dict)):
        return out
    ref = request.get("context_ref")
    if isinstance(ref, dict) and (
        ref.get("context_id") != context.get("context_id") or ref.get("revision") != context.get("revision")
    ):
        out.append(Violation(("context_ref",), "S-BINDING", "context_ref does not name this context revision"))
    if context.get("lifecycle_state") in ("CLOSED", "EXPIRED"):
        out.append(
            Violation(
                ("context_ref",),
                "S-CONTEXT-UNUSABLE",
                f"a {context['lifecycle_state']} revision cannot be the context of a new request (FAILED with MIND_INPUT_INVALID)",
            )
        )
    constraints = request.get("constraints")
    policy = constraints.get("freshness") if isinstance(constraints, dict) else None
    for v in check_observations(context, policy, sense_contract_version):
        out.append(Violation(("context",) + v.path, v.code, v.message))
    return sort_violations(out)


def check_result_for_request(request: Any, result: Any) -> list:
    out: list = []
    if not (isinstance(request, dict) and isinstance(result, dict)):
        return out
    if request.get("request_id") != result.get("request_id"):
        out.append(Violation(("request_id",), "S-BINDING", "result.request_id differs from the request"))
    if request.get("context_ref") != result.get("context_ref"):
        out.append(Violation(("context_ref",), "S-BINDING", "result.context_ref differs from the request"))
    return sort_violations(out)


# --------------------------------------------------------------------------
# Cancellation (section 1)
# --------------------------------------------------------------------------


def check_cancel_outcome(prior_result: Any, after_cancel: Any) -> list:
    """Judge the result held after a `cancel(request_id)`.

    prior_result is None when the request was non-terminal: the outcome must be
    a CANCELLED result. When the request already had a terminal result, a late
    cancel never rewrites it, so the result must be unchanged. Cancelling twice
    is idempotent, so the same check applies to a repeated cancel.
    """
    from .jsonschema_lite import json_equal

    if prior_result is None:
        if not (isinstance(after_cancel, dict) and after_cancel.get("status") == "CANCELLED"):
            return [Violation(("status",), "S-CANCEL", "cancelling a non-terminal request ends in a CANCELLED result")]
        return []
    if isinstance(prior_result, dict) and prior_result.get("status") in TERMINAL_STATUSES:
        if not json_equal(prior_result, after_cancel):
            return [Violation((), "S-CANCEL", "a late cancel never rewrites a terminal result")]
    return []
