"""kritva-mind: contract validation (KOS-MIND-002).

Validates Mind request, context and result documents against the proposed
0.1.0-draft contract. It implements no reasoning provider, memory backend or
transport, and it is not hardware or safety validation.
"""

from .contract import ContractValidator, StrictJSONError, load_json_file, load_json_text
from .jsonschema_lite import SchemaError, Violation

__all__ = [
    "ContractValidator",
    "SchemaError",
    "StrictJSONError",
    "Violation",
    "load_json_file",
    "load_json_text",
]
