"""A limited, dependency-free JSON Schema (draft 2020-12) validator.

Decision D-2 (ARCHITECTURE.md section 8.1): the validator supports only the
keywords the Mind contract schemas use and refuses every other keyword, so a
schema keyword can never be silently ignored.

This is NOT a complete JSON Schema implementation. It does not show that a
document is correct or safe, only that it satisfies the schema keywords listed
in ALLOWED_KEYWORDS. A new keyword in a contract schema needs a change here in
the same pull request (test_contract_keywords.py fails otherwise).

Properties relied on by AC-004 (deterministic validation):
  * no network access: `$ref` resolves only against schemas handed to the
    validator (by their `$id`) or JSON Pointer fragments inside them;
  * every violation is reported, sorted by (path, code, message);
  * no dependence on dict ordering, hashing or the clock.
"""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from typing import Any, Iterable

# Keywords that carry no validation behaviour (annotations / identifiers).
ANNOTATION_KEYWORDS = frozenset({"$schema", "$id", "title", "description"})

# Keywords that are implemented. Anything else in a schema is rejected.
ASSERTION_KEYWORDS = frozenset(
    {
        "$ref",
        "$defs",
        "type",
        "enum",
        "const",
        "properties",
        "required",
        "additionalProperties",
        "items",
        "minItems",
        "uniqueItems",
        "minimum",
        "minLength",
        "maxLength",
        "pattern",
        "propertyNames",
        "dependentRequired",
        "allOf",
        "anyOf",
        "not",
        "if",
        "then",
        "contains",
        "format",
    }
)

ALLOWED_KEYWORDS = ANNOTATION_KEYWORDS | ASSERTION_KEYWORDS

# `format` values that are asserted. Any other format value is rejected rather
# than treated as an annotation.
ASSERTED_FORMATS = frozenset({"date-time"})

_TYPES = frozenset({"object", "array", "string", "integer", "number", "boolean", "null"})


class SchemaError(Exception):
    """The schema itself is unusable (unknown keyword, bad $ref, ...).

    Raised, never swallowed: an unsupported schema fails closed.
    """


@dataclass(frozen=True)
class Violation:
    """One reason an instance does not satisfy a schema."""

    path: tuple  # sequence of str (property names) and int (array indexes)
    code: str  # the schema keyword (or semantic rule id) that failed
    message: str

    @property
    def pointer(self) -> str:
        return pointer_from_path(self.path)

    def sort_key(self):
        return (_path_key(self.path), self.code, self.message)

    def __str__(self) -> str:
        return f"{self.pointer or '/'}: [{self.code}] {self.message}"


def pointer_from_path(path: Iterable) -> str:
    out = []
    for seg in path:
        out.append("/" + str(seg).replace("~", "~0").replace("/", "~1"))
    return "".join(out)


def _path_key(path: tuple):
    # Integers sort numerically and before strings at the same position, so
    # /items/2 precedes /items/10 and the order is total and deterministic.
    return tuple((0, s, "") if isinstance(s, int) else (1, 0, s) for s in path)


def sort_violations(violations: Iterable[Violation]) -> list:
    return sorted(set(violations), key=lambda v: v.sort_key())


# --------------------------------------------------------------------------
# JSON value helpers
# --------------------------------------------------------------------------


def _is_integer(v: Any) -> bool:
    if isinstance(v, bool):
        return False
    if isinstance(v, int):
        return True
    return isinstance(v, float) and v.is_integer()


def _is_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _type_matches(v: Any, t: str) -> bool:
    if t == "object":
        return isinstance(v, dict)
    if t == "array":
        return isinstance(v, list)
    if t == "string":
        return isinstance(v, str)
    if t == "boolean":
        return isinstance(v, bool)
    if t == "null":
        return v is None
    if t == "integer":
        return _is_integer(v)
    if t == "number":
        return _is_number(v)
    raise SchemaError(f"unknown type {t!r}")


