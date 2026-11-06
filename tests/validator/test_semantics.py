"""Semantic rules of contract/SEMANTICS.md (AC-002, AC-003, AC-008, AC-011)."""

import unittest

import _helpers
from _helpers import codes, edit, valid, validator
from kritva_mind import semantics as sem

RESULT = valid("result-two-proposals-with-constraints.json")
CONTEXT = valid("context-with-observations.json")


class ProposalRules(unittest.TestCase):
    def test_duplicate_proposal_id_is_reported_at_the_second_use(self):
        doc = edit(RESULT, lambda d: d["proposed_skills"][1].update(proposal_id=d["proposed_skills"][0]["proposal_id"]))
        v = validator().validate("result", doc)
        self.assertEqual(codes(v), ["S-PROPOSAL-ID-UNIQUE"])
        self.assertEqual(v[0].pointer, "/proposed_skills/1/proposal_id")

    def test_distinct_proposal_ids_pass(self):
        self.assertEqual(validator().validate("result", RESULT), [])

    def test_proposal_id_uniqueness_is_case_sensitive(self):
        doc = edit(RESULT, lambda d: d["proposed_skills"][1].update(proposal_id=d["proposed_skills"][0]["proposal_id"].upper()))
        self.assertEqual(validator().validate("result", doc), [])

    def test_range_with_lower_bound_not_below_upper_is_invalid(self):
        for bad in (">=2.0.0 <2.0.0", ">=2.0.0 <1.0.0", ">=1.10.0 <1.9.0"):
            with self.subTest(constraint=bad):
                doc = edit(RESULT, lambda d: d["proposed_skills"][0].update(version_constraint=bad))
                v = validator().validate("result", doc)
                self.assertEqual(codes(v), ["S-VERSION-RANGE"])
                self.assertEqual(v[0].pointer, "/proposed_skills/0/version_constraint")

    def test_range_with_lower_bound_below_upper_is_valid(self):
        for ok in (">=1.0.0 <2.0.0", ">=1.2.3 <1.2.4", ">=0.0.0 <0.0.1", ">=1.9.0 <1.10.0"):
            with self.subTest(constraint=ok):
                doc = edit(RESULT, lambda d: d["proposed_skills"][0].update(version_constraint=ok))
                self.assertEqual(validator().validate("result", doc), [])

    def test_order_by_priority_then_proposal_id_with_missing_priority_last(self):
        props = [
            {"proposal_id": "b", "priority": 1},
            {"proposal_id": "z"},
            {"proposal_id": "a"},
            {"proposal_id": "c", "priority": 0},
            {"proposal_id": "a2", "priority": 1},
            {"proposal_id": "B", "priority": 1},
        ]
        got = [p["proposal_id"] for p in sem.order_proposals(props)]
        self.assertEqual(got, ["c", "B", "a2", "b", "a", "z"])  # code point order: "B" < "a2" < "b"

    def test_order_does_not_depend_on_array_order(self):
        props = [{"proposal_id": "p%d" % i, "priority": i % 3} for i in range(9)]
        self.assertEqual(sem.order_proposals(props), sem.order_proposals(list(reversed(props))))


