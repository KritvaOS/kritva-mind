"""Keyword behaviour of the limited validator (decision D-2, ARCHITECTURE.md 8.1)."""

import unittest

import _helpers  # noqa: F401  (sets sys.path)
from kritva_mind.jsonschema_lite import (
    SchemaError,
    Validator,
    check_schema,
    is_rfc3339_date_time,
    json_equal,
)


def run(schema, instance):
    s = dict(schema)
    s.setdefault("$id", "urn:test:s")
    return Validator([s]).validate(instance, "urn:test:s")


def fails(schema, instance, code=None):
    v = run(schema, instance)
    return bool(v) if code is None else code in [x.code for x in v]


class FailClosed(unittest.TestCase):
    def test_unknown_keyword_is_rejected_not_skipped(self):
        for kw in ("patternProperties", "oneOf", "maximum", "minProperties", "else", "unevaluatedProperties", "minContains", "contentEncoding", "$dynamicRef"):
            with self.subTest(keyword=kw):
                with self.assertRaises(SchemaError):
                    Validator([{"$id": "urn:test:s", kw: 1}])

    def test_unknown_keyword_nested_in_subschema_is_rejected(self):
        with self.assertRaises(SchemaError):
            Validator([{"$id": "urn:test:s", "properties": {"a": {"items": {"oneOf": []}}}}])

    def test_property_named_like_a_keyword_is_not_misread(self):
        v = run({"properties": {"oneOf": {"type": "integer"}, "$ref": {"type": "string"}}}, {"oneOf": 1, "$ref": "x"})
        self.assertEqual(v, [])

    def test_enum_and_const_values_are_data(self):
        self.assertEqual(run({"enum": [{"oneOf": 1}], "const": {"oneOf": 1}}, {"oneOf": 1}), [])

    def test_unknown_format_is_rejected_not_ignored(self):
        with self.assertRaises(SchemaError):
            Validator([{"$id": "urn:test:s", "format": "email"}])

    def test_unknown_type_is_rejected(self):
        with self.assertRaises(SchemaError):
            Validator([{"$id": "urn:test:s", "type": "float"}])

    def test_unknown_or_dangling_ref_fails_when_the_validator_is_built(self):
        for ref in ("urn:test:missing#/$defs/X", "#/$defs/Nope", "https://example.com/schema.json"):
            with self.subTest(ref=ref):
                with self.assertRaises(SchemaError):
                    Validator([{"$id": "urn:test:s", "properties": {"a": {"$ref": ref}}}])

    def test_non_pointer_fragment_is_rejected(self):
        with self.assertRaises(SchemaError):
            Validator([{"$id": "urn:test:s", "$defs": {"x": {}}, "$ref": "#anchor"}])

    def test_schema_without_id_or_with_duplicate_id_is_rejected(self):
        with self.assertRaises(SchemaError):
            Validator([{"type": "object"}])
        with self.assertRaises(SchemaError):
            Validator([{"$id": "urn:test:s"}, {"$id": "urn:test:s"}])

    def test_bad_pattern_is_rejected(self):
        with self.assertRaises(SchemaError):
            Validator([{"$id": "urn:test:s", "pattern": "("}])

    def test_check_schema_accepts_boolean_schemas(self):
        check_schema(True)
        check_schema({"properties": {"a": False}})


class Types(unittest.TestCase):
    def test_boolean_is_not_an_integer_or_number(self):
        self.assertTrue(fails({"type": "integer"}, True))
        self.assertTrue(fails({"type": "number"}, False))

    def test_integral_float_is_an_integer(self):
        self.assertFalse(fails({"type": "integer"}, 3.0))
        self.assertTrue(fails({"type": "integer"}, 3.5))

    def test_each_type(self):
        cases = {"object": {}, "array": [], "string": "", "boolean": True, "null": None, "integer": 1, "number": 1.5}
        for t, ok in cases.items():
            for t2, other in cases.items():
                if t == "number" and t2 == "integer":
                    continue
                with self.subTest(t=t, value=t2):
                    self.assertEqual(fails({"type": t}, other), t != t2)

    def test_type_list(self):
        self.assertFalse(fails({"type": ["string", "null"]}, None))
        self.assertTrue(fails({"type": ["string", "null"]}, 1))


