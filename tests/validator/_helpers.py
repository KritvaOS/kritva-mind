"""Shared test helpers (tests/validator is the discovery root, so this imports as `_helpers`)."""

import copy
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from kritva_mind import ContractValidator, load_json_file  # noqa: E402

_VALIDATOR = None


def validator():
    global _VALIDATOR
    if _VALIDATOR is None:
        _VALIDATOR = ContractValidator()
    return _VALIDATOR


def example(kind_dir, name):
    return load_json_file(REPO / "examples" / kind_dir / name)


def valid(name):
    return example("valid", name)


def edit(doc, fn):
    """Deep copy `doc`, apply `fn` to the copy, return it."""
    c = copy.deepcopy(doc)
    fn(c)
    return c


def codes(violations):
    return [v.code for v in violations]
