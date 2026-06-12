---
name: instagram-cli
description: >
  Drive Instagram from the command line for AI agents — read/send DMs, prospect
  (user/hashtag search, profiles, posts), comment, follow, like, post, stories,
  analytics. JSON in, JSON out. Use when the user wants to interact with Instagram
  programmatically: send a DM, read a conversation, find accounts, comment on a
  post, check a profile, post content. Keywords: instagram, DM, direct message,
  outreach, follow, like, comment, hashtag, story, instagram automation, msbc,
  clinstagram.
license: MIT
---

# Instagram CLI (MySetterBot Claw)

A JSON-clean Instagram CLI. Entrypoints: `msbc` (branded) or `clinstagram` (compat).
The login session lives in the OS keychain — you never handle the password.

## First, orient yourself
```bash
msbc --json doctor          # is the session healthy?
msbc --json auth status     # which backends are configured
msbc --json agent-info      # full machine-readable command manifest
```

## Core moves (global flags go BEFORE the subcommand)
```bash
# DMs
msbc --json dm inbox --limit 20
msbc --json dm thread <thread_id> --limit 20
msbc --json dm send <user> "your message"

# prospecting (read-only, safe)
msbc --json user info <username>
msbc --json user posts <username> --limit 12
msbc --json hashtag recent <tag> --limit 30
msbc --json user search "<query>"

# analytics
msbc --json analytics profile
msbc --json analytics post latest
```

## Growth actions — gated for safety
Follow / unfollow / like / comment need `--enable-growth-actions`:
```bash
msbc --enable-growth-actions --json like post <media_id>
msbc --enable-growth-actions --json comments add <media_id> "nice work"
```

## ⚠️ Anti-ban (non-negotiable)
Instagram detects automation. **Be human:** personalized, sparse, slow. Never loop
in bulk. Stop on exit code `3` (rate-limited) or `6` (policy-blocked). See
[ref/SAFETY.md](../../ref/SAFETY.md). For orchestrated outreach with dry-run +
quotas, use the **mysetterbot-claw MCP** instead of raw loops.

## Exit codes
`0` ok · `1` user error · `2` session expired (`msbc auth login`) · `3` rate-limited ·
`4` API error · `5` 2FA/challenge · `6` policy-blocked · `7` capability unavailable.

## Reference
- [ref/COMMANDS.md](../../ref/COMMANDS.md) — every command, args, examples
- [ref/SAFETY.md](../../ref/SAFETY.md) — anti-ban rules
- Helper: [scripts/ig.py](../../scripts/ig.py) — thin Python wrapper returning parsed JSON
