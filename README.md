<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7F00FF,100:00D4FF&height=200&section=header&text=ChainPulse&fontSize=70&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Health%20checks%20for%20EVM%20RPC%20endpoints&descAlignY=58&descSize=18" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3000&pause=800&color=00D4FF&center=true&vCenter=true&width=600&lines=Is+your+node+alive%3F;Is+it+synced%3F;Is+it+fast%3F;One+command.+Zero+dependencies.+%E2%9A%A1" alt="Typing SVG" />

<p>
  <a href="https://github.com/DaddyUnikii/chainpulse/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/DaddyUnikii/chainpulse/ci.yml?style=for-the-badge&logo=githubactions&logoColor=white&label=CI" alt="CI"/></a>
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Dependencies-Zero-00C853?style=for-the-badge" alt="Zero dependencies"/>
  <img src="https://img.shields.io/badge/License-MIT-7F00FF?style=for-the-badge" alt="MIT"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Ethereum-3C3C3D?style=flat-square&logo=ethereum&logoColor=white"/>
  <img src="https://img.shields.io/badge/BNB%20Chain-F0B90B?style=flat-square&logo=binance&logoColor=black"/>
  <img src="https://img.shields.io/badge/Polygon-7B3FE4?style=flat-square&logo=polygon&logoColor=white"/>
  <img src="https://img.shields.io/badge/Arbitrum-28A0F0?style=flat-square"/>
  <img src="https://img.shields.io/badge/Base-0052FF?style=flat-square"/>
</p>

<img src="assets/demo.svg" alt="ChainPulse demo" width="720"/>

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

⚡ **Parallel checks** — every endpoint at once, results in about a second

🧱 **Block height & chain ID** — spot a stalled or misconfigured node instantly

⏱ **Latency** — sorted fastest first, failures always last

</td>
<td width="50%">

📦 **Zero dependencies** — pure Python standard library

🤖 **Script friendly** — `--json` output and a meaningful exit code

🛰 **Your own nodes** — check validators and private RPCs by URL or config

</td>
</tr>
</table>

## 🚀 Quick start

```bash
git clone https://github.com/DaddyUnikii/chainpulse.git
cd chainpulse
python -m chainpulse
```

Install it as a global command:

```bash
pip install .
chainpulse
```

## 🛠 Usage

| Command | What it does |
|:--|:--|
| `chainpulse` | Check the built-in public endpoints |
| `chainpulse -u http://localhost:8545` | Check your own node (repeatable) |
| `chainpulse -c rpcs.example.json` | Check a list from a JSON file |
| `chainpulse --json` | Machine-readable output for scripts and bots |
| `chainpulse -t 3` | Timeout per request, in seconds |

<details>
<summary><b>📁 Config file format</b></summary>

```json
{
  "Ethereum": "https://ethereum-rpc.publicnode.com",
  "My Validator": "http://10.0.0.5:8545"
}
```

</details>

<details>
<summary><b>🔔 Use it as a node alert</b></summary>

Exit code is `0` when every endpoint is healthy and `1` otherwise:

```bash
# crontab: check every 5 minutes
*/5 * * * * chainpulse -u http://localhost:8545 || curl -s "https://api.telegram.org/bot$TOKEN/sendMessage?chat_id=$CHAT&text=Node%20down"
```

</details>

<details>
<summary><b>🧾 JSON output</b></summary>

```json
[
  {
    "name": "Base",
    "url": "https://base-rpc.publicnode.com",
    "ok": true,
    "chain_id": 8453,
    "block": 52978387,
    "latency_ms": 168.0,
    "error": null
  }
]
```

</details>

## 🧪 Tests

```bash
python -m unittest discover -s tests -v
```

## 🗺 Roadmap

- [x] Parallel health checks with latency
- [x] JSON output & exit codes
- [ ] Sync-lag detection against a reference node
- [ ] Watch mode with live refresh
- [ ] Built-in Telegram / Discord alerts

## 🤝 Contributing

Issues and pull requests are welcome. If ChainPulse saves you a midnight node check, a ⭐ helps a lot.

<div align="center">

**Built with ☕ by [DaddyUnikii](https://github.com/DaddyUnikii)**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00D4FF,100:7F00FF&height=100&section=footer" width="100%"/>

</div>
