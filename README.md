# 🌵 Desert Garden AI

AI-powered garden assistant for high-heat desert climates. Generates daily care
briefs from real weather data — built and battle-tested in St. George, UT
(zone 9a, 110°F summers, no mercy).

## Why

Generic gardening apps give generic advice. They don't know that your cucumbers
go bitter above 95°F, that a three-day heat spike means deep-watering *tonight*,
or that your parsley is on borrowed time the moment June arrives. This project
combines live forecast data (including ET₀ evapotranspiration — the actual
water-loss rate of your plants) with structured crop knowledge and an LLM to
produce specific, actionable daily guidance for a real garden.

## How it works

```
Open-Meteo API ──┐
 (7-day forecast,│
  ET₀, UV, wind) ├──► structured prompt ──► Claude API ──► Daily Garden Brief
                 │
Garden profile ──┘
 (beds, crops,
  heat tolerances)
```

1. **Weather** — pulled from [Open-Meteo](https://open-meteo.com) (free, no key),
   including `et0_fao_evapotranspiration`, the secret weapon for desert watering math.
2. **Garden profile** — beds, crops, and irrigation setup, plus a structured
   crop table with heat-stress thresholds and care notes.
3. **Claude** — synthesizes both into a brief: weekly headline, watering plan,
   per-bed actions, and one 10-minute task for tonight.

## Quick start

```bash
pip install requests anthropic
python garden_brief.py --dry-run        # no API key needed; shows data + prompt
export ANTHROPIC_API_KEY="sk-ant-..."   # from console.anthropic.com
python garden_brief.py                  # generates today's brief (~1¢/run)
```

## Roadmap

See [ROADMAP.md](ROADMAP.md). Short version: CLI script → Next.js app on
Vercel with Supabase profiles → automated 6am brief delivery via n8n →
planting calendars, pest photo ID, and multi-zone support.

## Status

🌱 v0.1 — the brain works. The app is sprouting.

## License

MIT
