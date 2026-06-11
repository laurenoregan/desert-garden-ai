# Roadmap

Built in evening sessions. Each phase ships something usable before the next begins.
Guiding rule: the success metric is "I actually use this for my own garden."

## ✅ Phase 1 — The Brain (CLI)
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
