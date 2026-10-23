"""Command line interface for ChainPulse."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import DEFAULT_TIMEOUT, check_all

DEFAULT_ENDPOINTS = {
    "Ethereum": "https://ethereum-rpc.publicnode.com",
    "BNB Chain": "https://bsc-rpc.publicnode.com",
    "Polygon": "https://polygon-bor-rpc.publicnode.com",
    "Arbitrum": "https://arbitrum-one-rpc.publicnode.com",
    "Base": "https://base-rpc.publicnode.com",
}

GREEN, RED, DIM, BOLD, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


def _color(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{RESET}" if enabled else text


def render_table(results, color: bool = True) -> str:
    headers = ["", "Network", "Chain ID", "Block", "Latency"]
    rows = []
    for r in results:
        if r.ok:
            rows.append(["●", r.name, str(r.chain_id), f"{r.block:,}", f"{r.latency_ms:.0f} ms"])
        else:
            rows.append(["●", r.name, "-", "-", r.error or "down"])
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = lambda cells: "  ".join(str(c).ljust(w) for c, w in zip(cells, widths))
    out = [_color(line(headers), BOLD, color)]
    for r, row in zip(results, rows):
        text = line(row)
        dot = _color("●", GREEN if r.ok else RED, color)
        out.append(dot + text[1:])
    up = sum(r.ok for r in results)
    out.append(_color(f"\n{up}/{len(results)} endpoints healthy", DIM, color))
    return "\n".join(out)


def load_endpoints(path: str | None) -> dict[str, str]:
    if not path:
        return DEFAULT_ENDPOINTS
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict) or not data:
        raise SystemExit("config must be a JSON object of {\"name\": \"rpc_url\"}")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="chainpulse",
        description="Check the health of EVM RPC endpoints: block height, chain id and latency.",
    )
    parser.add_argument("-c", "--config", help="JSON file mapping names to RPC URLs")
    parser.add_argument("-u", "--url", action="append", help="check a single RPC URL (repeatable)")
    parser.add_argument("-t", "--timeout", type=float, default=DEFAULT_TIMEOUT, help="seconds per request")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--no-color", action="store_true", help="disable colored output")
    parser.add_argument("-V", "--version", action="version", version=f"chainpulse {__version__}")
    args = parser.parse_args(argv)

    endpoints = {u: u for u in args.url} if args.url else load_endpoints(args.config)
    results = check_all(endpoints, timeout=args.timeout)

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
    else:
        print(render_table(results, color=not args.no_color and sys.stdout.isatty()))
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
