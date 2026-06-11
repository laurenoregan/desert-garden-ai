"""
Desert Garden AI — Evening 1: The Brain
========================================
Pulls a real 7-day forecast for St. George, UT from Open-Meteo (free, no API key),
combines it with your garden profile, and asks Claude to write a daily care brief.

Setup (one time):
    pip install requests anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."   # from console.anthropic.com

Run:
    python garden_brief.py              # full run: weather -> Claude -> brief
    python garden_brief.py --dry-run    # no API key needed: prints the data + prompt
"""

import json
import os
import sys
from datetime import date

import requests

# ---------------------------------------------------------------------------
# 1. YOUR GARDEN PROFILE (v0.1: hardcoded — moves to Supabase in Evening 2)
# ---------------------------------------------------------------------------

GARDEN = {
    "location": {"name": "St. George, UT", "lat": 37.0965, "lon": -113.5684},
    "irrigation": "Soaker hose drip on Hunter X2 controller",
    "beds": [
        {
            "name": "Green bed 1 (Permade 8x2x1 ft)",
            "crops": ["zucchini", "yellow squash"],
        },
        {
            "name": "Green bed 2 (Permade 8x2x1 ft)",
            "crops": ["cucumber", "basil", "parsley"],
        },
        {
            "name": "Tan bed (Land Guard 8x4x2 ft)",
            "crops": ["green pepper", "jalapeno", "rosemary", "sweet potato"],
        },
    ],
}

# Structured crop knowledge — the "secret sauce" that keeps advice consistent.
# heat_stress_f: daytime high where the plant starts suffering
# notes: what actually happens + what to do about it
CROPS = {
    "zucchini":     {"heat_stress_f": 100, "water": "high",   "notes": "Flowers drop / pollination fails over 100F. Morning deep water; afternoon shade cloth helps fruit set."},
    "yellow squash":{"heat_stress_f": 100, "water": "high",   "notes": "Same as zucchini. Watch for sunscald on exposed fruit."},
    "cucumber":     {"heat_stress_f": 95,  "water": "high",   "notes": "Bitter fruit + blossom drop when heat-stressed. Most heat-sensitive crop in the garden. 30-40% shade cloth over 100F."},
    "basil":        {"heat_stress_f": 105, "water": "medium", "notes": "Loves heat but bolts fast. Pinch flower spikes weekly in summer."},
    "parsley":      {"heat_stress_f": 90,  "water": "medium", "notes": "Cool-season herb. Will bolt/sulk in desert summer; needs afternoon shade to survive at all."},
    "green pepper": {"heat_stress_f": 95,  "water": "medium", "notes": "Blossom drop above 95F. Fruit already set is fine; new flowers will abort during a heat wave."},
    "jalapeno":     {"heat_stress_f": 100, "water": "medium", "notes": "Tougher than bells. Heat stress = hotter peppers but fewer of them."},
    "rosemary":     {"heat_stress_f": 115, "water": "low",    "notes": "Desert-proof. Biggest risk is overwatering it on a schedule built for the vegetables."},
    "sweet potato": {"heat_stress_f": 110, "water": "medium", "notes": "Thrives in heat. Vines wilt midday and recover by evening — that's normal, don't panic-water."},
}

# ---------------------------------------------------------------------------
# 2. WEATHER (Open-Meteo — free, no key, includes ET0 evapotranspiration)
# ---------------------------------------------------------------------------

def fetch_forecast(lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "et0_fao_evapotranspiration",   # mm of water plants lose per day
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "uv_index_max",
        ]),
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "America/Denver",
        "forecast_days": 7,
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def summarize_forecast(raw: dict) -> list[dict]:
    """Reshape Open-Meteo's column format into a list of day dicts."""
    d = raw["daily"]
    days = []
    for i, day in enumerate(d["time"]):
        days.append({
            "date": day,
            "high_f": d["temperature_2m_max"][i],
            "low_f": d["temperature_2m_min"][i],
            "et0_mm": d["et0_fao_evapotranspiration"][i],
            "precip_pct": d["precipitation_probability_max"][i],
            "wind_mph": d["wind_speed_10m_max"][i],
            "uv_max": d["uv_index_max"][i],
        })
    return days

# ---------------------------------------------------------------------------
# 3. THE PROMPT
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a desert gardening expert for the Mojave/high-desert
Southwest (St. George, UT — hot, arid, intense UV, drip irrigation on raised beds).

You will receive: (1) a garden profile with beds and crops, (2) structured crop
heat-tolerance data, and (3) a 7-day forecast including ET0 evapotranspiration.

Write a 'Daily Garden Brief' with:
1. HEADLINE — one sentence on the week's main weather story.
2. WATERING — concrete guidance for the drip system (when, how deep, any
   schedule changes), driven by the ET0 numbers and temperatures.
3. PER-BED ACTIONS — for each bed, only the crops that need attention this
   week, with specific actions and the day to do them. Skip crops that are fine.
4. ONE THING TONIGHT — the single most useful 10-minute task for this evening.

Be specific and practical, not generic. Reference actual forecast days and
temperatures. Total length: under 350 words."""


def build_user_prompt(garden: dict, crops: dict, days: list[dict]) -> str:
    return (
        f"Today is {date.today().isoformat()}.\n\n"
        f"GARDEN PROFILE:\n{json.dumps(garden, indent=2)}\n\n"
        f"CROP DATA:\n{json.dumps(crops, indent=2)}\n\n"
        f"7-DAY FORECAST:\n{json.dumps(days, indent=2)}\n\n"
        "Write today's Daily Garden Brief."
    )

# ---------------------------------------------------------------------------
# 4. CLAUDE
# ---------------------------------------------------------------------------

def generate_brief(user_prompt: str) -> str:
    import anthropic  # imported here so --dry-run works without the package
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return msg.content[0].text

# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    dry_run = "--dry-run" in sys.argv

    loc = GARDEN["location"]
    print(f"Fetching 7-day forecast for {loc['name']}...")
    raw = fetch_forecast(loc["lat"], loc["lon"])
    days = summarize_forecast(raw)

    print("\n--- FORECAST ---")
    for d in days:
        print(
            f"{d['date']}: high {d['high_f']}F / low {d['low_f']}F | "
            f"ET0 {d['et0_mm']} mm | precip {d['precip_pct']}% | "
            f"wind {d['wind_mph']} mph | UV {d['uv_max']}"
        )

    user_prompt = build_user_prompt(GARDEN, CROPS, days)

    if dry_run:
        print("\n--- PROMPT THAT WOULD BE SENT TO CLAUDE ---")
        print(user_prompt)
        print("\n(dry run: set ANTHROPIC_API_KEY and rerun without --dry-run)")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Try --dry-run first, or export the key.")

    print("\nGenerating brief with Claude...")
    print("\n" + "=" * 60)
    print("        TODAY'S GARDEN BRIEF — " + loc["name"])
    print("=" * 60 + "\n")
    print(generate_brief(user_prompt))


if __name__ == "__main__":
    main()