class VersionSemantics(unittest.TestCase):
    def test_exact(self):
        self.assertTrue(sem.version_satisfies("1.0.3", "1.0.3"))
        self.assertFalse(sem.version_satisfies("1.0.3", "1.0.4"))

    def test_caret_nonzero_major(self):
        c = "^1.2.0"
        for v, ok in (("1.2.0", True), ("1.9.9", True), ("1.1.9", False), ("2.0.0", False), ("0.9.0", False)):
            with self.subTest(v=v):
                self.assertEqual(sem.version_satisfies(c, v), ok)

    def test_caret_zero_major_pins_the_minor(self):
        c = "^0.2.3"
        for v, ok in (("0.2.3", True), ("0.2.9", True), ("0.2.2", False), ("0.3.0", False), ("1.2.3", False)):
            with self.subTest(v=v):
                self.assertEqual(sem.version_satisfies(c, v), ok)

    def test_range_is_half_open(self):
        c = ">=1.2.0 <2.0.0"
        for v, ok in (("1.2.0", True), ("1.99.99", True), ("2.0.0", False), ("1.1.99", False)):
            with self.subTest(v=v):
                self.assertEqual(sem.version_satisfies(c, v), ok)

    def test_invalid_range_matches_nothing(self):
        self.assertFalse(sem.version_satisfies(">=2.0.0 <1.0.0", "1.5.0"))
        self.assertFalse(sem.version_satisfies(">=1.0.0 <1.0.0", "1.0.0"))

    def test_versions_compare_numerically_not_as_text(self):
        self.assertTrue(sem.version_satisfies(">=1.2.0 <1.10.0", "1.9.0"))
        self.assertFalse(sem.version_satisfies("^1.10.0", "1.9.0"))


class ErrorMapping(unittest.TestCase):
    def with_error(self, code, sense):
        base = valid("result-completed-edge-with-warning.json")
        return edit(base, lambda d: d["errors"][0].update(code=code, detail={"sense_error_code": sense}))

    def test_table(self):
        table = {
            "STALE_DATA": "MIND_INPUT_STALE",
            "MISSING_DATA": "MIND_INPUT_MISSING",
            "INVALID_DATA": "MIND_INPUT_INVALID",
            "INVALID_TIMESTAMP": "MIND_INPUT_INVALID",
            "SEQUENCE_REGRESSION": "MIND_INPUT_INVALID",
            "UNKNOWN_FRAME": "MIND_INPUT_INVALID",
            "INVALID_UNIT": "MIND_INPUT_INVALID",
            "NON_FINITE_VALUE": "MIND_INPUT_INVALID",
            "MISSING_FIELD": "MIND_INPUT_INVALID",
            "MALFORMED_FIELD": "MIND_INPUT_INVALID",
            "UNKNOWN_FIELD": "MIND_INPUT_INVALID",
            "INVALID_SENSOR_ID": "MIND_INPUT_INVALID",
            "INVALID_VALIDITY": "MIND_INPUT_INVALID",
            "UNSUPPORTED_CONTRACT_VERSION": "MIND_INPUT_INVALID",
            "SOME_FUTURE_SENSE_CODE": "MIND_INPUT_INVALID",
        }
        for sense, mind in table.items():
            with self.subTest(sense=sense):
                self.assertEqual(sem.expected_mind_code(sense), mind)
                self.assertEqual(validator().validate("result", self.with_error(mind, sense)), [])

    def test_wrong_mind_code_for_a_sense_code_is_reported(self):
        for sense, wrong in (("STALE_DATA", "MIND_INPUT_INVALID"), ("MISSING_DATA", "MIND_INPUT_STALE"), ("INVALID_TIMESTAMP", "MIND_INPUT_STALE"), ("SOME_FUTURE_SENSE_CODE", "MIND_INPUT_MISSING")):
            with self.subTest(sense=sense):
                v = validator().validate("result", self.with_error(wrong, sense))
                self.assertEqual(codes(v), ["S-ERROR-MAPPING"])
                self.assertEqual(v[0].pointer, "/errors/0/code")

    def test_other_mind_codes_are_not_mapped(self):
        doc = self.with_error("MIND_TIMEOUT", "STALE_DATA")
        self.assertEqual(validator().validate("result", doc), [])


