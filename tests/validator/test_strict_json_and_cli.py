"""Strict JSON loading and the command line."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import _helpers
from _helpers import REPO
from kritva_mind import StrictJSONError, load_json_text
from kritva_mind.__main__ import main


class StrictJSON(unittest.TestCase):
    def test_duplicate_keys_are_rejected(self):
        with self.assertRaises(StrictJSONError):
            load_json_text('{"a": 1, "a": 2}')
        with self.assertRaises(StrictJSONError):
            load_json_text('{"x": {"a": 1, "a": 1}}')

    def test_nan_and_infinity_are_rejected(self):
        for text in ("NaN", "Infinity", "-Infinity", '{"a": NaN}'):
            with self.subTest(text=text):
                with self.assertRaises(StrictJSONError):
                    load_json_text(text)

    def test_syntax_errors_are_strict_errors(self):
        with self.assertRaises(StrictJSONError):
            load_json_text("{")

    def test_ordinary_json_loads(self):
        self.assertEqual(load_json_text('{"a": [1, 2.5, null, true, "x"]}'), {"a": [1, 2.5, None, True, "x"]})


def run_cli(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(list(args))
    return code, out.getvalue(), err.getvalue()


class Cli(unittest.TestCase):
    def test_valid_document_exits_zero(self):
        code, out, _ = run_cli("validate", "result", str(REPO / "examples/valid/result-completed.json"))
        self.assertEqual(code, 0)
        self.assertIn("no violation found", out)

    def test_invalid_document_exits_one_and_lists_violations(self):
        code, out, _ = run_cli("validate", "result", str(REPO / "examples/invalid/result-bad-digest.json"))
        self.assertEqual(code, 1)
        self.assertIn("/provenance/output/digest", out)
        self.assertIn("INVALID", out)

    def test_unreadable_or_malformed_input_exits_two(self):
        code, _, err = run_cli("validate", "request", "/nonexistent/file.json")
        self.assertEqual(code, 2)
        self.assertIn("error:", err)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "dup.json"
            p.write_text('{"a": 1, "a": 2}')
            code, _, err = run_cli("validate", "request", str(p))
            self.assertEqual(code, 2)
            self.assertIn("duplicate", err)

    def test_pinned_sense_version_option(self):
        f = str(REPO / "examples/valid/context-with-observations.json")
        self.assertEqual(run_cli("validate", "context", f, "--sense-contract-version", "0.1.0")[0], 0)
        self.assertEqual(run_cli("validate", "context", f, "--sense-contract-version", "9.9.9")[0], 1)

    def test_a_result_with_a_decision_field_stays_rejected(self):
        # AC-007: the contract has no field that commands an actuator or tells Skill to execute.
        doc = json.loads((REPO / "examples/valid/result-completed.json").read_text())
        for field in ("authorized", "execute", "command", "actuator"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as d:
                bad = dict(doc, **{field: True})
                p = Path(d) / "r.json"
                p.write_text(json.dumps(bad))
                code, out, _ = run_cli("validate", "result", str(p))
                self.assertEqual(code, 1)
                self.assertIn("additionalProperties", out)


if __name__ == "__main__":
    unittest.main()
