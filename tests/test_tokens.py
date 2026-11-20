from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402

DATA = build.load_tokens()
INDEX = build.build_index(DATA)
PATHS = set(INDEX)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_token_index_has_74_valid_tokens():
    assert len(INDEX) == 74
    for path, (token, typ) in INDEX.items():
        assert typ in build.TYPE_NAMES, path
        assert token.get("$value") not in (None, "", [], {}), path


def test_tokens_use_strict_dtcg_value_shapes():
    def is_color(value):
        return (
            isinstance(value, dict)
            and value.get("colorSpace") == "srgb"
            and isinstance(value.get("components"), list)
            and len(value["components"]) == 3
            and all(isinstance(c, (int, float)) and 0 <= c <= 1 for c in value["components"])
            and (("alpha" not in value) or (isinstance(value["alpha"], (int, float)) and 0 <= value["alpha"] <= 1))
        )
    def is_dimension(value):
        return isinstance(value, dict) and set(value) == {"value", "unit"} and value["unit"] in {"px", "rem"}
    for path, (token, typ) in INDEX.items():
        value = token["$value"]
        if isinstance(value, str) and value.startswith("{"):
            value = build.resolve(value, INDEX)
        if typ == "color":
            assert is_color(value), path
        elif typ == "dimension":
            assert is_dimension(value), path
        elif typ == "shadow":
            assert set(value) == {"offsetX", "offsetY", "blur", "spread", "color"}, path
            assert is_color(value["color"]), path
            assert all(is_dimension(value[key]) for key in ("offsetX", "offsetY", "blur", "spread")), path


def test_font_scale_and_line_height_are_standard_px_dimensions():
    sizes = sorted(int(p.split(".")[-1]) for p in PATHS if p.startswith("font.size."))
    assert sizes == [24, 28, 32, 36, 40, 48]
    for path in sorted(p for p in PATHS if p.startswith("font.lineHeight.")):
        assert INDEX[path][0]["$value"]["unit"] == "px"
    for path in sorted(p for p in PATHS if p.startswith("font.size.")):
        assert INDEX[path][0]["$value"]["unit"] == "px"
    theme = read(ROOT / "theme.wxss")
    assert "--td-font-size-m: 32rpx;" in theme
    assert "--td-line-height-body-medium: 40rpx;" in theme


def test_rework_tokens_exist():
    for path in ("color.brand.disabled", "color.focus.ring", "motion.duration.moderate", "motion.easing.decelerate", "motion.easing.accelerate"):
        assert path in PATHS