class ObservationUsable(unittest.TestCase):
    def policy(self, **kw):
        p = {"max_age_ns": 1_000, "clock": "utc", "now_ns": 1_793_613_590_000_001_000}
        p.update(kw)
        return p

    def ctx(self, ts, clock="utc", validity="VALID", usable=True, sensor="imu.base"):
        obs = {"sensor_id": sensor, "sequence": 1, "clock": clock, "timestamp_ns": ts, "validity": validity, "usable": usable, "source_contract": "0.1.0"}
        if validity != "VALID":
            obs["sense_error_code"] = "STALE_DATA"
        return {"observations": [obs]}

    NOW = 1_793_613_590_000_001_000

    def test_age_equal_to_the_limit_is_fresh(self):
        self.assertEqual(sem.check_observations(self.ctx(self.NOW - 1_000), self.policy()), [])

    def test_age_over_the_limit_cannot_be_usable(self):
        v = sem.check_observations(self.ctx(self.NOW - 1_001), self.policy())
        self.assertEqual(codes(v), ["S-OBSERVATION-USABLE"])
        self.assertIn("STALE_DATA", v[0].message)

    def test_zero_max_age_allows_only_age_zero(self):
        self.assertEqual(sem.check_observations(self.ctx(self.NOW), self.policy(max_age_ns=0)), [])
        self.assertTrue(sem.check_observations(self.ctx(self.NOW - 1), self.policy(max_age_ns=0)))

    def test_future_sample_cannot_be_usable(self):
        v = sem.check_observations(self.ctx(self.NOW + 1), self.policy())
        self.assertIn("INVALID_TIMESTAMP", v[0].message)

    def test_different_clock_cannot_be_usable(self):
        v = sem.check_observations(self.ctx(self.NOW, clock="monotonic"), self.policy())
        self.assertIn("clock", v[0].message)

    def test_per_sensor_override_wins(self):
        pol = self.policy(per_sensor_max_age_ns={"imu.base": 10})
        self.assertTrue(sem.check_observations(self.ctx(self.NOW - 500), pol))
        pol = self.policy(max_age_ns=10, per_sensor_max_age_ns={"imu.base": 5_000})
        self.assertEqual(sem.check_observations(self.ctx(self.NOW - 500), pol), [])

    def test_freshness_not_evaluated_without_now_or_clock(self):
        old = self.ctx(0)
        self.assertEqual(sem.check_observations(old, {"max_age_ns": 1}), [])
        self.assertEqual(sem.check_observations(old, {"max_age_ns": 1, "now_ns": self.NOW}), [])
        self.assertEqual(sem.check_observations(old, None), [])

    def test_unusable_is_always_allowed(self):
        self.assertEqual(sem.check_observations(self.ctx(0, usable=False), self.policy()), [])

    def test_not_valid_validity_cannot_be_usable_even_without_a_policy(self):
        v = sem.check_observations(self.ctx(5, validity="STALE", usable=True))
        self.assertEqual(codes(v), ["S-OBSERVATION-USABLE"])

    def test_pinned_sense_contract_version(self):
        self.assertEqual(sem.check_observations(CONTEXT, None, "0.1.0"), [])
        v = sem.check_observations(CONTEXT, None, "0.2.0")
        self.assertEqual(codes(v), ["S-SENSE-CONTRACT-VERSION"] * 2)
        self.assertEqual(sem.check_observations(CONTEXT, None, None), [])


