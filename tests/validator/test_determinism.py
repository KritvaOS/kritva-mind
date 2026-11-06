"""AC-004: the same input gives the same validation outcome."""

import copy
import json
import random
import subprocess
import sys
import unittest

import _helpers
from _helpers import REPO, validator
from kritva_mind import load_json_file

MANIFEST = load_json_file(REPO / "examples" / "manifest.json")


def reorder(value, rng):
    """Same JSON value with every object's keys in a shuffled insertion order."""
    if isinstance(value, dict):
        keys = list(value)
        rng.shuffle(keys)
        return {k: reorder(value[k], rng) for k in keys}
    if isinstance(value, list):
        return [reorder(v, rng) for v in value]
    return value


def cases():
    for name, kind in MANIFEST["valid"].items():
        yield name, kind, load_json_file(REPO / "examples" / "valid" / name)
    for name, info in MANIFEST["invalid"].items():
        yield name, info["schema"], load_json_file(REPO / "examples" / "invalid" / name)


class Determinism(unittest.TestCase):
    def test_repeated_runs_are_identical(self):
        for name, kind, doc in cases():
            with self.subTest(example=name):
                first = [str(v) for v in validator().validate(kind, doc)]
                for _ in range(3):
                    self.assertEqual([str(v) for v in validator().validate(kind, copy.deepcopy(doc))], first)

    def test_key_order_does_not_change_the_outcome(self):
        rng = random.Random(20261103)
        for name, kind, doc in cases():
            with self.subTest(example=name):
                base = [str(v) for v in validator().validate(kind, doc)]
                for _ in range(5):
                    self.assertEqual([str(v) for v in validator().validate(kind, reorder(doc, rng))], base)

    def test_fresh_validators_agree(self):
        from kritva_mind import ContractValidator

        a, b = ContractValidator(), ContractValidator()
        for name, kind, doc in cases():
            with self.subTest(example=name):
                self.assertEqual([str(v) for v in a.validate(kind, doc)], [str(v) for v in b.validate(kind, doc)])

    def test_violations_are_sorted_and_unique(self):
        for name, kind, doc in cases():
            with self.subTest(example=name):
                v = validator().validate(kind, doc)
                self.assertEqual(v, sorted(v, key=lambda x: x.sort_key()))
                self.assertEqual(len(v), len(set(v)))

    def test_output_is_identical_across_hash_seeds(self):
        code = (
            "import sys; sys.path.insert(0, %r)\n"
            "from kritva_mind import ContractValidator, load_json_file\n"
            "cv = ContractValidator()\n"
            "for f in sorted(%r):\n"
            "    kind = f.split('/')[-1].split('-')[0]\n"
            "    print(f, [str(v) for v in cv.validate(kind, load_json_file(f))])\n"
        ) % (str(REPO / "src"), [str(p) for p in (REPO / "examples" / "invalid").glob("*.json")])
        outs = set()
        for seed in ("0", "1", "12345"):
            r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, env={"PYTHONHASHSEED": seed}, check=True)
            outs.add(r.stdout)
        self.assertEqual(len(outs), 1)
        self.assertIn("result-bad-digest.json", next(iter(outs)))  # the comparison covered real output


if __name__ == "__main__":
    unittest.main()
