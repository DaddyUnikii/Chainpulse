"""Core logic: query an EVM JSON-RPC endpoint and measure its health."""

from __future__ import annotations

import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from typing import Optional

DEFAULT_TIMEOUT = 8.0


@dataclass
class RpcResult:
    name: str
    url: str
    ok: bool
    chain_id: Optional[int] = None
    block: Optional[int] = None
    latency_ms: Optional[float] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


def _call(url: str, method: str, timeout: float) -> object:
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": []}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "chainpulse/0.1"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode())
    if "error" in body:
        raise RuntimeError(body["error"].get("message", "rpc error"))
    return body["result"]


def check(name: str, url: str, timeout: float = DEFAULT_TIMEOUT) -> RpcResult:
    """Check one endpoint: block height, chain id and round-trip latency."""
    try:
        start = time.perf_counter()
        block_hex = _call(url, "eth_blockNumber", timeout)
        latency = (time.perf_counter() - start) * 1000
        chain_hex = _call(url, "eth_chainId", timeout)
        return RpcResult(
            name=name,
            url=url,
            ok=True,
            chain_id=int(str(chain_hex), 16),
            block=int(str(block_hex), 16),
            latency_ms=round(latency, 1),
        )
    except Exception as exc:  # noqa: BLE001 - we report any failure
        return RpcResult(name=name, url=url, ok=False, error=str(exc)[:80])


def check_all(endpoints: dict[str, str], timeout: float = DEFAULT_TIMEOUT) -> list[RpcResult]:
    """Check many endpoints in parallel, fastest first, failures last."""
    with ThreadPoolExecutor(max_workers=min(16, max(1, len(endpoints)))) as pool:
        results = list(pool.map(lambda kv: check(kv[0], kv[1], timeout), endpoints.items()))
    return sorted(results, key=lambda r: (not r.ok, r.latency_ms or 0))
