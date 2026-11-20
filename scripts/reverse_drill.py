#!/usr/bin/env python3
"""Reverse drill: inject three defects into a throwaway copy and prove the gates catch them."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "artifacts" / "reverse-drill.log"
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def run(cwd: Path, script: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(cwd / "scripts" / script)], cwd=cwd, capture_output=True, text=True, encoding="utf-8", env=ENV)


def copy_repo() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="clawhunt-1835-")) / "repo"
    shutil.copytree(ROOT, tmp, ignore=shutil.ignore_patterns("artifacts", "__pycache__", ".pytest_cache", "*.pyc"))
    (tmp / "artifacts").mkdir(exist_ok=True)
    return tmp


def main() -> None:
    lines = ["#1835 reverse drill", ""]
    results = []

    base = copy_repo()
    try:
        build = run(base, "build.py")
        validate = run(base, "validate.py")
        if build.returncode != 0 or validate.returncode != 0:
            raise SystemExit("baseline copy failed; refusing to run mutation drill")
        lines += ["BASELINE build=0 validate=0", ""]
    finally:
        shutil.rmtree(base.parent, ignore_errors=True)

    def case_contrast(tmp: Path) -> tuple[bool, str]:
        path = tmp / "tokens.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        try:
            value = payload["color"]["neutral"]["500"]["$value"]
        except KeyError:
            return False, "target token color.neutral.500 not found"
        if value.get("hex") != "#57677C":
            return False, f"unexpected neutral.500 hex: {value.get('hex')!r}"
        value["hex"] = "#D5DAE2"
        value["components"] = [round(0xD5 / 255, 6), round(0xDA / 255, 6), round(0xE2 / 255, 6)]
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        proc = run(tmp, "build.py")
        return proc.returncode != 0, proc.stdout + proc.stderr

    def case_theme_mapping(tmp: Path) -> tuple[bool, str]:
        path = tmp / "scripts" / "build.py"
        text = path.read_text(encoding="utf-8")
        needle = '    ("--td-brand-color", "color.brand.primary"),\n'
        if needle not in text:
            return False, "theme mapping line not found"
        path.write_text(text.replace(needle, "", 1), encoding="utf-8")
        build = run(tmp, "build.py")
        validate = run(tmp, "validate.py")
        return validate.returncode != 0, build.stdout + validate.stdout + validate.stderr

    def case_figma_name(tmp: Path) -> tuple[bool, str]:
        build = run(tmp, "build.py")
        if build.returncode != 0:
            return False, "baseline build failed"
        path = tmp / "figma" / "figma-variables.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        first = payload["collections"][0]["variables"][0]
        first["name"] = first["name"] + ".broken"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        validate = run(tmp, "validate.py")
        return validate.returncode != 0, validate.stdout + validate.stderr

    cases = [
        ("A: contrast regression (neutral.500 #57677C -> #D5DAE2)", case_contrast),
        ("B: removed TDesign brand mapping", case_theme_mapping),
        ("C: stale/renamed Figma variable", case_figma_name),
    ]
    detected = 0
    for name, fn in cases:
        tmp = copy_repo()
        try:
            ok, output = fn(tmp)
            tail = "\n".join((output or "").strip().splitlines()[-4:])
            status = "yes" if ok else "NO"
            lines += [f"{name}: DETECTED={status}", tail, ""]
            results.append({"name": name, "detected": ok, "tail": tail})
            if ok:
                detected += 1
        finally:
            shutil.rmtree(tmp.parent, ignore_errors=True)

    summary = f"mutations={len(cases)} detected={detected}"
    lines.append("RESULT: " + summary)
    LOG.parent.mkdir(exist_ok=True)
    LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": detected == len(cases), "mutations": len(cases), "detected": detected, "results": results}, ensure_ascii=False, indent=2))
    if detected != len(cases):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