class Equality(unittest.TestCase):
    def test_true_is_not_one(self):
        self.assertFalse(json_equal(True, 1))
        self.assertFalse(json_equal(0, False))
        self.assertTrue(fails({"enum": [1]}, True))
        self.assertTrue(fails({"const": True}, 1))

    def test_one_equals_one_point_zero(self):
        self.assertTrue(json_equal(1, 1.0))

    def test_nested_and_key_order(self):
        self.assertTrue(json_equal({"a": [1, {"b": 2}], "c": 3}, {"c": 3, "a": [1.0, {"b": 2}]}))
        self.assertFalse(json_equal({"a": [True]}, {"a": [1]}))

    def test_unique_items_uses_json_equality(self):
        self.assertTrue(fails({"uniqueItems": True}, [1, 1.0]))
        self.assertFalse(fails({"uniqueItems": True}, [1, True]))
        self.assertFalse(fails({"uniqueItems": True}, ["a", "b"]))


class StringKeywords(unittest.TestCase):
    def test_pattern_dollar_does_not_accept_a_trailing_newline(self):
        schema = {"pattern": "^[a-z]+$"}
        self.assertFalse(fails(schema, "abc"))
        self.assertTrue(fails(schema, "abc\n"))

    def test_dollar_inside_a_character_class_is_literal(self):
        schema = {"pattern": "^[a$]+$"}
        self.assertFalse(fails(schema, "a$a"))
        self.assertTrue(fails(schema, "a$a\n"))

    def test_pattern_is_unanchored_search_like_json_schema(self):
        self.assertFalse(fails({"pattern": "b"}, "abc"))

    def test_pattern_ignores_non_strings(self):
        self.assertFalse(fails({"pattern": "^a$"}, 5))

    def test_min_and_max_length_count_code_points(self):
        self.assertFalse(fails({"minLength": 1, "maxLength": 1}, "\U0001F600"))
        self.assertTrue(fails({"minLength": 2}, "\U0001F600"))

    def test_date_time(self):
        good = ["2026-11-03T10:00:00Z", "2026-11-03T10:00:00.123+05:30", "2026-11-03t10:00:00z", "2016-12-31T23:59:60Z", "2024-02-29T00:00:00-08:00"]
        bad = [
            "2026-11-03",
            "2026-11-03 10:00:00Z",
            "2026-11-03T10:00:00",
            "2026-13-03T10:00:00Z",
            "2026-02-29T10:00:00Z",
            "2026-11-03T24:00:00Z",
            "2026-11-03T10:60:00Z",
            "2026-11-03T10:00:61Z",
            "2026-11-03T10:00:00+24:00",
            "2026-11-03T10:00:00+0530",
            "2026-11-03T10:00:00Z\n",
            "٢026-11-03T10:00:00Z",
            "2026-11-03T10:00:00.Z",
            "",
        ]
        for s in good:
            with self.subTest(good=s):
                self.assertTrue(is_rfc3339_date_time(s))
        for s in bad:
            with self.subTest(bad=s):
                self.assertFalse(is_rfc3339_date_time(s))

    def test_format_is_asserted_for_strings_only(self):
        self.assertTrue(fails({"format": "date-time"}, "yesterday"))
        self.assertFalse(fails({"format": "date-time"}, 5))


class NumberAndObjectKeywords(unittest.TestCase):
    def test_minimum_is_inclusive_and_ignores_booleans(self):
        self.assertFalse(fails({"minimum": 1}, 1))
        self.assertTrue(fails({"minimum": 1}, 0))
        self.assertFalse(fails({"minimum": 1}, True))

    def test_required_and_additional_properties(self):
        s = {"properties": {"a": {}}, "required": ["a"], "additionalProperties": False}
        self.assertFalse(fails(s, {"a": 1}))
        self.assertTrue(fails(s, {}, "required"))
        self.assertTrue(fails(s, {"a": 1, "b": 2}, "additionalProperties"))

    def test_additional_properties_schema(self):
        s = {"additionalProperties": {"type": "integer"}}
        self.assertFalse(fails(s, {"x": 1}))
        self.assertTrue(fails(s, {"x": "1"}))

    def test_property_names(self):
        s = {"propertyNames": {"pattern": "^[a-z]+$"}}
        self.assertFalse(fails(s, {"abc": 1}))
        self.assertTrue(fails(s, {"ABC": 1}, "propertyNames"))

    def test_dependent_required(self):
        s = {"dependentRequired": {"a": ["b"]}}
        self.assertFalse(fails(s, {}))
        self.assertFalse(fails(s, {"b": 1}))
        self.assertTrue(fails(s, {"a": 1}, "dependentRequired"))

    def test_keywords_ignore_instances_of_other_types(self):
        s = {"required": ["a"], "properties": {"a": {}}, "minItems": 1, "items": False}
        self.assertEqual(run(s, "text"), [])


