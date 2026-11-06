"""Every example in examples/manifest.json gives its expected outcome (D-2 safeguard, AC-001, AC-002, AC-008, AC-011).

These are synthetic examples checked by this repository's own validator. That is
a consistency check of the draft contract, not evidence that the contract is
right, accepted or safe.
"""

import unittest

import _helpers
from _helpers import REPO, validator
from kritva_mind import load_json_file

MANIFEST = load_json_file(REPO / "examples" / "manifest.json")


class ManifestExamples(unittest.TestCase):
    def test_every_valid_example_passes_its_schema_and_semantic_rules(self):
        for name, kind in MANIFEST["valid"].items():
            with self.subTest(example=name):
                doc = load_json_file(REPO / "examples" / "valid" / name)
                self.assertEqual([str(v) for v in validator().validate(kind, doc)], [])

    def test_every_invalid_example_is_rejected(self):
        for name, info in MANIFEST["invalid"].items():
            with self.subTest(example=name, reason=info["reason"]):
                doc = load_json_file(REPO / "examples" / "invalid" / name)
                self.assertTrue(validator().validate(info["schema"], doc), "expected at least one violation")

    def test_invalid_examples_fail_for_the_reason_given(self):
        # The manifest reason is prose; pin the keyword or rule that must be among the violations.
        expected = {
            "request-missing-context-ref.json": "required",
            "context-no-content-or-snapshot.json": "anyOf",
            "context-revision-zero.json": "minimum",
            "result-authorized-field.json": "additionalProperties",
            "result-failed-without-errors.json": "required",
            "result-partial-without-missing.json": "required",
            "result-completed-with-missing.json": "not",
            "result-score-without-scale.json": "dependentRequired",
            "result-bad-digest.json": "pattern",
            "result-missing-provenance.json": "required",
            "result-completed-without-output.json": "required",
            "result-partial-attempt-only-provenance.json": "required",
            "context-stale-observation-marked-usable.json": "S-OBSERVATION-USABLE",
            "context-observation-no-clock.json": "required",
            "request-freshness-now-without-clock.json": "dependentRequired",
            "result-sense-error-code-as-mind-code.json": "enum",
            "result-proposal-without-id.json": "required",
            "result-skill-id-uppercase.json": "pattern",
            "result-version-constraint-latest.json": "pattern",
            "result-version-constraint-wildcard.json": "pattern",
            "result-version-constraint-prerelease.json": "pattern",
            "result-negative-priority.json": "minimum",
            "result-input-without-digest.json": "required",
            "result-output-without-digest.json": "required",
            "result-context-snapshot-without-digest.json": "required",
            "result-completed-without-context-snapshot.json": "required",
            "result-failed-with-only-warning.json": "contains",
            "result-placement-unknown-value.json": "enum",
            "context-valid-observation-with-sense-error-code.json": "not",
            "context-sense-error-code-lowercase.json": "pattern",
            "request-id-with-space.json": "pattern",
            "result-id-too-long.json": "pattern",
            "result-proposal-id-slash.json": "pattern",
        }
        self.assertEqual(set(expected), set(MANIFEST["invalid"]), "update this table when an example is added")
        for name, code in expected.items():
            with self.subTest(example=name):
                info = MANIFEST["invalid"][name]
                doc = load_json_file(REPO / "examples" / "invalid" / name)
                got = [v.code for v in validator().validate(info["schema"], doc)]
                self.assertIn(code, got)

    def test_no_example_file_is_missing_from_the_manifest(self):
        for folder, key in (("valid", "valid"), ("invalid", "invalid")):
            on_disk = {p.name for p in (REPO / "examples" / folder).glob("*.json")}
            self.assertEqual(on_disk, set(MANIFEST[key]), f"examples/{folder} and the manifest disagree")

    def test_schema_kinds_in_the_manifest_are_known(self):
        kinds = set(MANIFEST["valid"].values()) | {i["schema"] for i in MANIFEST["invalid"].values()}
        self.assertLessEqual(kinds, {"request", "context", "result"})


if __name__ == "__main__":
    unittest.main()
