#!/usr/bin/env python3
"""Validate the design-token package: DTCG shape, theme mapping, contrast, Figma 1:1, demo references."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402

FAILURES: list[str] = []
CHECKS: list[dict] = []


def check(name: str, fn) -> None:
    try:
        detail = fn()
        CHECKS.append({"name": name, "ok": True, "detail": detail})
    except Exception as exc:  # noqa: BLE001
        CHECKS.append({"name": name, "ok": False, "detail": f"{type(exc).__name__}: {exc}"})
        FAILURES.append(f"{name}: {exc}")


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def tdesign_wxss_texts() -> list[str]:
    """Read TDesign 1.18.0 wxss from the vendored tarball, not a generated node_modules tree."""
    archive = ROOT / "vendor" / "tdesign-miniprogram-1.18.0.tgz"
    if not archive.exists():
        raise AssertionError(f"missing vendored TDesign package: {archive.relative_to(ROOT)}")
    texts: list[str] = []
    with tarfile.open(archive, "r:gz") as bundle:
        for member in bundle.getmembers():
            if member.isfile() and member.name.endswith(".wxss"):
                handle = bundle.extractfile(member)
                if handle is not None:
                    texts.append(handle.read().decode("utf-8"))
    if not texts:
        raise AssertionError("vendored TDesign package contains no wxss files")
    return texts


TOKENS = build.load_tokens()
INDEX = build.build_index(TOKENS)
PATHS = set(INDEX)

REQUIRED_CATEGORIES = {
    "color.brand.primary": "color",
    "color.accent.primary": "color",
    "color.neutral.50": "color",
    "color.neutral.900": "color",
    "color.semantic.success": "color",
    "color.semantic.warning": "color",
    "color.semantic.error": "color",
    "color.semantic.info": "color",
    "color.brand.disabled": "color",
    "color.brand.light": "color",
    "color.focus.ring": "color",
    "font.size.24": "dimension",
    "font.size.28": "dimension",
    "font.size.32": "dimension",
    "font.size.36": "dimension",
    "font.size.40": "dimension",
    "font.size.48": "dimension",
    "font.lineHeight.24": "dimension",
    "font.weight.regular": "fontWeight",
    "radius.8": "dimension",
    "radius.16": "dimension",
    "radius.24": "dimension",
    "radius.full": "dimension",
    "space.16": "dimension",
    "space.64": "dimension",
    "shadow.sm": "shadow",
    "shadow.md": "shadow",
    "shadow.lg": "shadow",
    "motion.duration.base": "duration",
    "motion.duration.moderate": "duration",
    "motion.easing.standard": "cubicBezier",
    "motion.easing.decelerate": "cubicBezier",
    "motion.easing.accelerate": "cubicBezier",
}



def _number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_color(value) -> bool:
    if not isinstance(value, dict):
        return False
    if set(value) - {"colorSpace", "components", "alpha", "hex"}:
        return False
    if value.get("colorSpace") != "srgb":
        return False
    components = value.get("components")
    if not isinstance(components, list) or len(components) != 3:
        return False
    if not all(_number(c) and 0 <= c <= 1 for c in components):
        return False
    if "alpha" in value and not (_number(value["alpha"]) and 0 <= value["alpha"] <= 1):
        return False
    if "hex" in value and not re.fullmatch(r"#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?", str(value["hex"])):
        return False
    return True


def _is_dimension(value) -> bool:
    return (
        isinstance(value, dict)
        and set(value) == {"value", "unit"}
        and _number(value["value"])
        and value["value"] >= 0
        and value["unit"] in {"px", "rem"}
    )


def validate_dtcg() -> str:
    for path, (token, typ) in INDEX.items():
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9]*(\.[A-Za-z0-9][A-Za-z0-9]*)+", path):
            raise AssertionError(f"invalid token path: {path}")
        if typ not in build.TYPE_NAMES:
            raise AssertionError(f"invalid $type at {path}: {typ!r}")
        value = token.get("$value")
        if value in (None, "", [], {}):
            raise AssertionError(f"empty $value at {path}")
        if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            value = build.resolve(value, INDEX)
        if typ == "color":
            if not _is_color(value):
                raise AssertionError(f"invalid DTCG color at {path}: {value!r}")
        elif typ == "dimension":
            if not _is_dimension(value):
                raise AssertionError(f"invalid DTCG dimension at {path}: {value!r}")
        elif typ == "shadow":
            if not isinstance(value, dict) or set(value) != {"offsetX", "offsetY", "blur", "spread", "color"}:
                raise AssertionError(f"invalid shadow at {path}: {value!r}")
            if not _is_color(value["color"]):
                raise AssertionError(f"invalid DTCG shadow color at {path}: {value['color']!r}")
            for key in ("offsetX", "offsetY", "blur", "spread"):
                if not _is_dimension(value[key]):
                    raise AssertionError(f"invalid DTCG shadow dimension at {path}.{key}: {value[key]!r}")
        elif typ == "duration":
            if not isinstance(value, dict) or set(value) != {"value", "unit"} or value["unit"] not in {"ms", "s"} or not _number(value["value"]):
                raise AssertionError(f"invalid duration at {path}: {value!r}")
        elif typ == "cubicBezier":
            if not isinstance(value, list) or len(value) != 4 or not all(_number(n) and 0 <= n <= 1 for n in value):
                raise AssertionError(f"invalid cubicBezier at {path}: {value!r}")
        elif typ == "fontWeight":
            if not isinstance(value, int) or not 1 <= value <= 1000:
                raise AssertionError(f"invalid fontWeight at {path}: {value!r}")
        elif typ == "fontFamily":
            if isinstance(value, list):
                if not value or not all(isinstance(v, str) and v for v in value):
                    raise AssertionError(f"invalid fontFamily at {path}: {value!r}")
            elif not isinstance(value, str) or not value:
                raise AssertionError(f"invalid fontFamily at {path}: {value!r}")
        elif typ == "number":
            if not _number(value):
                raise AssertionError(f"invalid number at {path}: {value!r}")
        elif typ == "string":
            if not isinstance(value, str):
                raise AssertionError(f"invalid string at {path}: {value!r}")
    return f"{len(INDEX)} tokens; strict DTCG value types valid (color objects, px dimensions, composite shadows)"


def validate_categories() -> str:
    if len(INDEX) != 74:
        raise AssertionError(f"expected 74 tokens, got {len(INDEX)}")
    for path, typ in REQUIRED_CATEGORIES.items():
        if path not in INDEX:
            raise AssertionError(f"missing required token: {path}")
        if INDEX[path][1] != typ:
            raise AssertionError(f"type mismatch at {path}: {INDEX[path][1]} != {typ}")
    sizes = sorted(int(p.split(".")[-1]) for p, (_, t) in INDEX.items() if p.startswith("font.size."))
    if sizes != [24, 28, 32, 36, 40, 48]:
        raise AssertionError(f"font size scale must be 24/28/32/36/40/48, got {sizes}")
    neutrals = sorted(int(p.split(".")[-1]) for p in PATHS if re.fullmatch(r"color\.neutral\.\d+", p))
    if neutrals != [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]:
        raise AssertionError(f"neutral scale incomplete: {neutrals}")
    for name in ("success", "warning", "error", "info"):
        for suffix in ("", "Light"):
            if f"color.semantic.{name}{suffix}" not in PATHS:
                raise AssertionError(f"missing semantic token: color.semantic.{name}{suffix}")
    return f"{len(REQUIRED_CATEGORIES)} required tokens; 6 sizes; 10 neutrals; 4 semantics"


def validate_aliases() -> str:
    aliases = 0
    for path, (token, _) in INDEX.items():
        value = token.get("$value")
        if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            try:
                build.resolve(value, INDEX)
            except SystemExit as exc:
                raise AssertionError(f"alias at {path} is invalid: {exc}") from exc
            aliases += 1
    return f"{aliases} aliases resolve without cycles"


def validate_contrast() -> str:
    pairs = build.CONTRAST_PAIRS
    if len(pairs) < 57:
        raise AssertionError(f"expected at least 57 body-text pairs, got {len(pairs)}")
    worst = None
    for label, fg_path, bg_path in pairs:
        fg = build.resolve(INDEX[fg_path][0]["$value"], INDEX)
        bg = build.resolve(INDEX[bg_path][0]["$value"], INDEX)
        ratio = build.contrast(fg, bg)
        if ratio < 4.5:
            raise AssertionError(f"contrast below 4.5:1: {label} {fg} on {bg} = {ratio:.2f}")
        if worst is None or ratio < worst[1]:
            worst = (label, ratio)
    return f"{len(pairs)} pairs, minimum {worst[0]} {worst[1]:.2f}:1"


def validate_theme() -> str:
    mapped = [css_var for css_var, _ in build.THEME_MAP]
    if len(mapped) != len(set(mapped)):
        raise AssertionError("THEME_MAP contains duplicate variables")
    if not all(css_var.startswith("--td-") for css_var in mapped):
        raise AssertionError("THEME_MAP contains a non-TDesign variable")
    theme = read(ROOT / "theme.wxss")
    if theme != build.render_theme(INDEX):
        raise AssertionError("theme.wxss is stale; run python scripts/build.py")
    names = re.findall(r"^  (--td-[A-Za-z0-9-]+):", theme, re.M)
    if len(names) != len(mapped) or set(names) != set(mapped):
        raise AssertionError(f"theme variable count/set mismatch: {len(names)} vs {len(mapped)}")
    if "rpx" not in theme:
        raise AssertionError("theme.wxss should use rpx")
    for bad in (
        "--td-brand-color-hover", "--td-font-line-height", "--td-spacing-",
        "--td-transition-", "--td-info-", "--td-font-weight-",
        "--td-bg-color-inverse", "--td-font-size-xxxl",
    ):
        if bad in theme:
            raise AssertionError(f"theme.wxss contains non-TDesign variable {bad!r}")

    consumed = set()
    for wxss in tdesign_wxss_texts():
        consumed.update(re.findall(r"var\((--td-[A-Za-z0-9-]+)", wxss))
    directly_consumed = sorted(set(mapped) & consumed)
    compatibility_only = sorted(set(mapped) - consumed)
    if len(directly_consumed) < 75:
        raise AssertionError(f"only {len(directly_consumed)} mapped variables are directly consumed by TDesign")
    if len(compatibility_only) > 8:
        raise AssertionError(f"too many compatibility-only variables: {compatibility_only}")

    mini_theme = read(ROOT / "miniprogram-demo" / "theme.wxss")
    if mini_theme != theme:
        raise AssertionError("miniprogram-demo/theme.wxss is stale; run python scripts/build.py")
    app_wxss = read(ROOT / "miniprogram-demo" / "app.wxss")
    if '@import "./theme.wxss"' not in app_wxss:
        raise AssertionError("miniprogram-demo/app.wxss must import ./theme.wxss")
    demo = read(ROOT / "demo" / "theme.css")
    if demo != build.render_demo_theme(INDEX):
        raise AssertionError("demo/theme.css is stale; run python scripts/build.py")
    demo_names = re.findall(r"^  (--(?:td|brand)-[A-Za-z0-9-]+):", demo, re.M)
    if len(demo_names) != len(mapped) + len(build.DEMO_EXTRA_MAP) or len(set(demo_names)) != len(demo_names):
        raise AssertionError(f"demo theme variable count/duplication mismatch: {len(demo_names)}")
    for css_var, _ in build.DEMO_EXTRA_MAP:
        if css_var not in demo_names:
            raise AssertionError(f"demo extension variable missing: {css_var}")
    return (
        f"{len(mapped)} mapped variables; {len(directly_consumed)} directly consumed by TDesign 1.18.0; "
        f"{len(compatibility_only)} compatibility-only; miniprogram-demo/theme.wxss matches; "
        f"{len(build.DEMO_EXTRA_MAP)} preview extensions; browser preview is 2x rpx->px"
    )



def validate_figma() -> str:
    payload = json.loads(read(ROOT / "figma" / "figma-variables.json"))
    variables = payload["collections"][0]["variables"]
    names = [v["name"] for v in variables]
    token_paths = [v["tokenPath"] for v in variables]
    expected_display = {path.replace(".", "/") for path in PATHS}
    if len(names) != 74 or len(token_paths) != 74:
        raise AssertionError(f"Figma variable count must be 74, got names={len(names)} tokenPaths={len(token_paths)}")
    if set(token_paths) != PATHS:
        missing = sorted(PATHS - set(token_paths))
        extra = sorted(set(token_paths) - PATHS)
        raise AssertionError(f"Figma canonical token paths not 1:1; missing={missing} extra={extra}")
    if set(names) != expected_display:
        missing = sorted(expected_display - set(names))
        extra = sorted(set(names) - expected_display)
        raise AssertionError(f"Figma slash display names not 1:1; missing={missing} extra={extra}")
    for variable in variables:
        if variable["name"] != variable["tokenPath"].replace(".", "/"):
            raise AssertionError(f"Figma display name/tokenPath mismatch: {variable!r}")
    if payload["tokensHash"] != hashlib.sha256((ROOT / "tokens.json").read_bytes()).hexdigest():
        raise AssertionError("figma-variables tokensHash is stale")
    doc = read(ROOT / "docs" / "FIGMA-VARIABLES.md")
    for path in PATHS:
        slash = path.replace(".", "/")
        if f"| {path} | {slash} |" not in doc:
            raise AssertionError(f"Figma mapping doc missing row: {path} -> {slash}")
    plugin = read(ROOT / "figma" / "create-variables.js")
    for path in PATHS:
        slash = path.replace(".", "/")
        if slash not in plugin:
            raise AssertionError(f"Figma plugin script missing slash variable: {slash}")
    import_path = ROOT / "figma" / "figma-import.tokens.json"
    import_text = read(import_path)
    expected_import = json.dumps(build.render_figma_import(INDEX), ensure_ascii=False, indent=2) + "\n"
    if import_text != expected_import:
        raise AssertionError("figma-import.tokens.json is stale; run python scripts/build.py")
    if read(ROOT / "figma" / "Light.tokens.json") != expected_import:
        raise AssertionError("figma/Light.tokens.json must be identical to figma-import.tokens.json")
    imported = json.loads(import_text)
    imported_paths = {p for p, _, _ in build.walk(imported)}
    if imported_paths != PATHS:
        missing = sorted(PATHS - imported_paths)
        extra = sorted(imported_paths - PATHS)
        raise AssertionError(f"Figma DTCG import names not 1:1; missing={missing} extra={extra}")
    expected_types = {"color": 0, "number": 0, "string": 0}
    for _, typ in INDEX.values():
        expected_types[build.figma_import_type(typ)] += 1
    actual_types = {kind: 0 for kind in expected_types}
    for _, _, typ in build.walk(imported):
        actual_types[typ] = actual_types.get(typ, 0) + 1
    if actual_types != expected_types:
        raise AssertionError(f"Figma import type counts {actual_types} != {expected_types}")
    if imported["color"]["text"]["primary"]["$value"] != "{color.neutral.900}":
        raise AssertionError("Figma import aliases must be preserved as {path} references")
    if "（rpx" in import_text:
        raise AssertionError("Figma import description contains a truncated rpx suffix")
    return (
        f"{len(variables)} Figma variables with / display names; {len(imported_paths)} DTCG import variables; "
        "canonical tokenPath values exactly equal tokens.json dot paths"
    )


def validate_demo() -> str:
    html = read(ROOT / "demo" / "index.html")
    css = read(ROOT / "demo" / "demo.css")
    for needle in (
        '<link rel="stylesheet" href="theme.css"',
        '<link rel="stylesheet" href="demo.css"',
        'data-accent="button"',
        'data-accent="tag"',
        "会员空间平台",
    ):
        if needle not in html:
            raise AssertionError(f"demo/index.html missing {needle!r}")
    theme = read(ROOT / "demo" / "theme.css")
    defined = set(re.findall(r"^  (--(?:td|brand)-[A-Za-z0-9-]+):", theme, re.M))
    used = set(re.findall(r"var\((--(?:td|brand)-[A-Za-z0-9-]+)", css))
    missing = sorted(used - defined)
    if missing:
        raise AssertionError(f"demo.css uses undefined theme variables: {missing}")
    return f"{len(used)} theme variables used by demo, all defined"


def validate_contrast_doc() -> str:
    doc = read(ROOT / "docs" / "CONTRAST.md")
    rows = [line for line in doc.splitlines() if line.startswith("| ") and ":1" in line]
    if len(rows) != len(build.CONTRAST_PAIRS):
        raise AssertionError(f"CONTRAST.md rows {len(rows)} != {len(build.CONTRAST_PAIRS)}")
    if "FAIL" in doc:
        raise AssertionError("CONTRAST.md contains FAIL")
    return f"{len(rows)} documented pairs, no FAIL"


for _name, _fn in [
    ("DTCG structure and value types", validate_dtcg),
    ("required token categories and scales", validate_categories),
    ("alias resolution", validate_aliases),
    ("WCAG contrast >= 4.5:1", validate_contrast),
    ("theme.wxss and browser preview freshness", validate_theme),
    ("Figma variables 1:1", validate_figma),
    ("demo references and variables", validate_demo),
    ("contrast documentation", validate_contrast_doc),
]:
    check(_name, _fn)

log_lines = ["ClawHunt #1835 token package validation", ""]
for item in CHECKS:
    status = "PASS" if item["ok"] else "FAIL"
    log_lines.append(f"[{status}] {item['name']}: {item['detail']}")
result = "PASS" if not FAILURES else "FAIL"
log_lines += ["", f"RESULT: {result} ({len(CHECKS) - len(FAILURES)}/{len(CHECKS)} checks)"]
log = "\n".join(log_lines) + "\n"
(ROOT / "artifacts").mkdir(exist_ok=True)
(ROOT / "artifacts" / "validation.log").write_text(log, encoding="utf-8")
(ROOT / "artifacts" / "validation.json").write_text(json.dumps({
    "ok": not FAILURES,
    "checks": CHECKS,
    "failures": FAILURES,
    "tokens": len(PATHS),
    "themeVariables": len(build.THEME_MAP),
    "contrastPairs": len(build.CONTRAST_PAIRS),
    "tokensHash": hashlib.sha256((ROOT / "tokens.json").read_bytes()).hexdigest(),
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(log, end="")
sys.exit(0 if not FAILURES else 1)