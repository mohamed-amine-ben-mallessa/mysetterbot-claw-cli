# Safety & anti-ban guide

Instagram aggressively detects automation. A careless script can get an account
**action-blocked, shadow-banned, or permanently disabled**. Read this once.

## The golden rules

1. **Be a human.** Personalized, sparse, on a human cadence. One thoughtful DM is
   outreach; a hundred identical ones is spam — and spam is how accounts die.
2. **Growth actions are locked for a reason.** Follow / unfollow / like / comment
   require `--enable-growth-actions`. That gate is a feature, not an obstacle.
3. **Warm up before you DM.** A genuine like or comment first reads far more human
   than a cold message out of nowhere.
4. **Respect rate limits.** Defaults live in `~/.clinstagram/config.toml`:

   | limit | default |
   |---|---|
   | `private_dm_per_hour` | 30 |
   | `graph_dm_per_hour` | 200 |
   | `private_likes_per_hour` | 20 |
   | `private_follows_per_day` | 20 |
   | `request_delay_min` / `max` | 2s / 5s |

5. **Never loop in bulk.** No "for user in 500 users: dm(...)". Spread actions
   across hours and days, with jitter.
6. **Stop on signals.** If you get exit code `3` (rate-limited) or `6`
   (policy-blocked), STOP — don't hammer. Back off for hours, not seconds.

## A new account is fragile

Fresh accounts and accounts with little history get limited fastest. Ramp up slowly
over days. Post real content. Have real conversations.

## Prefer the MCP for orchestration

[mysetterbot-claw](https://github.com/mohamed-amine-ben-mallessa/mysetterbot-claw)
wraps this CLI and adds **dry-run by default**, **per-action daily quotas**, and a
**minimum cooldown between writes** — so the bot shows you the draft, you approve,
then it sends. If you're automating, automate through the MCP, not raw loops.

## Credentials

The session lives in your **OS keychain**, never in a file or `.env`. The raw
password is never stored. If a session expires (`exit_code: 2`), re-run
`msbc auth login`.
