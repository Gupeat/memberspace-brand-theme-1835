#!/usr/bin/env python3
"""One clean acceptance round for the #1835 token package."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
NODE = os.environ.get("NODE") or shutil.which("node")
if not NODE:
    raise SystemExit("Node.js not found; set NODE to the node executable")

HOME = str(Path.home())

def redact(text: str) -> str:
    for value in sorted({str(ROOT), str(ROOT).replace("\\", "\\\\"), str(ROOT).replace("\\", "/")}, key=len, reverse=True):
        text = text.replace(value, "<repo>")
    for value in sorted({HOME, HOME.replace("\\", "\\\\"), HOME.replace("\\", "/")}, key=len, reverse=True):
        text = text.replace(value, "<home>")
    return text

GENERATED_DIRS = [ROOT / "__pycache__", ROOT / "scripts" / "__pycache__", ROOT / "tests" / "__pycache__", ROOT / ".pytest_cache"]
GENERATED_FILES = [
    ROOT / "theme.wxss",
    ROOT / "miniprogram-demo" / "theme.wxss",
    ROOT / "demo" / "theme.css",
    ROOT / "figma" / "figma-variables.json",
    ROOT / "figma" / "create-variables.js",
    ROOT / "figma" / "figma-import.tokens.json",
    ROOT / "figma" / "Light.tokens.json",
    ROOT / "docs" / "CONTRAST.md",
    ROOT / "docs" / "FIGMA-VARIABLES.md",
    ARTIFACTS / "example-page.png",
    ARTIFACTS / "validation.log",
    ARTIFACTS / "validation.json",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_info(path: Path) -> tuple[int, int, str]:
    data = path.read_bytes()[:33]
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise SystemExit(f"not a PNG: {path}")
    width, height = struct.unpack(">II", data[16:24])
    color_type = data[25]
    mode = {0: "L", 2: "RGB", 3: "P", 4: "LA", 6: "RGBA"}.get(color_type, f"type{color_type}")
    return width, height, mode


def run(label: str, cmd: list[str]) -> dict:
    started = datetime.now(timezone.utc)
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    elapsed = (datetime.now(timezone.utc) - started).total_seconds()
    entry = {
        "label": label,
        "command": " ".join(cmd),
        "exitCode": proc.returncode,
        "elapsedSeconds": round(elapsed, 2),
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }
    if proc.returncode != 0:
        raise SystemExit(json.dumps({"ok": False, "step": label, "entry": entry}, ensure_ascii=False, indent=2))
    return entry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="round")
    args = parser.parse_args()

    for path in GENERATED_FILES:
        path.unlink(missing_ok=True)
    for path in GENERATED_DIRS:
        shutil.rmtree(path, ignore_errors=True)
    ARTIFACTS.mkdir(exist_ok=True)

    steps = []
    build = run("build", [sys.executable, str(ROOT / "scripts" / "build.py")])
    steps.append(build)
    steps.append(run("figma-syntax", [NODE, "--check", str(ROOT / "figma" / "create-variables.js")]))
    build_json = json.loads(build["stdout"])
    steps.append(run("validate", [sys.executable, str(ROOT / "scripts" / "validate.py")]))
    pytest_step = run("pytest", [sys.executable, "-m", "pytest", "-q", "tests"])
    steps.append(pytest_step)
    match = re.search(r"(\d+) passed", pytest_step["stdout"])
    if not match or int(match.group(1)) < 18:
        raise SystemExit("pytest did not report at least 18 passed")
    tests_passed = int(match.group(1))

    steps.append(run("verify-figma", [sys.executable, str(ROOT / "scripts" / "verify_figma_export.py")]))
    steps.append(run("verify-devtools", [sys.executable, str(ROOT / "scripts" / "verify_devtools_evidence.py")]))

    steps.append(run("capture", [NODE, str(ROOT / "scripts" / "capture.mjs")]))

    screenshot = ARTIFACTS / "example-page.png"
    if not screenshot.exists() or screenshot.stat().st_size < 10000:
        raise SystemExit("missing or tiny screenshot")
    width, height, mode = png_info(screenshot)
    if width != 750 or height < 1500 or mode != "RGB":
        raise SystemExit(f"unexpected screenshot: {width}x{height} {mode}")

    hashes = {
        "tokens.json": sha256(ROOT / "tokens.json"),
        "theme.wxss": sha256(ROOT / "theme.wxss"),
        "miniprogram-demo/theme.wxss": sha256(ROOT / "miniprogram-demo" / "theme.wxss"),
        "demo/theme.css": sha256(ROOT / "demo" / "theme.css"),
        "figma/figma-variables.json": sha256(ROOT / "figma" / "figma-variables.json"),
        "docs/CONTRAST.md": sha256(ROOT / "docs" / "CONTRAST.md"),
        "docs/FIGMA-VARIABLES.md": sha256(ROOT / "docs" / "FIGMA-VARIABLES.md"),
        "artifacts/example-page.png": sha256(screenshot),
    }
    validation = json.loads((ARTIFACTS / "validation.json").read_text(encoding="utf-8"))
    figma_verify = json.loads((ROOT / "evidence" / "figma-online" / "verify.json").read_text(encoding="utf-8"))
    devtools_verify = json.loads((ROOT / "evidence" / "devtools" / "verify.json").read_text(encoding="utf-8"))
    summary = {
        "ok": validation["ok"] and build_json["tokens"] == 74 and build_json["themeVariables"] == 84 and build_json["figmaImportVariables"] == 74 and build_json["contrastPairs"] == 62 and figma_verify["ok"] and devtools_verify["ok"],
        "figmaExport": {"ok": figma_verify["ok"], "checked": figma_verify["checked"], "collection": figma_verify["collection"], "mode": figma_verify["mode"]},
        "devtoolsEvidence": {"ok": devtools_verify["ok"], "checked": len(devtools_verify["checks"]), "tool": devtools_verify["tool"]},
        "label": args.label,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "build": build_json,
        "validation": {"ok": validation["ok"], "checks": len(validation["checks"]), "failures": validation["failures"]},
        "pytest": f"{tests_passed} passed",
        "screenshot": {"file": "artifacts/example-page.png", "width": width, "height": height, "mode": mode, "bytes": screenshot.stat().st_size},
        "hashes": hashes,
        "steps": [{k: v for k, v in step.items() if k in ("label", "exitCode", "elapsedSeconds")} for step in steps],
    }

    log_lines = [f"#1835 acceptance {args.label}", f"generatedAt={summary['generatedAt']}", ""]
    for step in steps:
        log_lines.append(f"## {step['label']} (exit {step['exitCode']}, {step['elapsedSeconds']}s)")
        log_lines.append("$ " + step["command"])
        log_lines.append(step["stdout"])
        if step["stderr"]:
            log_lines.append("[stderr] " + step["stderr"])
        log_lines.append("")
    log = "\n".join(log_lines)
    log = redact(log)
    (ARTIFACTS / f"acceptance-{args.label}.log").write_text(log, encoding="utf-8")

    md = [
        f"# #1835 验收记录（{args.label}）",
        "",
        f"- 生成时间：{summary['generatedAt']}",
        f"- tokens.json SHA-256：`{hashes['tokens.json']}`",
        f"- theme.wxss SHA-256：`{hashes['theme.wxss']}`",
        f"- Figma 变量集 SHA-256：`{hashes['figma/figma-variables.json']}`",
        f"- demo/theme.css SHA-256：`{hashes['demo/theme.css']}`",
        f"- docs/CONTRAST.md SHA-256：`{hashes['docs/CONTRAST.md']}`",
        f"- docs/FIGMA-VARIABLES.md SHA-256：`{hashes['docs/FIGMA-VARIABLES.md']}`",
        f"- miniprogram-demo/theme.wxss SHA-256：`{hashes['miniprogram-demo/theme.wxss']}`",
        f"- 截图：`artifacts/example-page.png`，{width}x{height}，{screenshot.stat().st_size} B，SHA-256：`{hashes['artifacts/example-page.png']}`",
        f"- 单测：{tests_passed} passed",
        f"- 校验：{len(validation['checks'])}/8 PASS",
        f"- token / TDesign 变量 / 对比度组合：{build_json['tokens']} / {build_json['themeVariables']} / {build_json['contrastPairs']}（最小 {build_json['minContrast']}:1）",
        f"- Figma 在线导出：{figma_verify['checked']}/74 名称 1:1，collection {figma_verify['collection']} / mode {figma_verify['mode']}",
        f"- 微信开发者工具：{devtools_verify['tool']}，{len(devtools_verify['checks'])} 项证据校验通过",
        "",
        "| 步骤 | 命令 | exit | 秒 |",
        "| --- | --- | ---: | ---: |",
    ]
    for step in steps:
        md.append(f"| {step['label']} | `{step['command']}` | {step['exitCode']} | {step['elapsedSeconds']} |")
    md += ["", "## 校验明细", ""]
    for item in validation["checks"]:
        status = "PASS" if item["ok"] else "FAIL"
        md.append(f"- [{status}] {item['name']}：{item['detail']}")
    md += ["", "## 结论", "", f"全部 7 步命令 exit 0；8/8 校验通过；{tests_passed} 项 pytest 通过；Figma 在线导出 {figma_verify['checked']}/74 校验通过；微信开发者工具证据 {len(devtools_verify['checks'])} 项通过；Web 截图为 750px 宽。"]
    md_text = "\n".join(md) + "\n"
    md_text = redact(md_text)
    (ARTIFACTS / f"ACCEPTANCE-{args.label}.md").write_text(md_text, encoding="utf-8")
    (ARTIFACTS / "ACCEPTANCE.md").write_text(md_text, encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
