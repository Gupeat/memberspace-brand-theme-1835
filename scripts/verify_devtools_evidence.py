#!/usr/bin/env python3
"""Verify the WeChat DevTools evidence against the repository and run.json."""
from __future__ import annotations

import hashlib
import json
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "devtools"
RUN = EVIDENCE / "run.json"
OUT = EVIDENCE / "verify.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def check(name: str, condition: bool, detail: str) -> dict:
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    return {"name": name, "ok": True, "detail": detail}


def main() -> None:
    run = json.loads(read(RUN))
    checks = []

    screenshots = {}
    for key in ("screenshot_simulator", "screenshot_devtools"):
        item = run[key]
        path = ROOT / item["path"]
        actual = {
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "width": png_size(path)[0],
            "height": png_size(path)[1],
        }
        checks.append(check(key + " exists", path.is_file(), item["path"]))
        checks.append(check(key + " bytes", actual["bytes"] == item["bytes"], f'{actual["bytes"]} == {item["bytes"]}'))
        checks.append(check(key + " sha256", actual["sha256"] == item["sha256"], actual["sha256"]))
        checks.append(check(key + " dimensions", actual["width"] == item["width"] and actual["height"] == item["height"], f'{actual["width"]}x{actual["height"]}'))
        screenshots[key] = {"path": item["path"], **actual}

    project = json.loads(read(ROOT / "miniprogram-demo" / "project.config.json"))
    checks.append(check("appid", project.get("appid") == run["appid"], project.get("appid", "")))
    checks.append(check("libVersion", project.get("libVersion") == run["lib_version"], project.get("libVersion", "")))

    theme = read(ROOT / "theme.wxss")
    mini_theme = read(ROOT / "miniprogram-demo" / "theme.wxss")
    checks.append(check("miniprogram theme matches generated theme", mini_theme == theme, "byte-identical"))
    checks.append(check("app.wxss imports theme", '@import "./theme.wxss"' in read(ROOT / "miniprogram-demo" / "app.wxss"), "present"))

    wxml = read(ROOT / "miniprogram-demo" / "pages" / "index" / "index.wxml")
    checks.append(check("uses t-button", "t-button" in wxml, "t-button present"))
    checks.append(check("uses t-tag", "t-tag" in wxml, "t-tag present"))

    styles = run["computed_styles"]
    checks.append(check("primary button brand", styles["button_primary"]["background"] == "rgb(31, 94, 255)", styles["button_primary"]["background"]))
    checks.append(check("brand tag background", styles["tag_brand"]["background"] == "rgb(241, 244, 255)", styles["tag_brand"]["background"]))
    checks.append(check("brand tag text", styles["tag_brand"]["color"] == "rgb(31, 94, 255)", styles["tag_brand"]["color"]))
    checks.append(check("success tag", styles["tag_success"]["color"] == "rgb(14, 122, 95)", styles["tag_success"]["color"]))

    result = {
        "ok": True,
        "checkedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": run["tool"],
        "appid": run["appid"],
        "screenshots": screenshots,
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "checked": len(checks), "screenshots": screenshots, "verify": str(OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        sys.exit(1)