class ArrayKeywords(unittest.TestCase):
    def test_min_items_items_and_contains(self):
        self.assertTrue(fails({"minItems": 1}, []))
        self.assertTrue(fails({"items": {"type": "integer"}}, [1, "x"]))
        c = {"contains": {"const": 1}}
        self.assertFalse(fails(c, [0, 1]))
        self.assertTrue(fails(c, [0, 2], "contains"))
        self.assertTrue(fails(c, [], "contains"))


class Combinators(unittest.TestCase):
    def test_all_of_reports_every_branch(self):
        v = run({"allOf": [{"required": ["a"]}, {"required": ["b"]}]}, {})
        self.assertEqual(len(v), 2)

    def test_any_of(self):
        s = {"anyOf": [{"required": ["a"]}, {"required": ["b"]}]}
        self.assertFalse(fails(s, {"b": 1}))
        self.assertTrue(fails(s, {}, "anyOf"))

    def test_not(self):
        self.assertTrue(fails({"not": {"required": ["a"]}}, {"a": 1}, "not"))
        self.assertFalse(fails({"not": {"required": ["a"]}}, {}))

    def test_if_then_without_else(self):
        s = {"if": {"properties": {"k": {"const": 1}}, "required": ["k"]}, "then": {"required": ["v"]}}
        self.assertFalse(fails(s, {"k": 2}))
        self.assertFalse(fails(s, {"k": 1, "v": 0}))
        self.assertTrue(fails(s, {"k": 1}, "required"))

    def test_ref_with_sibling_keywords_applies_both(self):
        s = {"$defs": {"R": {"type": "object"}}, "$ref": "#/$defs/R", "required": ["a"]}
        v = run(s, {})
        self.assertEqual([x.code for x in v], ["required"])
        self.assertTrue(fails(s, [], "type"))

    def test_ref_to_other_registered_schema_and_local_ref_stay_in_their_own_document(self):
        common = {"$id": "urn:test:common", "$defs": {"Id": {"type": "string"}, "Pair": {"$ref": "#/$defs/Id"}}}
        main = {"$id": "urn:test:main", "$defs": {"Id": {"type": "integer"}}, "properties": {"a": {"$ref": "urn:test:common#/$defs/Pair"}, "b": {"$ref": "#/$defs/Id"}}}
        v = Validator([common, main])
        self.assertEqual(v.validate({"a": "x", "b": 1}, "urn:test:main"), [])
        self.assertEqual([x.pointer for x in v.validate({"a": 1, "b": "x"}, "urn:test:main")], ["/a", "/b"])

    def test_ref_cycle_is_an_error_not_a_hang(self):
        v = Validator([{"$id": "urn:test:s", "$defs": {"A": {"$ref": "#/$defs/A"}}, "$ref": "#/$defs/A"}])
        with self.assertRaises(SchemaError):
            v.validate(1, "urn:test:s")

    def test_unknown_schema_id(self):
        with self.assertRaises(SchemaError):
            Validator([{"$id": "urn:test:s"}]).validate(1, "urn:test:other")


class Ordering(unittest.TestCase):
    def test_violations_sorted_by_path_then_code_with_numeric_indexes(self):
        s = {"properties": {"z": {"type": "string"}, "a": {"type": "string"}, "l": {"items": {"type": "string"}}}}
        inst = {"z": 1, "a": 1, "l": [0] * 11}
        v = run(s, inst)
        self.assertEqual(
            [x.pointer for x in v],
            ["/a", "/l/0", "/l/1", "/l/2", "/l/3", "/l/4", "/l/5", "/l/6", "/l/7", "/l/8", "/l/9", "/l/10", "/z"],
        )

    def test_same_path_sorted_by_code(self):
        v = run({"type": "string", "minLength": 3, "pattern": "^x"}, "")
        self.assertEqual([x.code for x in v], ["minLength", "pattern"])

    def test_pointer_escapes(self):
        v = run({"properties": {"a/b~c": {"type": "string"}}}, {"a/b~c": 1})
        self.assertEqual(v[0].pointer, "/a~1b~0c")


if __name__ == "__main__":
    unittest.main()
