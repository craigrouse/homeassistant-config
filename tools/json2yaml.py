#!/usr/bin/env python3
"""Convert HA automation config JSON (as returned by the config API) to readable YAML.

Usage: python3 tools/json2yaml.py <src_dir> <dest_dir>
Multiline strings (Jinja templates) are emitted as literal blocks.
"""
import json
import sys
from pathlib import Path

import yaml


class LiteralStr(str):
    pass


def _literal_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(LiteralStr, _literal_representer)


def literalize(obj):
    if isinstance(obj, dict):
        return {k: literalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [literalize(v) for v in obj]
    if isinstance(obj, str) and "\n" in obj:
        # Literal blocks cannot carry trailing spaces before newlines
        cleaned = "\n".join(line.rstrip() for line in obj.split("\n"))
        return LiteralStr(cleaned)
    return obj


def main(src_dir: str, dest_dir: str) -> None:
    src, dest = Path(src_dir), Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    for jf in sorted(src.glob("*.json")):
        config = json.loads(jf.read_text())
        out = dest / (jf.stem + ".yaml")
        out.write_text(
            yaml.dump(
                literalize(config),
                sort_keys=False,
                allow_unicode=True,
                width=120,
                default_flow_style=False,
            )
        )
        print(f"{jf.name} -> {out.name}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
