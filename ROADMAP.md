# Roadmap

Built in evening sessions. Each phase ships something usable before the next begins.
Guiding rule: the success metric is "I actually use this for my own garden."

## ✅ Phase 1 — The Brain (CLI) — DONE June 10, 2026
- [x] Pull 7-day forecast from Open-Meteo (temps, ET₀, UV, wind, precip)
- [x] Hardcoded garden profile (3 raised beds, 9 crops) + structured crop
      heat-tolerance table
- [x] Claude API generates a Daily Garden Brief (`garden_brief.py`)

## 🔨 Phase 2 — The App (Next.js + Supabase)
- [ ] Next.js project scaffold (App Router, TypeScript)
- [ ] Supabase: `gardens`, `beds`, `crops`, `plantings` tables
      (migrate the hardcoded JSON + CROPS dict into real schema)
- [ ] Garden setup form (location, beds, crops, irrigation)
- [ ] "Today's Brief" page — server-side: fetch weather → call Claude → render
- [ ] Deploy to Vercel; add to phone home screen

## 📬 Phase 3 — The Service (automation)
- [ ] n8n workflow: 6am cron → fetch weather → generate brief → email/SMS
- [ ] Heat-wave alert trigger (forecast crosses crop stress thresholds →
      proactive warning, not just the daily brief)
- [ ] Brief history stored in Supabase (foundation for later ML)

## 🔮 Phase 4 — Smarter (the fun ML stuff)
- [ ] Planting calendar generator (zone 9a windows per crop)
- [ ] Pest/disease photo ID (vision model)
- [ ] Watering runtime math: ET₀ → minutes on the drip controller
- [ ] Multi-zone support (Phoenix, Vegas, Tucson...)

## 💰 Phase 5 — Maybe Money (only if people want it)
- [ ] Waitlist / landing page for other desert gardeners
- [ ] $4–5/mo tier: saved gardens + daily delivery
- [ ] Affiliate links for gear actually used (shade cloth, soaker hose, etc.)

## Conventions
- Secrets live in `.env` (gitignored). Never commit keys.
- Commit at the end of every session with a message describing what changed —
  the git log is the project journal.

---

## Session log

### Session 1 — June 10, 2026 ✅
Phase 1 complete in one evening:
- Wrote `garden_brief.py` (Open-Meteo + garden profile + CROPS table + Claude API)
- Created public GitHub repo (MIT, Node .gitignore), wrote README + ROADMAP
- Set up git auth (personal access token), made first commits and pushed
- Forecast validation: real 103.5°F spike detected for June 12-13 — exactly
  the kind of event this tool exists for

**Next session:** Move repo out of iCloud-synced ~/Documents (see below),
install Claude Code, run `/init`, then start Phase 2 (Next.js + Supabase).

## Need-to-knows (gotchas captured along the way)
- ⚠️ **iCloud:** repo currently in ~/Documents which syncs to iCloud. Move to
  `~/dev/` BEFORE any `npm install` — iCloud cannot handle node_modules.
- **GitHub token** (classic, repo scope) expires ~Sept 2026; keychain stores
  it until then. Regenerate when pushes start failing, or switch to `gh` CLI.
- **Mac Python:** always `python3` / `pip3`.
- **Terminal habit:** paste one command at a time — stacked pastes get
  swallowed by interactive prompts (learned via the git username incident).
- **Browser quirk:** .py files may refuse to download from chat; rename
  .py.txt workaround exists but won't matter once Claude Code edits files
  directly.
