# CLAUDE.md — Desert Garden AI

## What this project is
An AI-powered garden assistant for high-heat desert climates (built in
St. George, UT — zone 9a, 100-115°F summers). It combines a live Open-Meteo
forecast (including ET₀ evapotranspiration) with a structured garden profile
and crop heat-tolerance data, then uses the Claude API to generate a daily
care brief. See README.md for architecture and ROADMAP.md for the phased plan.

## Who's building it and why
Lauren — AI analyst transitioning to AI engineer. This is an evening passion
project with three goals, in priority order: (1) fun and learning,
(2) long-term passive income potential, (3) portfolio/resume value.
She is also user #1: the garden profile in the code is her real garden.
Success metric: "I actually use this instead of asking an AI chat about my squash."

## Working style — important
- Built in short evening sessions (1-2 hours). Prefer small shippable steps
  over big refactors. Always leave the repo in a working state.
- Lauren is learning as she goes: explain what you're doing and why in plain
  language as you work. Don't assume deep terminal/git fluency yet.
- Run commands one at a time; flag anything destructive before doing it.
- End every session by committing with a clear message — the git log is the
  project journal — and suggesting the next session's starting point.

## Current state (end of session 1, June 10, 2026)
- `garden_brief.py` works: fetches 7-day St. George forecast from Open-Meteo,
  combines with hardcoded garden profile + CROPS dict, generates a brief via
  Claude API. Has a `--dry-run` mode that needs no API key.
- Repo is public on GitHub (laurenoregan/desert-garden-ai), MIT licensed,
  Node .gitignore.
- Next up: Phase 2 in ROADMAP.md — Next.js app + Supabase schema.

## Stack decisions (already made — don't relitigate)
- Next.js (App Router, TypeScript) on Vercel free tier
- Supabase free tier for garden profiles
- Open-Meteo for weather (free, no key; ET₀ is the differentiator)
- Claude API (claude-sonnet-4-5) for brief generation
- n8n later for the 6am automated delivery (Phase 3)
- Crop knowledge stays STRUCTURED DATA (tables), not LLM freestyle —
  consistency now, ML features later

## Environment gotchas (learned the hard way)
- The project currently lives in ~/Documents, which is iCloud-synced.
  BEFORE running `npx create-next-app` or any `npm install`, move the repo to
  a non-synced folder (e.g. ~/dev/desert-garden-ai) — iCloud chokes on
  node_modules. Update the remote nothing; a plain `mv` works, git config
  travels with the folder.
- Mac uses `python3` / `pip3`, not `python` / `pip`.
- GitHub auth uses a personal access token (classic, repo scope), stored in
  keychain, expires ~Sept 2026. If a push suddenly fails with auth errors
  around then, the token expired — regenerate at GitHub → Settings →
  Developer settings. Consider switching to `gh auth login` at that point.
- ANTHROPIC_API_KEY lives in the shell environment / .env only. Never commit
  keys; .gitignore already covers .env files.

## Commands
- `python3 garden_brief.py --dry-run` — test the data pipeline, no key needed
- `python3 garden_brief.py` — generate today's real brief (needs ANTHROPIC_API_KEY)