def json_equal(a: Any, b: Any) -> bool:
    """JSON equality: true is not 1, 1 equals 1.0, objects ignore key order."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if _is_number(a) and _is_number(b):
        return a == b
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(json_equal(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(json_equal(x, y) for x, y in zip(a, b))
    return type(a) is type(b) and a == b


# --------------------------------------------------------------------------
# Patterns and formats
# --------------------------------------------------------------------------


def _translate_pattern(pattern: str) -> str:
    """Make a Python regex behave like the ECMA-262 anchors the schemas assume.

    In Python `$` also matches before a trailing newline, so "abc\\n" would
    satisfy ^[a-z]+$. An unescaped `$` outside a character class becomes `\\Z`.
    """
    out = []
    i = 0
    in_class = False
    while i < len(pattern):
        c = pattern[i]
        if c == "\\" and i + 1 < len(pattern):
            out.append(pattern[i : i + 2])
            i += 2
            continue
        if in_class:
            if c == "]":
                in_class = False
        elif c == "[":
            in_class = True
        elif c == "$":
            out.append(r"\Z")
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


_PATTERN_CACHE: dict = {}


def _compile(pattern: str):
    rx = _PATTERN_CACHE.get(pattern)
    if rx is None:
        try:
            rx = re.compile(_translate_pattern(pattern))
        except re.error as exc:
            raise SchemaError(f"invalid pattern {pattern!r}: {exc}") from exc
        _PATTERN_CACHE[pattern] = rx
    return rx


_DATE_TIME = re.compile(
    r"([0-9]{4})-([0-9]{2})-([0-9]{2})[Tt]([0-9]{2}):([0-9]{2}):([0-9]{2})"
    r"(\.[0-9]+)?([Zz]|[+-]([0-9]{2}):([0-9]{2}))\Z"
)


def is_rfc3339_date_time(value: str) -> bool:
    """RFC 3339 `date-time` (section 5.6), asserted rather than annotated."""
    m = _DATE_TIME.match(value)
    if not m:
        return False
    year, month, day, hour, minute, second = (int(m.group(i)) for i in range(1, 7))
    try:
        datetime.date(year, month, day)
    except ValueError:
        return False
    if hour > 23 or minute > 59 or second > 60:  # 60 allows a leap second
        return False
    if m.group(9) is not None and (int(m.group(9)) > 23 or int(m.group(10)) > 59):
        return False
    return True


# --------------------------------------------------------------------------
# Schema checking (the keyword allowlist)
# --------------------------------------------------------------------------

_SUBSCHEMA_MAP_KEYWORDS = ("properties", "$defs")
_SUBSCHEMA_KEYWORDS = ("items", "additionalProperties", "propertyNames", "not", "if", "then", "contains")
_SUBSCHEMA_LIST_KEYWORDS = ("allOf", "anyOf")


def check_schema(schema: Any, _where: str = "") -> None:
    """Raise SchemaError if the schema uses anything this validator lacks.

    Walks sub-schemas by position, so a property that happens to be named like
    a keyword is not misread, and `enum` / `const` values are treated as data.
    """
    if isinstance(schema, bool):
        return
    if not isinstance(schema, dict):
        raise SchemaError(f"{_where or '#'}: a schema must be an object or boolean")
    for key in sorted(schema):
        if key not in ALLOWED_KEYWORDS:
            raise SchemaError(f"{_where or '#'}: unsupported keyword {key!r}; refusing to ignore it")
    for key in _SUBSCHEMA_MAP_KEYWORDS:
        if key in schema:
            if not isinstance(schema[key], dict):
                raise SchemaError(f"{_where}/{key}: must be an object of schemas")
            for name in sorted(schema[key]):
                check_schema(schema[key][name], f"{_where}/{key}/{name}")
    for key in _SUBSCHEMA_KEYWORDS:
        if key in schema:
            check_schema(schema[key], f"{_where}/{key}")
    for key in _SUBSCHEMA_LIST_KEYWORDS:
        if key in schema:
            if not isinstance(schema[key], list) or not schema[key]:
                raise SchemaError(f"{_where}/{key}: must be a non-empty array of schemas")
            for i, sub in enumerate(schema[key]):
                check_schema(sub, f"{_where}/{key}/{i}")
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        for t in types:
            if t not in _TYPES:
                raise SchemaError(f"{_where}/type: unknown type {t!r}")
    if "format" in schema and schema["format"] not in ASSERTED_FORMATS:
        raise SchemaError(f"{_where}/format: only {sorted(ASSERTED_FORMATS)} is asserted; {schema['format']!r} would be ignored")
    if "pattern" in schema:
        if not isinstance(schema["pattern"], str):
            raise SchemaError(f"{_where}/pattern: must be a string")
        _compile(schema["pattern"])
    if "required" in schema and not (
        isinstance(schema["required"], list) and all(isinstance(x, str) for x in schema["required"])
    ):
        raise SchemaError(f"{_where}/required: must be an array of strings")
    if "dependentRequired" in schema:
        dr = schema["dependentRequired"]
        if not isinstance(dr, dict) or not all(
            isinstance(v, list) and all(isinstance(x, str) for x in v) for v in dr.values()
        ):
            raise SchemaError(f"{_where}/dependentRequired: must map names to arrays of names")
    if "enum" in schema and not isinstance(schema["enum"], list):
        raise SchemaError(f"{_where}/enum: must be an array")
    for key in ("minItems", "minLength", "maxLength"):
        if key in schema and not (_is_integer(schema[key]) and schema[key] >= 0):
            raise SchemaError(f"{_where}/{key}: must be a non-negative integer")
    if "minimum" in schema and not _is_number(schema["minimum"]):
        raise SchemaError(f"{_where}/minimum: must be a number")
    if "uniqueItems" in schema and not isinstance(schema["uniqueItems"], bool):
        raise SchemaError(f"{_where}/uniqueItems: must be a boolean")
    if "$ref" in schema and not isinstance(schema["$ref"], str):
        raise SchemaError(f"{_where}/$ref: must be a string")


# --------------------------------------------------------------------------
# Validator
# --------------------------------------------------------------------------


class Validator:
    """Validates instances against schemas registered by their `$id`."""

    def __init__(self, schemas: Iterable[dict]):
        self._by_id: dict = {}
        for schema in schemas:
            check_schema(schema)
            sid = schema.get("$id")
            if not isinstance(sid, str) or not sid:
                raise SchemaError("every registered schema needs an $id")
            if sid in self._by_id:
                raise SchemaError(f"duplicate $id {sid}")
            self._by_id[sid] = schema
        # Resolve every $ref once, up front, so a dangling reference fails when
        # the validator is built and never while validating some instance.
        for schema in self._by_id.values():
            self._check_refs(schema, schema, "")

    # -- reference handling ------------------------------------------------

    def _resolve(self, ref: str, root: dict):
        base, _, fragment = ref.partition("#")
        if base:
            if base not in self._by_id:
                raise SchemaError(f"$ref {ref!r}: unknown schema {base!r} (no network access is attempted)")
            root = self._by_id[base]
        node: Any = root
        if fragment:
            if not fragment.startswith("/"):
                raise SchemaError(f"$ref {ref!r}: only JSON Pointer fragments are supported")
            for raw in fragment[1:].split("/"):
                seg = raw.replace("~1", "/").replace("~0", "~")
                if not isinstance(node, dict) or seg not in node:
                    raise SchemaError(f"$ref {ref!r}: pointer does not resolve")
                node = node[seg]
        return node, root

    def _check_refs(self, schema: Any, root: dict, where: str) -> None:
        if not isinstance(schema, dict):
            return
        if "$ref" in schema:
            target, target_root = self._resolve(schema["$ref"], root)
            check_schema(target)
        for key in _SUBSCHEMA_MAP_KEYWORDS:
            for name, sub in sorted(schema.get(key, {}).items()):
                self._check_refs(sub, root, f"{where}/{key}/{name}")
        for key in _SUBSCHEMA_KEYWORDS:
            if key in schema:
                self._check_refs(schema[key], root, f"{where}/{key}")
        for key in _SUBSCHEMA_LIST_KEYWORDS:
            for i, sub in enumerate(schema.get(key, [])):
                self._check_refs(sub, root, f"{where}/{key}/{i}")

    # -- public API ---------------------------------------------------------

    def validate(self, instance: Any, schema_id: str) -> list:
        """Return every violation, sorted; an empty list means the instance conforms."""
        if schema_id not in self._by_id:
            raise SchemaError(f"unknown schema {schema_id!r}")
        root = self._by_id[schema_id]
        return sort_violations(self._validate(instance, root, root, ()))

    # -- core ---------------------------------------------------------------

    def _validate(self, inst: Any, schema: Any, root: dict, path: tuple, _depth: int = 0) -> list:
        if _depth > 200:
            raise SchemaError("schema nesting or $ref cycle too deep")
        if schema is True:
            return []
        if schema is False:
            return [Violation(path, "false-schema", "no value is allowed here")]
        out: list = []
        d = _depth + 1

        if "$ref" in schema:
            target, target_root = self._resolve(schema["$ref"], root)
            out += self._validate(inst, target, target_root, path, d)

        if "type" in schema:
            types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
            if not any(_type_matches(inst, t) for t in types):
                out.append(Violation(path, "type", f"expected {' or '.join(types)}, got {_json_type(inst)}"))

        if "enum" in schema and not any(json_equal(inst, e) for e in schema["enum"]):
            out.append(Violation(path, "enum", f"{_short(inst)} is not one of {_short(schema['enum'])}"))

        if "const" in schema and not json_equal(inst, schema["const"]):
            out.append(Violation(path, "const", f"expected {_short(schema['const'])}, got {_short(inst)}"))

        if isinstance(inst, str):
            if "minLength" in schema and len(inst) < schema["minLength"]:
                out.append(Violation(path, "minLength", f"shorter than {schema['minLength']} characters"))
            if "maxLength" in schema and len(inst) > schema["maxLength"]:
                out.append(Violation(path, "maxLength", f"longer than {schema['maxLength']} characters"))
            if "pattern" in schema and not _compile(schema["pattern"]).search(inst):
                out.append(Violation(path, "pattern", f"{_short(inst)} does not match {schema['pattern']}"))
            if schema.get("format") == "date-time" and not is_rfc3339_date_time(inst):
                out.append(Violation(path, "format", f"{_short(inst)} is not an RFC 3339 date-time"))

        if _is_number(inst) and "minimum" in schema and inst < schema["minimum"]:
            out.append(Violation(path, "minimum", f"{inst} is less than {schema['minimum']}"))

        if isinstance(inst, dict):
            props = schema.get("properties", {})
            for name in schema.get("required", []):
                if name not in inst:
                    out.append(Violation(path, "required", f"missing required property {name!r}"))
            for name, deps in schema.get("dependentRequired", {}).items():
                if name in inst:
                    for dep in deps:
                        if dep not in inst:
                            out.append(Violation(path, "dependentRequired", f"{name!r} requires {dep!r}"))
            for name in inst:
                if name in props:
                    out += self._validate(inst[name], props[name], root, path + (name,), d)
                elif "additionalProperties" in schema:
                    ap = schema["additionalProperties"]
                    if ap is False:
                        out.append(Violation(path + (name,), "additionalProperties", f"unknown property {name!r}"))
                    elif ap is not True:
                        out += self._validate(inst[name], ap, root, path + (name,), d)
                if "propertyNames" in schema:
                    for v in self._validate(name, schema["propertyNames"], root, path + (name,), d):
                        out.append(Violation(v.path, "propertyNames", f"property name {name!r}: {v.message}"))

        if isinstance(inst, list):
            if "minItems" in schema and len(inst) < schema["minItems"]:
                out.append(Violation(path, "minItems", f"fewer than {schema['minItems']} items"))
            if schema.get("uniqueItems"):
                for i in range(len(inst)):
                    if any(json_equal(inst[i], inst[j]) for j in range(i)):
                        out.append(Violation(path + (i,), "uniqueItems", "duplicate of an earlier item"))
            if "items" in schema:
                for i, item in enumerate(inst):
                    out += self._validate(item, schema["items"], root, path + (i,), d)
            if "contains" in schema:
                if not any(not self._validate(item, schema["contains"], root, path + (i,), d) for i, item in enumerate(inst)):
                    out.append(Violation(path, "contains", "no item satisfies the required condition"))

        for sub in schema.get("allOf", []):
            out += self._validate(inst, sub, root, path, d)

        if "anyOf" in schema:
            if not any(not self._validate(inst, sub, root, path, d) for sub in schema["anyOf"]):
                out.append(Violation(path, "anyOf", "does not satisfy any of the allowed alternatives"))

        if "not" in schema and not self._validate(inst, schema["not"], root, path, d):
            out.append(Violation(path, "not", "satisfies a condition it must not satisfy"))

        if "if" in schema and "then" in schema:
            if not self._validate(inst, schema["if"], root, path, d):
                out += self._validate(inst, schema["then"], root, path, d)

        return out


def _json_type(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, int):
        return "integer"
    if isinstance(v, float):
        return "number"
    if isinstance(v, str):
        return "string"
    if isinstance(v, list):
        return "array"
    return "object"


def _short(v: Any, limit: int = 60) -> str:
    import json

    s = json.dumps(v, sort_keys=True, ensure_ascii=True)
    return s if len(s) <= limit else s[: limit - 3] + "..."