def test_neutral_scale_and_semantic_colors():
    neutrals = sorted(int(p.split(".")[-1]) for p in PATHS if re.fullmatch(r"color\.neutral\.\d+", p))
    assert neutrals == [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
    for name in ("success", "warning", "error", "info"):
        assert f"color.semantic.{name}" in PATHS
        assert f"color.semantic.{name}Light" in PATHS


def test_aliases_resolve_without_cycles():
    aliases = 0
    for path, (token, _) in INDEX.items():
        value = token["$value"]
        if isinstance(value, str) and value.startswith("{"):
            assert value.endswith("}")
            build.resolve(value, INDEX)
            aliases += 1
    assert aliases >= 7


def test_all_62_body_text_pairs_meet_wcag_aa():
    assert len(build.CONTRAST_PAIRS) == 62
    ratios = []
    for label, fg_path, bg_path in build.CONTRAST_PAIRS:
        fg = build.resolve(INDEX[fg_path][0]["$value"], INDEX)
        bg = build.resolve(INDEX[bg_path][0]["$value"], INDEX)
        ratio = build.contrast(fg, bg)
        assert ratio >= 4.5, f"{label}: {ratio:.2f}"
        ratios.append(ratio)
    assert min(ratios) >= 4.5


def test_font_family_keeps_generic_family_unquoted():
    theme = read(ROOT / "theme.wxss")
    assert "sans-serif" in theme
    assert '"sans-serif"' not in theme

def test_theme_mapping_is_fresh_and_targets_real_tdesign_names():
    theme = read(ROOT / "theme.wxss")
    names = re.findall(r"^  (--td-[A-Za-z0-9-]+):", theme, re.M)
    assert len(build.THEME_MAP) == 84
    assert len(names) == 84
    assert len(set(names)) == 84
    assert theme == build.render_theme(INDEX)
    for bad in ("--td-font-line-height", "--td-spacing-", "--td-transition-", "--td-info-", "--td-font-weight-", "--td-bg-color-inverse", "--td-brand-color-hover", "--td-font-size-xxxl"):
        assert bad not in theme
    assert "rpx" in theme
    for css_var in (
        "--td-tag-success-light-color",
        "--td-tag-warning-light-color",
        "--td-tag-danger-light-color",
        "--td-font-size-body-medium",
        "--td-font-size-mark-large",
        "--td-line-height-mark-large",
        "--td-line-height-headline-small",
    ):
        assert css_var in theme, css_var
    assert "--td-font-size-xxl" not in theme


def test_miniprogram_demo_uses_the_generated_theme():
    theme = read(ROOT / "theme.wxss")
    mini = read(ROOT / "miniprogram-demo" / "theme.wxss")
    app = read(ROOT / "miniprogram-demo" / "app.wxss")
    assert mini == theme
    assert '@import "./theme.wxss"' in app


def test_browser_preview_is_same_theme_at_2x():
    demo = read(ROOT / "demo" / "theme.css")
    assert demo == build.render_demo_theme(INDEX)
    assert "rpx" not in demo.split("page, .td-theme {", 1)[1]
    assert "\n  --brand-info-color:" in demo


def test_demo_uses_only_defined_theme_variables():
    theme = read(ROOT / "demo" / "theme.css")
    css = read(ROOT / "demo" / "demo.css")
    defined = set(re.findall(r"^  (--(?:td|brand)-[A-Za-z0-9-]+):", theme, re.M))
    used = set(re.findall(r"var\((--(?:td|brand)-[A-Za-z0-9-]+)", css))
    assert used
    assert used <= defined, sorted(used - defined)


def test_figma_variables_are_exactly_1_to_1():
    payload = json.loads(read(ROOT / "figma" / "figma-variables.json"))
    variables = payload["collections"][0]["variables"]
    assert len(variables) == 74
    assert {v["tokenPath"] for v in variables} == PATHS
    assert {v["name"] for v in variables} == {p.replace(".", "/") for p in PATHS}
    for variable in variables:
        assert variable["name"] == variable["tokenPath"].replace(".", "/")
    assert payload["tokensHash"] == hashlib.sha256((ROOT / "tokens.json").read_bytes()).hexdigest()


def test_figma_plugin_and_doc_cover_every_token():
    plugin = read(ROOT / "figma" / "create-variables.js")
    doc = read(ROOT / "docs" / "FIGMA-VARIABLES.md")
    manifest = json.loads(read(ROOT / "figma" / "manifest.json"))
    assert manifest["main"] == "create-variables.js"
    assert "figma" in manifest["editorType"]
    assert "getLocalVariableCollections" in plugin
    assert "variableCollectionId" in plugin
    assert ".remove()" not in plugin
    assert "left untouched" in plugin
    for path in PATHS:
        slash = path.replace(".", "/")
        assert slash in plugin
        assert f"| {path} | {slash} |" in doc


def test_figma_import_file_is_nested_dtcg_and_matches_tokens():
    text = read(ROOT / "figma" / "figma-import.tokens.json")
    payload = json.loads(text)
    assert payload == build.render_figma_import(INDEX)
    import_paths = {p for p, _, _ in build.walk(payload)}
    assert import_paths == PATHS
    assert json.loads(read(ROOT / "figma" / "Light.tokens.json")) == payload
    assert payload["color"]["text"]["primary"]["$value"] == "{color.neutral.900}"
    assert "（rpx" not in text
    assert "（24rpx = 12px）" in text
    assert "（200ms）" in text


def test_contrast_doc_matches_generated_pairs():
    doc = read(ROOT / "docs" / "CONTRAST.md")
    rows = [line for line in doc.splitlines() if line.startswith("| ") and ":1" in line]
    assert len(rows) == 62
    assert len(rows) == len(build.CONTRAST_PAIRS)
    assert "FAIL" not in doc
    assert "4.66:1" in doc


def test_validation_script_reports_8_of_8_pass():
    env = {"PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py")],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RESULT: PASS (8/8 checks)" in proc.stdout
    payload = json.loads(read(ROOT / "artifacts" / "validation.json"))
    assert payload["ok"] is True
    assert len(payload["checks"]) == 8
    assert payload["failures"] == []
