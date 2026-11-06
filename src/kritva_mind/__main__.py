"""Command line: python3 -m kritva_mind validate <request|context|result> FILE

Exit status: 0 no violation found, 1 violations found, 2 unusable input
(unreadable file, bad JSON, unsupported schema). Output order is deterministic.
"""

from __future__ import annotations

import argparse
import sys

from .contract import KINDS, ContractValidator, StrictJSONError, load_json_file
from .jsonschema_lite import SchemaError


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="kritva_mind", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate", help="validate one JSON document against the draft contract")
    v.add_argument("kind", choices=KINDS)
    v.add_argument("file")
    v.add_argument("--sense-contract-version", help="reject observations that follow another Sense contract version")
    args = parser.parse_args(argv)

    try:
        validator = ContractValidator()
        document = load_json_file(args.file)
    except (OSError, StrictJSONError, SchemaError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    violations = validator.validate(args.kind, document, sense_contract_version=args.sense_contract_version)
    for violation in violations:
        print(violation)
    print(f"{args.file}: {'INVALID' if violations else 'no violation found'} as {args.kind} (contract {validator.contract_version}-draft)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
