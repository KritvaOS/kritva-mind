"""Optional differential test against the third-party `jsonschema` package.

Skipped, and reported as SKIPPED, when `jsonschema` is not installed: a skip is
never a pass (ARCHITECTURE.md 8.1). The validator under test has no dependency
on it. `jsonschema` is asked to assert `date-time`; its own default is to ignore
formats, which the check below also notes.
"""

import json
import unittest

import _helpers
from _helpers import REPO, validator
from kritva_mind import load_json_file

try:  # pragma: no cover - depends on the environment
    import jsonschema
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except Exception:  # noqa: BLE001
    jsonschema = None

MANIFEST = load_json_file(REPO / "examples" / "manifest.json")


@unittest.skipIf(jsonschema is None, "SKIPPED: jsonschema (with `referencing`) is not installed; this is not a pass")
class Differential(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schemas = {n: json.loads((REPO / "contract" / f"mind-{n}.schema.json").read_text()) for n in ("common", "request", "context", "result")}
        registry = Registry().with_resources((s["$id"], Resource.from_contents(s, default_specification=DRAFT202012)) for s in schemas.values())
        checker = Draft202012Validator.FORMAT_CHECKER
        cls.third_party = {
            k: Draft202012Validator(schemas[k], registry=registry, format_checker=checker) for k in ("request", "context", "result")
        }

    def test_schema_level_verdict_agrees_on_every_example(self):
        for folder in ("valid", "invalid"):
            for name, info in MANIFEST[folder].items():
                kind = info if folder == "valid" else info["schema"]
                doc = load_json_file(REPO / "examples" / folder / name)
                with self.subTest(example=f"{folder}/{name}"):
                    theirs = not list(self.third_party[kind].iter_errors(doc))
                    # Compare schema keyword violations only: S-* semantic rules have no `jsonschema` counterpart.
                    ours = not [v for v in validator().validate(kind, doc) if not v.code.startswith("S-")]
                    self.assertEqual(ours, theirs)


if __name__ == "__main__":
    unittest.main()