class ContextLifecycle(unittest.TestCase):
    def rev(self, n, state, **extra):
        d = {"context_id": "ctx-1", "revision": n, "lifecycle_state": state, "created_at": "2026-11-03T00:00:00Z"}
        d.update(extra)
        return d

    SNAP = {"ref": "snap://1", "digest": "sha256:" + "a" * 64}

    def test_first_revision_is_created(self):
        self.assertEqual(sem.check_context(self.rev(1, "CREATED")), [])
        self.assertEqual(codes(sem.check_context(self.rev(1, "ACTIVE"))), ["S-CONTEXT-INITIAL"])

    def test_created_is_only_the_first_revision(self):
        self.assertEqual(codes(sem.check_context(self.rev(2, "CREATED"))), ["S-CONTEXT-INITIAL"])

    def test_legal_transitions(self):
        legal = [("CREATED", "ACTIVE"), ("ACTIVE", "ACTIVE"), ("ACTIVE", "SNAPSHOTTED"), ("SNAPSHOTTED", "ACTIVE")]
        legal += [(s, t) for s in ("CREATED", "ACTIVE", "SNAPSHOTTED") for t in ("CLOSED", "EXPIRED")]
        for a, b in legal:
            with self.subTest(a=a, b=b):
                extra = {"snapshot_ref": self.SNAP} if b == "SNAPSHOTTED" else {}
                self.assertEqual(sem.check_context_transition(self.rev(1, a), self.rev(2, b, **extra)), [])

    def test_illegal_transitions(self):
        states = ("CREATED", "ACTIVE", "SNAPSHOTTED", "CLOSED", "EXPIRED")
        legal = {("CREATED", "ACTIVE"), ("ACTIVE", "ACTIVE"), ("ACTIVE", "SNAPSHOTTED"), ("SNAPSHOTTED", "ACTIVE")}
        legal |= {(s, t) for s in ("CREATED", "ACTIVE", "SNAPSHOTTED") for t in ("CLOSED", "EXPIRED")}
        for a in states:
            for b in states:
                if (a, b) in legal:
                    continue
                with self.subTest(a=a, b=b):
                    extra = {"snapshot_ref": self.SNAP}
                    v = sem.check_context_transition(self.rev(1, a), self.rev(2, b, **extra))
                    self.assertIn("S-CONTEXT-TRANSITION", codes(v))

    def test_revision_increases_by_exactly_one(self):
        for n in (1, 3, 5):
            with self.subTest(n=n):
                self.assertEqual(codes(sem.check_context_transition(self.rev(1, "ACTIVE"), self.rev(n, "ACTIVE"))), ["S-CONTEXT-TRANSITION"])

    def test_identity_and_created_at_are_immutable(self):
        a = self.rev(1, "ACTIVE")
        self.assertEqual(len(sem.check_context_transition(a, edit(self.rev(2, "ACTIVE"), lambda d: d.update(context_id="ctx-2")))), 1)
        self.assertEqual(len(sem.check_context_transition(a, edit(self.rev(2, "ACTIVE"), lambda d: d.update(created_at="2026-11-04T00:00:00Z")))), 1)

    def test_snapshotted_revision_needs_a_snapshot_reference_and_digest(self):
        a = self.rev(1, "ACTIVE")
        self.assertTrue(sem.check_context_transition(a, self.rev(2, "SNAPSHOTTED")))
        self.assertTrue(sem.check_context_transition(a, self.rev(2, "SNAPSHOTTED", snapshot_ref={"ref": "snap://1"})))

    def test_example_revisions_are_a_legal_chain(self):
        active = valid("context-active.json")
        snap = valid("context-snapshot-only.json")
        self.assertEqual(active["context_id"], snap["context_id"])


