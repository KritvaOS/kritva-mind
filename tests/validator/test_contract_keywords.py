"""Keyword audit: a keyword in a contract schema the validator lacks must fail the build (D-2)."""

import json
import unittest

import _helpers
from _helpers import REPO
from kritva_mind.jsonschema_lite import ALLOWED_KEYWORDS, SchemaError, Validator, check_schema


def schema_files():
    return sorted((REPO / "contract").glob("*.schema.json"))


class ContractKeywords(unittest.TestCase):
    def test_there_are_four_schemas(self):
        self.assertEqual([p.name for p in schema_files()], ["mind-common.schema.json", "mind-context.schema.json", "mind-request.schema.json", "mind-result.schema.json"])

    def test_every_contract_schema_passes_the_keyword_allowlist(self):
        for p in schema_files():
            with self.subTest(schema=p.name):
                check_schema(json.loads(p.read_text(encoding="utf-8")))

    def test_the_validator_builds_from_the_contract_schemas(self):
        Validator([json.loads(p.read_text(encoding="utf-8")) for p in schema_files()])

    def test_every_schema_declares_2020_12_and_a_versioned_urn_id(self):
        for p in schema_files():
            with self.subTest(schema=p.name):
                s = json.loads(p.read_text(encoding="utf-8"))
                self.assertEqual(s["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertRegex(s["$id"], r"^urn:kritva:mind:contract:[a-z]+:[0-9]+\.[0-9]+\.[0-9]+$")

    def test_a_new_keyword_would_be_caught(self):
        s = json.loads((REPO / "contract" / "mind-request.schema.json").read_text(encoding="utf-8"))
        s["properties"]["intent"]["maxItems"] = 3  # not implemented
        with self.assertRaises(SchemaError):
            check_schema(s)

    def test_allowlist_is_the_documented_set_plus_contains(self):
        # ARCHITECTURE.md 8.1 lists the keywords at the time of decision D-2.
        documented = {"$ref", "$defs", "type", "enum", "const", "properties", "required", "additionalProperties", "items", "minItems", "uniqueItems", "minimum", "minLength", "maxLength", "pattern", "propertyNames", "dependentRequired", "allOf", "anyOf", "not", "if", "then", "format"}
        annotations = {"$schema", "$id", "title", "description"}
        self.assertEqual(ALLOWED_KEYWORDS, documented | annotations | {"contains"})


if __name__ == "__main__":
    unittest.main()
