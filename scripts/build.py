#!/usr/bin/env python3
"""Generate theme.wxss, Figma variables, contrast table and mapping table from tokens.json."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS_PATH = ROOT / "tokens.json"
THEME_PATH = ROOT / "theme.wxss"
DEMO_CSS_PATH = ROOT / "demo" / "theme.css"
FIGMA_JSON_PATH = ROOT / "figma" / "figma-variables.json"
FIGMA_PLUGIN_PATH = ROOT / "figma" / "create-variables.js"
CONTRAST_PATH = ROOT / "docs" / "CONTRAST.md"
FIGMA_MANIFEST_PATH = ROOT / "figma" / "manifest.json"
FIGMA_DOC_PATH = ROOT / "docs" / "FIGMA-VARIABLES.md"
FIGMA_IMPORT_PATH = ROOT / "figma" / "figma-import.tokens.json"
FIGMA_LIGHT_IMPORT_PATH = ROOT / "figma" / "Light.tokens.json"
FIGMA_FILE_URL = "https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1"

TYPE_NAMES = {
    "color", "dimension", "fontFamily", "fontWeight", "number",
    "shadow", "duration", "cubicBezier", "string",
}


def load_tokens(path: Path = TOKENS_PATH) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("tokens.json must be an object")
    return data


def walk(node: dict, inherited_type: str | None = None, prefix: tuple[str, ...] = ()):
    node_type = node.get("$type", inherited_type)
    for key, value in node.items():
        if key.startswith("$"):
            continue
        path = prefix + (key,)
        if isinstance(value, dict) and "$value" in value:
            yield ".".join(path), value, value.get("$type", node_type)
        elif isinstance(value, dict):
            yield from walk(value, node_type, path)
        else:
            raise SystemExit(f"invalid group at {'.'.join(path)}: expected object or token")


def build_index(data: dict):
    return {path: (token, typ) for path, token, typ in walk(data)}


def resolve(value, index, seen=()):
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        ref = value[1:-1]
        if ref in seen:
            raise SystemExit(f"alias cycle: {' -> '.join(seen + (ref,))}")
        if ref not in index:
            raise SystemExit(f"alias target not found: {ref}")
        return resolve(index[ref][0]["$value"], index, seen + (ref,))
    return value


def dim(value) -> str:
    if not isinstance(value, dict) or set(value) != {"value", "unit"}:
        raise SystemExit(f"invalid dimension: {value!r}")
    return f"{value['value']}{value['unit']}"


def color_css(value: str) -> str:
    value = value.strip()
    if len(value) == 9:
        r, g, b = value[1:3], value[3:5], value[5:7]
        a = int(value[7:9], 16) / 255
        return f"rgba({int(r,16)},{int(g,16)},{int(b,16)},{a:.3f})"
    return value.upper()


def css_value(path: str, token: dict, typ: str, index: dict) -> str:
    value = resolve(token["$value"], index)
    if typ == "color":
        return color_css(value)
    if typ == "dimension":
        return dim(value)
    if typ == "fontFamily":
        generic = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-sans-serif", "ui-serif"}
        if isinstance(value, list):
            return ", ".join(v if v in generic else f'"{v}"' for v in value)
        return value if value in generic else f'"{value}"'
    if typ == "fontWeight":
        return str(value)
    if typ == "shadow":
        return f"{dim(value['offsetX'])} {dim(value['offsetY'])} {dim(value['blur'])} {dim(value['spread'])} {color_css(value['color'])}"
    if typ == "duration":
        return f"{value['value']}{value['unit']}"
    if typ == "cubicBezier":
        return "cubic-bezier(" + ", ".join(str(n) for n in value) + ")"
    if typ == "number":
        return str(value)
    if typ == "string":
        return str(value)
    raise SystemExit(f"unsupported type {typ!r} at {path}")


def esc_js(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def figma_type(typ: str) -> str:
    if typ == "color":
        return "COLOR"
    if typ in {"dimension", "fontWeight", "duration", "number"}:
        return "FLOAT"
    return "STRING"


def figma_value(path: str, token: dict, typ: str, index: dict):
    value = resolve(token["$value"], index)
    if typ == "color":
        return value.upper()
    if typ == "dimension":
        number = value["value"]
        unit = value["unit"]
        if unit == "rpx":
            return round(number / 2, 2)
        if unit == "px":
            return number
        if unit == "rem":
            return round(number * 16, 2)
    if typ == "fontWeight":
        return value
    if typ == "duration":
        return value["value"]
    if typ == "cubicBezier":
        return "cubic-bezier(" + ", ".join(str(n) for n in value) + ")"
    if typ == "fontFamily":
        return ", ".join(value) if isinstance(value, list) else str(value)
    if typ == "shadow":
        return css_value(path, token, typ, index)
    return str(value)


def figma_import_type(typ: str) -> str:
    if typ == "color":
        return "color"
    if typ in {"dimension", "fontWeight", "duration", "number"}:
        return "number"
    return "string"


def px_number(value: dict) -> float:
    number = value["value"]
    unit = value["unit"]
    if unit == "rpx":
        return round(number / 2, 4)
    if unit == "rem":
        return round(number * 16, 4)
    return number


def ms_number(value: dict) -> float:
    return value["value"] * 1000 if value["unit"] == "s" else value["value"]


def figma_import_value(path: str, token: dict, typ: str, index: dict):
    raw = token["$value"]
    if isinstance(raw, str) and raw.startswith("{") and raw.endswith("}"):
        return raw  # keep DTCG alias; Figma imports it as a variable reference
    value = resolve(raw, index)
    if typ == "color":
        h = value.lstrip("#")
        if len(h) not in (6, 8):
            raise SystemExit(f"invalid color at {path}: {value!r}")
        alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        components = [round(int(h[i:i + 2], 16) / 255, 6) for i in (0, 2, 4)]
        return {"colorSpace": "srgb", "components": components, "alpha": alpha, "hex": value.upper()}
    if typ == "dimension":
        return px_number(value)
    if typ == "fontWeight":
        return int(value)
    if typ == "duration":
        return round(ms_number(value), 4)
    if typ == "cubicBezier":
        return "cubic-bezier(" + ", ".join(str(n) for n in value) + ")"
    if typ == "fontFamily":
        return ", ".join(value) if isinstance(value, list) else str(value)
    if typ == "shadow":
        parts = [f"{px_number(value[key]):g}px" for key in ("offsetX", "offsetY", "blur", "spread")]
        return " ".join(parts + [color_css(value["color"])])
    return str(value)


def figma_import_description(token: dict, typ: str, index: dict) -> str:
    desc = token.get("$description", "").strip()
    raw = token["$value"]
    if isinstance(raw, str) and raw.startswith("{") and raw.endswith("}"):
        return desc
    value = resolve(raw, index)
    if typ == "dimension":
        suffix = f"{value['value']}{value['unit']} = {px_number(value):g}px"
    elif typ == "duration":
        suffix = f"{value['value']}ms" if value["unit"] == "ms" else f"{value['value']}s = {ms_number(value):g}ms"
    elif typ == "fontWeight":
        suffix = f"{value}"
    else:
        return desc
    return f"{desc}（{suffix}）" if desc else suffix


def render_figma_import(index: dict) -> dict:
    root: dict = {}
    for path, (token, typ) in index.items():
        node = root
        parts = path.split(".")
        for part in parts[:-1]:
            child = node.get(part)
            if child is None:
                child = {}
                node[part] = child
            node = child
        leaf = {
            "$type": figma_import_type(typ),
            "$value": figma_import_value(path, token, typ, index),
        }
        desc = figma_import_description(token, typ, index)
        if desc:
            leaf["$description"] = desc
        node[parts[-1]] = leaf
    return root


def hex_to_rgba(hex_value: str) -> dict:
    h = hex_value.lstrip("#")
    if len(h) == 8:
        r, g, b, a = h[0:2], h[2:4], h[4:6], h[6:8]
        return {"r": int(r, 16) / 255, "g": int(g, 16) / 255, "b": int(b, 16) / 255, "a": int(a, 16) / 255}
    if len(h) != 6:
        raise SystemExit(f"invalid color {hex_value}")
    return {"r": int(h[0:2], 16) / 255, "g": int(h[2:4], 16) / 255, "b": int(h[4:6], 16) / 255, "a": 1.0}


THEME_MAP = [
    ("--td-brand-color", "color.brand.primary"),
    ("--td-brand-color-active", "color.brand.active"),
    ("--td-brand-color-disabled", "color.brand.disabled"),
    ("--td-brand-color-focus", "color.focus.ring"),
    ("--td-brand-color-light", "color.brand.light"),
    ("--td-brand-color-light-active", "color.brand.lightHover"),
    ("--td-text-color-brand", "color.brand.hover"),
    ("--td-text-color-link", "color.brand.hover"),
    ("--td-success-color", "color.semantic.success"),
    ("--td-success-color-light", "color.semantic.successLight"),
    ("--td-warning-color", "color.semantic.warning"),
    ("--td-warning-color-light", "color.semantic.warningLight"),
    ("--td-error-color", "color.semantic.error"),
    ("--td-error-color-light", "color.semantic.errorLight"),
    ("--td-text-color-primary", "color.text.primary"),
    ("--td-text-color-secondary", "color.text.secondary"),
    ("--td-text-color-placeholder", "color.neutral.400"),
    ("--td-text-color-disabled", "color.neutral.300"),
    ("--td-text-color-anti", "color.text.anti"),
    ("--td-bg-color-page", "color.bg.page"),
    ("--td-bg-color-container", "color.bg.surface"),
    ("--td-bg-color-container-active", "color.bg.surfaceAlt"),
    ("--td-bg-color-secondarycontainer", "color.neutral.100"),
    ("--td-bg-color-secondarycontainer-active", "color.neutral.200"),
    ("--td-bg-color-component", "color.neutral.200"),
    ("--td-bg-color-component-active", "color.neutral.300"),
    ("--td-bg-color-component-disabled", "color.neutral.100"),
    ("--td-bg-color-secondarycomponent", "color.neutral.200"),
    ("--td-bg-color-secondarycomponent-active", "color.neutral.300"),
    ("--td-bg-color-specialcomponent", "color.bg.surface"),
    ("--td-component-stroke", "color.border.default"),
    ("--td-border-color", "color.border.default"),
    ("--td-border-level-1-color", "color.border.default"),
    ("--td-component-border", "color.border.default"),
    ("--td-border-level-2-color", "color.border.strong"),
    ("--td-font-family", "font.family.sans"),
    ("--td-font-size-s", "font.size.24"),
    ("--td-font-size-base", "font.size.28"),
    ("--td-font-size-m", "font.size.32"),
    ("--td-font-size-l", "font.size.36"),
    ("--td-font-size-xl", "font.size.40"),
    ("--td-font-size-xxl", "font.size.48"),
    ("--td-line-height-body-extraSmall", "font.lineHeight.24"),
    ("--td-line-height-body-small", "font.lineHeight.28"),
    ("--td-line-height-title-small", "font.lineHeight.32"),
    ("--td-line-height-title-medium", "font.lineHeight.36"),
    ("--td-line-height-title-large", "font.lineHeight.40"),
    ("--td-line-height-title-extraLarge", "font.lineHeight.48"),
    ("--td-line-height-headline-large", "font.lineHeight.48"),
    ("--td-radius-small", "radius.8"),
    ("--td-radius-default", "radius.16"),
    ("--td-radius-large", "radius.24"),
    ("--td-radius-round", "radius.full"),
    ("--td-spacer", "space.16"),
    ("--td-spacer-1", "space.24"),
    ("--td-spacer-2", "space.32"),
    ("--td-spacer-3", "space.48"),
    ("--td-spacer-4", "space.64"),
    ("--td-shadow-1", "shadow.sm"),
    ("--td-shadow-2", "shadow.md"),
    ("--td-shadow-3", "shadow.lg"),
    ("--td-anim-duration-base", "motion.duration.base"),
    ("--td-anim-time-fn-easing", "motion.easing.standard"),
    ("--td-anim-time-fn-ease-out", "motion.easing.decelerate"),
]

# Web preview extensions: not TDesign mini-program variables, clearly namespaced.
DEMO_EXTRA_MAP = [
    ("--brand-color-hover", "color.brand.hover"),
    ("--brand-bg-inverse", "color.bg.inverse"),
    ("--brand-info-color", "color.semantic.info"),
    ("--brand-info-color-light", "color.semantic.infoLight"),
    ("--brand-accent-color", "color.accent.primary"),
    ("--brand-accent-light", "color.accent.light"),
    ("--brand-font-weight-regular", "font.weight.regular"),
    ("--brand-font-weight-medium", "font.weight.medium"),
    ("--brand-font-weight-semibold", "font.weight.semibold"),
    ("--brand-duration-fast", "motion.duration.fast"),
]

BODY_TEXT = [
    ("正文主文字", "color.text.primary"),
    ("正文二级", "color.text.secondary"),
    ("正文三级", "color.text.tertiary"),
    ("正文弱化", "color.text.muted"),
]
LIGHT_BACKGROUNDS = [
    ("白底", "color.bg.surface"),
    ("页面底", "color.bg.page"),
    ("次级容器底", "color.bg.surfaceAlt"),
    ("中性 100", "color.neutral.100"),
    ("中性 200", "color.neutral.200"),
    ("品牌浅底", "color.brand.light"),
    ("成功浅底", "color.semantic.successLight"),
    ("警告浅底", "color.semantic.warningLight"),
    ("错误浅底", "color.semantic.errorLight"),
    ("信息浅底", "color.semantic.infoLight"),
    ("辅助浅底", "color.accent.light"),
]
DARK_BACKGROUNDS = [
    ("品牌主色", "color.brand.primary"),
    ("品牌悬停", "color.brand.hover"),
    ("品牌按下", "color.brand.active"),
    ("成功", "color.semantic.success"),
    ("警告", "color.semantic.warning"),
    ("错误", "color.semantic.error"),
    ("信息", "color.semantic.info"),
    ("辅助色", "color.accent.primary"),
    ("反色底", "color.bg.inverse"),
]

CONTRAST_PAIRS = []
for _text_label, _fg in BODY_TEXT:
    for _bg_label, _bg in LIGHT_BACKGROUNDS:
        CONTRAST_PAIRS.append((f"{_text_label} / {_bg_label}", _fg, _bg))
for _bg_label, _bg in DARK_BACKGROUNDS:
    CONTRAST_PAIRS.append((f"反白文字 / {_bg_label}", "color.text.anti", _bg))
for _bg_label, _bg in (("白底", "color.bg.surface"), ("页面底", "color.bg.page"), ("品牌浅底", "color.brand.light")):
    CONTRAST_PAIRS.append((f"品牌链接 / {_bg_label}", "color.brand.hover", _bg))
CONTRAST_PAIRS.append(("品牌主色文字 / 品牌浅底", "color.brand.primary", "color.brand.light"))


def theme_lines(index) -> list[str]:
    lines = [
        "/* Generated by scripts/build.py from tokens.json. DO NOT EDIT. */",
        "/* TDesign mini-program theme variables; 2rpx = 1px at 375pt viewport. */",
        "page, .td-theme {",
    ]
    for css_var, path in THEME_MAP:
        token, typ = index[path]
        lines.append(f"  {css_var}: {css_value(path, token, typ, index)};")
    return lines


def render_theme(index) -> str:
    return "\n".join(theme_lines(index) + ["}"]) + "\n"


def render_demo_theme(index) -> str:
    lines = theme_lines(index)
    lines += ["", "  /* Web preview extensions (not TDesign variables). */"]
    for css_var, path in DEMO_EXTRA_MAP:
        token, typ = index[path]
        lines.append(f"  {css_var}: {css_value(path, token, typ, index)};")
    lines.append("}")
    text = "\n".join(lines) + "\n"
    text = text.replace("rpx", "px")
    text = text.replace(
        "/* TDesign mini-program theme variables; 2px = 1px at 375pt viewport. */",
        "/* Browser preview: 2rpx = 1px, so a 750px-wide screenshot equals a 375pt device at 2x. */",
    )
    return text


def luminance(hex_value: str) -> float:
    h = hex_value.lstrip("#")
    if len(h) == 8:
        h = h[:6]
    if len(h) != 6:
        raise SystemExit(f"invalid color {hex_value}")
    parts = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    def linear(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (linear(p) for p in parts)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def main() -> None:
    data = load_tokens()
    index = build_index(data)
    if not index:
        raise SystemExit("no tokens found")
    for path, (token, typ) in index.items():
        if typ not in TYPE_NAMES:
            raise SystemExit(f"invalid or missing type at {path}: {typ!r}")
        if not isinstance(token.get("$value"), (str, int, float, list, dict)):
            raise SystemExit(f"invalid $value at {path}")

    for _, path in THEME_MAP:
        if path not in index:
            raise SystemExit(f"theme mapping target missing: {path}")

    theme = render_theme(index)
    THEME_PATH.write_text(theme, encoding="utf-8")
    DEMO_CSS_PATH.write_text(render_demo_theme(index), encoding="utf-8")

    figma_vars = []
    for path, (token, typ) in index.items():
        if typ not in {"color", "dimension", "fontFamily", "fontWeight", "shadow", "duration", "cubicBezier", "number"}:
            continue
        figma_vars.append({
            "name": path,
            "tokenPath": path,
            "type": figma_type(typ),
            "value": figma_value(path, token, typ, index),
            "description": token.get("$description", ""),
        })
    payload = {
        "name": "会员空间平台 / Theme",
        "generatedFrom": "tokens.json",
        "tokensHash": hashlib.sha256(TOKENS_PATH.read_bytes()).hexdigest(),
        "collections": [{"name": "Theme", "modes": ["Light"], "variables": figma_vars}],
    }
    FIGMA_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    import_payload = render_figma_import(index)
    import_text = json.dumps(import_payload, ensure_ascii=False, indent=2) + "\n"
    FIGMA_IMPORT_PATH.write_text(import_text, encoding="utf-8")
    # Figma uses the imported file name as the mode name; Light.tokens.json -> mode "Light".
    FIGMA_LIGHT_IMPORT_PATH.write_text(import_text, encoding="utf-8")

    js_lines = [
        "// Generated by scripts/build.py from tokens.json. DO NOT EDIT.",
        "// Figma Plugin API: idempotently sync one variable collection with the same names/values as tokens.json.",
        "// Usage: Figma desktop -> Plugins -> Development -> Import plugin from manifest.json, then run.",
        "const COLLECTION_NAME = 'MemberSpace / Theme';",
        "const VARIABLES = " + json.dumps(figma_vars, ensure_ascii=False, indent=2) + ";",
        "",
        "function findCollection(name) {",
        "  const all = figma.variables.getLocalVariableCollections();",
        "  return all.find(function (c) { return c.name === name; }) || null;",
        "}",
        "",
        "const collection = findCollection(COLLECTION_NAME) || figma.variables.createVariableCollection(COLLECTION_NAME);",
        "const modeId = collection.modes[0].modeId;",
        "const existing = figma.variables.getLocalVariables().filter(function (v) { return v.variableCollectionId === collection.id; });",
        "const byName = {};",
        "for (const v of existing) byName[v.name] = v;",
        "const wanted = {};",
        "const conflicts = [];",
        "for (const v of VARIABLES) {",
        "  wanted[v.name] = true;",
        "  let variable = byName[v.name] || null;",
        "  if (variable && variable.resolvedType !== v.type) { conflicts.push(v.name); continue; }",
        "  if (!variable) variable = figma.variables.createVariable(v.name, collection, v.type);",
        "  if (v.type === 'COLOR') {",
        "    const h = v.value.replace('#', '');",
        "    const a = h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1;",
        "    variable.setValueForMode(modeId, { r: parseInt(h.slice(0,2),16)/255, g: parseInt(h.slice(2,4),16)/255, b: parseInt(h.slice(4,6),16)/255, a });",
        "  } else if (v.type === 'FLOAT') {",
        "    variable.setValueForMode(modeId, Number(v.value));",
        "  } else {",
        "    variable.setValueForMode(modeId, String(v.value));",
        "  }",
        "  if (v.description) variable.description = v.description;",
        "}",
        "const extras = existing.filter(function (v) { return !wanted[v.name]; }).map(function (v) { return v.name; });",
        "if (conflicts.length) console.warn('Skipped type conflicts (left untouched): ' + conflicts.join(', '));",
        "if (extras.length) console.warn('Left unrelated existing variables untouched: ' + extras.join(', '));",
        "figma.notify('Synced ' + (VARIABLES.length - conflicts.length) + ' variables in ' + COLLECTION_NAME + '; ' + conflicts.length + ' type conflicts skipped; ' + extras.length + ' existing variables left untouched');",
        "figma.closePlugin();",
    ]
    FIGMA_PLUGIN_PATH.write_text("\n".join(js_lines) + "\n", encoding="utf-8")
    manifest = {
        "name": "1835 Brand Theme Variables",
        "api": "1.0.0",
        "main": "create-variables.js",
        "editorType": ["figma"],
    }
    FIGMA_MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rows = []
    failures = []
    for label, fg_path, bg_path in CONTRAST_PAIRS:
        fg = resolve(index[fg_path][0]["$value"], index)
        bg = resolve(index[bg_path][0]["$value"], index)
        ratio = contrast(fg, bg)
        ok = ratio >= 4.5
        if not ok:
            failures.append(f"{label}: {ratio:.2f}")
        rows.append((label, fg, bg, ratio, "PASS" if ok else "FAIL"))
    if failures:
        raise SystemExit("contrast failures: " + "; ".join(failures))

    lines = [
        "# 对比度检查表",
        "",
        "口径：WCAG 2.1 相对亮度；正文文字与背景对比度 >= 4.5:1。全部数值由 scripts/build.py 计算。",
        "",
        "| 组合 | 前景 | 背景 | 对比度 | 结果 |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for label, fg, bg, ratio, status in rows:
        lines.append(f"| {label} | {fg} | {bg} | {ratio:.2f}:1 | {status} |")
    lines += [
        "",
        "## 统计与说明",
        "",
        "- 上表覆盖 4 种正文文字（主/二级/三级/弱化）× 11 种浅底，以及反白文字 × 9 种深底。",
        "- 表外颜色只用于边框、占位、禁用态、装饰性色块，不作为正文文字。",
        "- 品牌链接统一使用品牌悬停色，避免主色在浅底上余量不足。",
        "- 最小对比度由 scripts/build.py 计算并断言，低于 4.5:1 会直接失败。",
    ]
    CONTRAST_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    figma_lines = [
        "# Figma 变量对照表",
        "",
        "在线 Figma 文件（viewer 可看）：" + FIGMA_FILE_URL,
        "",
        "该文件由 Figma Variables 导入 `figma/Light.tokens.json` 生成：collection `Theme`、mode `Light`、74 个变量；Figma 中显示为 / 分隔的嵌套分组，对应下表的点分路径。",
        "`figma/figma-import.tokens.json` 为同一 DTCG 数据的通用文件名副本；`figma/figma-variables.json` 与 `figma/create-variables.js` 是机器可读定义和桌面插件备选路径。",
        "",
        "变量名严格等于 tokens.json 的点分路径。尺寸按 2rpx = 1px 换算为 Figma 数值；别名保留为 `{path}` 引用。",
        "",
        "| # | token 路径 | Figma 变量名 | Figma 类型 | 值 | 说明 |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for i, v in enumerate(figma_vars, 1):
        val = v["value"]
        if isinstance(val, (dict, list)):
            val = json.dumps(val, ensure_ascii=False)
        figma_lines.append(f"| {i} | {v['tokenPath']} | {v['name']} | {v['type']} | {val} | {v['description']} |")
    FIGMA_DOC_PATH.write_text("\n".join(figma_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "tokens": len(index),
        "themeVariables": len(THEME_MAP),
        "figmaVariables": len(figma_vars),
        "figmaImportVariables": len(index),
        "contrastPairs": len(rows),
        "minContrast": round(min(r[3] for r in rows), 2),
        "tokensHash": hashlib.sha256(TOKENS_PATH.read_bytes()).hexdigest(),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
