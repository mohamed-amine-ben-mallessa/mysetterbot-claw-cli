<h1 align="center">🦅 MySetterBot Claw — CLI</h1>

<p align="center">
  <b>The Instagram action layer for AI agents.</b><br>
  One JSON-clean command for DMs, posts, stories, comments, follows, analytics — Graph API <i>and</i> private API, with your session in the OS keychain.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/instagram-CLI-E1306C?logo=instagram&logoColor=white" alt="Instagram">
  <img src="https://img.shields.io/badge/agent--ready-JSON%20envelope-6E59F7" alt="Agent-ready">
  <img src="https://img.shields.io/badge/session-OS%20keychain-1f9d55" alt="Keychain">
  <img src="https://img.shields.io/badge/python-%E2%89%A53.10-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="MIT">
</p>

```bash
pip install -e .
msbc auth login --username <you>
msbc --json dm inbox --limit 20
```

---

> This is the **CLI half** of MySetterBot Claw. The other half is
> [**mysetterbot-claw**](https://github.com/mohamed-amine-ben-mallessa/mysetterbot-claw) —
> an MCP server that wraps these actions as 42 agent tools and adds a free LLM layer
> that writes the openers, follow-ups and qualification messages.

## Why this exists

Most "Instagram automation" is a brittle browser macro or a paid SaaS dashboard. An agent
needs neither. It needs **one binary that speaks JSON**, returns predictable exit codes, and
keeps credentials out of plaintext.

- 🔐 **Sessions in your OS keychain** — never in a file, never in `.env`.
- 📦 **Clean JSON envelope** — `{ exit_code, data, backend_used }` on every call.
- 🔀 **Hybrid backend** — official Graph API when possible, private API when needed.
- 🛡️ **Growth gate** — follow / like / comment are *locked by default* behind
  `--enable-growth-actions` to protect the account.
- 🧩 **Agent manifest** — `msbc --json agent-info` returns the full machine-readable
  capability map (every command, args, exit codes, backends). Your agent discovers the
  tool instead of guessing at it.

## Install

| Surface | Install | Notes |
|---|---|---|
| **From this repo** | `pip install -e .` | Python ≥ 3.10 |
| **Agent Skills hosts** (Claude Code, Codex, Cursor, Copilot, Gemini CLI, +50 more) | `npx skills add mohamed-amine-ben-mallessa/mysetterbot-claw-cli -g` | Installs [`skills/instagram-cli`](skills/instagram-cli/SKILL.md) |
| **With the MCP layer** | [mysetterbot-claw](https://github.com/mohamed-amine-ben-mallessa/mysetterbot-claw) | Recommended — adds dry-run, quotas, and the free-LLM copywriting |

Two entrypoints are installed: `msbc` (branded) and `clinstagram` (compat).

## Login (one time)

```bash
msbc auth login --username <you>        # password prompted; stored in OS keychain
msbc --json doctor                      # health check
```

## The moves

```bash
# read / send DMs
msbc --json dm inbox --limit 20
msbc --json dm thread <thread_id> --limit 20
msbc --json dm send <user> "hey 👋"

# discover prospects
msbc --json user posts <username> --limit 12
msbc --json hashtag recent <tag> --limit 30
msbc --json user search "<query>"

# analytics
msbc --json analytics profile
msbc --json analytics post latest

# growth actions — LOCKED unless you opt in (read the warning below)
msbc --enable-growth-actions followers follow <user>
msbc --enable-growth-actions like post <media_id>
msbc --enable-growth-actions comments add <media_id> "nice work"
```

## ⚠️ The ban warning (read this)

`--enable-growth-actions` unlocks **follow / unfollow / like / comment**. Instagram
actively detects automation patterns (speed, volume, regularity). Misuse can get
your account **action-blocked, shadow-banned, or permanently suspended**.

- Act **slowly, sparingly, and on a human cadence**. Never loop in bulk.
- Respect the rate limits in `~/.clinstagram/config.toml` (they exist for a reason).
- Prefer **warm-up** (a like / a genuine comment) before any cold DM.
- One *personalized* message ≠ mass copy-paste. The first is outreach; the second is spam.
- Stay within Instagram's terms of service and the messaging law that applies to you.

The MCP layer ([mysetterbot-claw](https://github.com/mohamed-amine-ben-mallessa/mysetterbot-claw))
defaults to **dry-run** for exactly this reason: it shows you the draft, you approve, then it sends.

## 🩹 Known dependency bug (auto-fixed)

Reading a DM thread that contains a voice note / video-call event / some shared
media can crash upstream `instagrapi` with `list index out of range`
(`extract_direct_media` does `sorted(...)[-1]` on an empty version list — present
in 2.9.9 **and** 2.9.11). We ship a guard:

```bash
python fixups.py            # re-apply after any `pip install/upgrade instagrapi`
python fixups.py --check    # CI: exit 1 if the guard is missing
```

See [`patches/instagrapi-empty-media-versions.patch`](patches/instagrapi-empty-media-versions.patch).

## Skill, scripts & docs

For AI agents (Claude Code / Cursor / any MCP-style runner) and humans:

```
skills/instagram-cli/SKILL.md   portable agent skill (when/how to drive the CLI)
scripts/ig.py                   dependency-free wrapper: run a subcommand, get parsed JSON
ref/COMMANDS.md                 every command, args, examples, the JSON envelope
ref/SAFETY.md                   the anti-ban playbook (read before growth actions)
```

```bash
python scripts/ig.py dm inbox --limit 5
python scripts/ig.py user info <username>
```

## Exit codes

`0` success · `1` user error · `2` auth/session · `3` rate-limited · `4` API error ·
`5` challenge/2FA · `6` policy-blocked (growth gate / compliance) · `7` capability unavailable.

Predictable enough that an agent can branch on them without parsing prose.

## Credits

Fork of **[clinstagram](https://github.com/199-biotechnologies/clinstagram)** by
Boris Djordjevic / 199 Biotechnologies & Paperfoot AI — MIT. This fork adds the
MySetterBot branding, the instagrapi DM-media fix, and packaging tweaks. Not
affiliated with or endorsed by Instagram / Meta. "Instagram" is a trademark of its owner.

## License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  <sub>Built by <a href="https://github.com/mohamed-amine-ben-mallessa">Mohamed Amine Ben Mallessa</a> · ⭐ star it if your agent stopped scraping HTML</sub>
</p>
