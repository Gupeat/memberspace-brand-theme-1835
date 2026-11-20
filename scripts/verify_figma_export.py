
#!/usr/bin/env python3
"""Verify the Figma export snapshot against tokens.json and the import projection."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BUILD_PATH = ROOT / "scripts" / "build.py"
TOKENS_PATH = ROOT / "tokens.json"
IMPORT_PATH = ROOT / "figma" / "figma-import.tokens.json"
LIGHT_PATH = ROOT / "figma" / "Light.tokens.json"
FIGMA_VARS_PATH = ROOT / "figma" / "figma-variables.json"
EXPORT_PATH = ROOT / "evidence" / "figma-online" / "Light.tokens.json"
OUT_PATH = ROOT / "evidence" / "figma-online" / "verify.json"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_build():
    spec = importlib.util.spec_from_file_location("brand_build", BUILD_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def flatten(node, prefix=()):
    out = {}
    for key, value in node.items():
        path = prefix + (key,)
        if isinstance(value, dict) and "$value" in value:
            out[".".join(path)] = value
        elif isinstance(value, dict):
            out.update(flatten(value, path))
    return out

def close(a, b, tol=1e-4) -> bool:
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return a == b

def compare_value(name, expected, actual):
    if isinstance(expected, str):
        if expected.startswith("{") and expected.endswith("}"):
            return expected == actual
        return expected == actual
    if isinstance(expected, dict) and expected.get("colorSpace") == "srgb":
        if not isinstance(actual, dict):
            return False
        if str(actual.get("hex", "")).upper() != str(expected.get("hex", "")).upper():
            return False
        if not close(actual.get("alpha", 1), expected.get("alpha", 1)):
            return False
        got = actual.get("components")
        want = expected.get("components")
        if not isinstance(got, list) or not isinstance(want, list) or len(got) != 3 or len(want) != 3:
            return False
        return all(close(a, b) for a, b in zip(got, want))
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        return close(expected, actual)
    return expected == actual

def main() -> int:
    build = load_build()
    data = build.load_tokens()
    index = build.build_index(data)
    expected_import = build.render_figma_import(index)
    expected = flatten(expected_import)

    actual_import = json.loads(IMPORT_PATH.read_text(encoding="utf-8"))
    actual_light = json.loads(LIGHT_PATH.read_text(encoding="utf-8"))
    actual_export = json.loads(EXPORT_PATH.read_text(encoding="utf-8"))
    export = flatten(actual_export)
    figma_payload = json.loads(FIGMA_VARS_PATH.read_text(encoding="utf-8"))
    figma_variables = figma_payload["collections"][0]["variables"]
    expected_names = {p.replace(".", "/") for p in expected}
    figma_token_paths = {v["tokenPath"] for v in figma_variables}
    figma_display_names = {v["name"] for v in figma_variables}
    display_names_ok = (
        len(figma_variables) == 74
        and figma_token_paths == set(expected)
        and figma_display_names == expected_names
        and all(v["name"] == v["tokenPath"].replace(".", "/") for v in figma_variables)
    )

    import_fresh = actual_import == expected_import
    light_identical = IMPORT_PATH.read_bytes() == LIGHT_PATH.read_bytes()

    missing = sorted(set(expected) - set(export))
    extra = sorted(set(export) - set(expected))
    type_mismatches = []
    value_mismatches = []
    description_mismatches = []
    for name in sorted(set(expected) & set(export)):
        want = expected[name]
        got = export[name]
        if want.get("$type") != got.get("$type"):
            type_mismatches.append({"name": name, "expected": want.get("$type"), "actual": got.get("$type")})
        if not compare_value(name, want.get("$value"), got.get("$value")):
            value_mismatches.append({"name": name, "expected": want.get("$value"), "actual": got.get("$value")})
        if want.get("$description", "") != got.get("$description", ""):
            description_mismatches.append({"name": name, "expected": want.get("$description", ""), "actual": got.get("$description", "")})

    counts = {"color": 0, "number": 0, "string": 0}
    for name in export:
        typ = export[name].get("$type")
        if typ in counts:
            counts[typ] += 1
    expected_counts = {"color": 38, "number": 28, "string": 8}
    ok = (
        import_fresh
        and light_identical
        and not missing
        and not extra
        and not type_mismatches
        and not value_mismatches
        and not description_mismatches
        and counts == expected_counts
        and len(export) == 74
        and display_names_ok
    )
    report = {
        "ok": ok,
        "checked": len(export),
        "expected": len(expected),
        "counts": counts,
        "expected_counts": expected_counts,
        "import_fresh": import_fresh,
        "light_identical": light_identical,
        "display_names_ok": display_names_ok,
        "display_names": sorted(figma_display_names),
        "missing": missing,
        "extra": extra,
        "type_mismatches": type_mismatches,
        "value_mismatches": value_mismatches,
        "description_mismatches": description_mismatches,
        "figma_file_url": build.FIGMA_FILE_URL,
        "collection": "Theme",
        "mode": "Light",
        "hashes": {
            "tokens.json": sha256(TOKENS_PATH),
            "figma/figma-import.tokens.json": sha256(IMPORT_PATH),
            "figma/Light.tokens.json": sha256(LIGHT_PATH),
            "figma/figma-variables.json": sha256(FIGMA_VARS_PATH),
            "evidence/figma-online/Light.tokens.json": sha256(EXPORT_PATH),
            "evidence/figma-online/Theme.zip": sha256(EXPORT_PATH.parent / "Theme.zip"),
        },
    }
    OUT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("ok", "checked", "counts", "import_fresh", "light_identical", "missing", "extra")}, ensure_ascii=False))
    if not ok:
        print(json.dumps({"type_mismatches": type_mismatches, "value_mismatches": value_mismatches, "description_mismatches": description_mismatches}, ensure_ascii=False, indent=2))
        return 1
    print("OK: 74/74 canonical paths and / display names, type counts, aliases, values and descriptions match; export snapshot is fresh.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
