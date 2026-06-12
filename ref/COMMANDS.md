# MySetterBot Claw CLI — command reference

The CLI speaks JSON. Put global flags **before** the subcommand. Two entrypoints
are equivalent: `msbc` (branded) and `clinstagram` (compat). Examples use `msbc`.

```
msbc [--json] [--account NAME] [--backend auto|graph_ig|graph_fb|private]
     [--enable-growth-actions] [--dry-run] [--proxy URL]  <command> [args]
```

## JSON envelope

Every `--json` call returns one of:

```jsonc
// success
{ "exit_code": 0, "data": <any>, "backend_used": "private" | "graph_ig" | null }
// error
{ "exit_code": 4, "error": "…", "remediation": "…", "retry_after": 30 }
```

## Exit codes

| code | meaning | what to do |
|---|---|---|
| 0 | success | — |
| 1 | user error | fix arguments |
| 2 | auth error / session expired | `msbc auth login` |
| 3 | rate-limited | back off, respect quotas, retry later |
| 4 | API error (transient) | retry with backoff |
| 5 | challenge / 2FA | log in interactively once |
| 6 | policy-blocked (growth gate / compliance) | needs `--enable-growth-actions` |
| 7 | capability unavailable on this backend | omit `--backend` (let it auto-pick) |

## Auth

```bash
msbc auth login --username <you>     # password prompted; stored in OS keychain
msbc --json auth status              # which backends are configured
msbc --json doctor                   # full health check (add --deep for live probes)
msbc auth logout --yes               # clear stored session for the account
```

## Read / prospect

```bash
msbc --json dm inbox --limit 20 [--unread]
msbc --json dm thread <thread_id> --limit 20
msbc --json dm search "<keyword>"
msbc --json user info <username>
msbc --json user search "<query>"
msbc --json user posts <username> --limit 12
msbc --json hashtag recent <tag> --limit 30      # tag without '#'
msbc --json hashtag top <tag> --limit 30
msbc --json comments list <media_id> --limit 50
msbc --json followers list --limit 50
msbc --json followers following --limit 50
msbc --json analytics profile
msbc --json analytics post latest        # or a media_id
msbc --json analytics hashtag <tag>
msbc --json media download <id|shortcode|url> --output <dir>
```

## Send (DMs — not growth-gated)

```bash
msbc --json dm send <user> "message text"
msbc --json dm send-media <user> <path|url>
```

## Posting

```bash
msbc --json post photo <path|url> --caption "…"
msbc --json post video <path|url> --caption "…" --thumbnail <path>
msbc --json post reel  <path|url> --caption "…"
msbc --json post carousel <p1> <p2> … --caption "…"
msbc --json story post-photo <path|url> [--link URL] [--mention user]
msbc --json story list [user]
msbc --json story viewers <story_id>
```

## Growth actions — REQUIRE `--enable-growth-actions`

```bash
msbc --enable-growth-actions --json followers follow <user>
msbc --enable-growth-actions --json followers unfollow <user>
msbc --enable-growth-actions --json like post <media_id>
msbc --enable-growth-actions --json like undo <media_id>
msbc --enable-growth-actions --json comments add <media_id> "text"
msbc --enable-growth-actions --json comments reply <comment_id> "text"
```

See [SAFETY.md](SAFETY.md) before using any of these.

## Discover everything programmatically

```bash
msbc --json agent-info        # full machine-readable manifest: commands, args, exit codes, backends
```
