"""Load the Mind contract schemas and validate documents against them.

Validation = schema keywords (jsonschema_lite) + semantic rules (semantics).
The schemas are the 0.1.0-draft contract under contract/; they are proposed,
not accepted. A valid document is not thereby correct or safe.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from . import semantics
from .jsonschema_lite import SchemaError, Validator, Violation, sort_violations

KINDS = ("request", "context", "result")

_COMMON_ID = "urn:kritva:mind:contract:common:0.1.0"
_SCHEMA_FILES = {
    "common": "mind-common.schema.json",
    "request": "mind-request.schema.json",
    "context": "mind-context.schema.json",
    "result": "mind-result.schema.json",
}


class StrictJSONError(ValueError):
    """The text is not acceptable JSON for the contract (see load_json_text)."""


def _no_duplicates(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise StrictJSONError(f"duplicate object key {k!r}")
        seen[k] = v
    return seen


def _no_constant(name):
    raise StrictJSONError(f"{name} is not valid JSON")


def load_json_text(text: str) -> Any:
    """Parse JSON, rejecting duplicate keys, NaN and Infinity.

    Python's default parser silently keeps the last duplicate key, which would
    let two readers see different documents.
    """
    try:
        return json.loads(text, object_pairs_hook=_no_duplicates, parse_constant=_no_constant)
    except json.JSONDecodeError as exc:
        raise StrictJSONError(str(exc)) from exc


def load_json_file(path) -> Any:
    return load_json_text(Path(path).read_text(encoding="utf-8"))


def default_contract_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "contract"


class ContractValidator:
    def __init__(self, contract_dir: Optional[Path] = None):
        d = Path(contract_dir) if contract_dir else default_contract_dir()
        schemas = {name: load_json_file(d / fn) for name, fn in _SCHEMA_FILES.items()}
        self._ids = {name: s["$id"] for name, s in schemas.items()}
        self._validator = Validator(schemas.values())  # fails closed on an unsupported keyword
        self.contract_version = schemas["common"]["$id"].rsplit(":", 1)[-1]

    def validate(
        self,
        kind: str,
        document: Any,
        *,
        freshness: Optional[dict] = None,
        sense_contract_version: Optional[str] = None,
    ) -> list:
        """Every violation of `document` as a `kind`, sorted; [] means none found.

        `freshness` and `sense_contract_version` are optional consumer inputs
        for the observation rules of SEMANTICS.md section 6.
        """
        if kind not in KINDS:
            raise ValueError(f"kind must be one of {KINDS}, got {kind!r}")
        found = list(self._validator.validate(document, self._ids[kind]))
        if kind == "result":
            found += semantics.check_result(document)
        elif kind == "context":
            found += semantics.check_context(document, freshness, sense_contract_version)
        # A request alone has no observation to judge; cross-document rules
        # (request with context, result with request) are in semantics.py.
        return sort_violations(found)


__all__ = ["ContractValidator", "KINDS", "SchemaError", "StrictJSONError", "Violation", "load_json_file", "load_json_text"]