class RequestContextBinding(unittest.TestCase):
    REQ = valid("request-with-freshness.json")

    def ctx(self, **kw):
        c = {"context_id": self.REQ["context_ref"]["context_id"], "revision": self.REQ["context_ref"]["revision"], "lifecycle_state": "ACTIVE"}
        c.update(kw)
        return c

    def test_matching_active_context(self):
        self.assertEqual(sem.check_request_context(self.REQ, self.ctx()), [])

    def test_context_ref_must_name_the_revision(self):
        self.assertEqual(codes(sem.check_request_context(self.REQ, self.ctx(revision=self.REQ["context_ref"]["revision"] + 1))), ["S-BINDING"])
        self.assertEqual(codes(sem.check_request_context(self.REQ, self.ctx(context_id="other"))), ["S-BINDING"])

    def test_closed_and_expired_revisions_are_unusable_for_a_new_request(self):
        for state in ("CLOSED", "EXPIRED"):
            with self.subTest(state=state):
                v = sem.check_request_context(self.REQ, self.ctx(lifecycle_state=state))
                self.assertEqual(codes(v), ["S-CONTEXT-UNUSABLE"])
                self.assertIn("MIND_INPUT_INVALID", v[0].message)

    def test_request_freshness_policy_applies_to_the_context_observations(self):
        pol = self.REQ["constraints"]["freshness"]
        self.assertIn("now_ns", pol)
        stale = {"sensor_id": "imu.base", "sequence": 1, "clock": pol["clock"], "timestamp_ns": pol["now_ns"] - pol["max_age_ns"] - 1, "validity": "VALID", "usable": True, "source_contract": "0.1.0"}
        v = sem.check_request_context(self.REQ, self.ctx(observations=[stale]))
        self.assertEqual(codes(v), ["S-OBSERVATION-USABLE"])
        self.assertEqual(v[0].pointer, "/context/observations/0/usable")

    def test_result_must_name_the_request_and_context_it_answered(self):
        res = valid("result-completed.json")
        req = {"request_id": res["request_id"], "context_ref": res["context_ref"]}
        self.assertEqual(sem.check_result_for_request(req, res), [])
        self.assertEqual(codes(sem.check_result_for_request(edit(req, lambda d: d.update(request_id="other")), res)), ["S-BINDING"])
        bad = edit(req, lambda d: d["context_ref"].update(revision=99))
        self.assertEqual(codes(sem.check_result_for_request(bad, res)), ["S-BINDING"])


class Cancellation(unittest.TestCase):
    CANCELLED = valid("result-cancelled.json")
    COMPLETED = valid("result-completed.json")

    def test_cancelling_a_non_terminal_request_ends_cancelled(self):
        self.assertEqual(sem.check_cancel_outcome(None, self.CANCELLED), [])
        self.assertEqual(codes(sem.check_cancel_outcome(None, self.COMPLETED)), ["S-CANCEL"])
        self.assertEqual(codes(sem.check_cancel_outcome(None, None)), ["S-CANCEL"])

    def test_a_cancelled_example_is_valid_and_lists_what_is_missing(self):
        self.assertEqual(validator().validate("result", self.CANCELLED), [])
        self.assertTrue(self.CANCELLED["missing"])

    def test_late_cancel_never_rewrites_a_terminal_result(self):
        for name in ("result-completed.json", "result-partial.json", "result-failed-provider-unavailable.json", "result-cancelled.json"):
            prior = valid(name)
            with self.subTest(prior=name):
                self.assertEqual(sem.check_cancel_outcome(prior, edit(prior, lambda d: None)), [])
                self.assertEqual(codes(sem.check_cancel_outcome(prior, self.CANCELLED if name != "result-cancelled.json" else edit(prior, lambda d: d.update(result_id="x")))), ["S-CANCEL"])

    def test_repeated_cancel_is_idempotent(self):
        self.assertEqual(sem.check_cancel_outcome(self.CANCELLED, edit(self.CANCELLED, lambda d: None)), [])


class ToleratesMalformedInput(unittest.TestCase):
    def test_semantic_checks_do_not_raise_on_garbage(self):
        junk = [None, 1, "x", [], {}, {"proposed_skills": 5}, {"proposed_skills": [1, None, {"proposal_id": 3}]}, {"errors": [1, {"detail": []}]}, {"observations": "x"}, {"observations": [1, {"usable": True}]}]
        for j in junk:
            with self.subTest(doc=j):
                sem.check_result(j)
                sem.check_context(j, {"max_age_ns": 1, "now_ns": 1, "clock": "utc"}, "0.1.0")
                sem.check_context_transition(j, j)
                sem.check_request_context(j, j)
                sem.check_result_for_request(j, j)
                sem.check_cancel_outcome(j, j)
                validator().validate("result", j)
                validator().validate("context", j)
                validator().validate("request", j)


if __name__ == "__main__":
    unittest.main()
