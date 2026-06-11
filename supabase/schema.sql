-- Desert Garden AI schema
-- Run this in the Supabase SQL editor (supabase.com → your project → SQL Editor)

-- Master crop knowledge table (mirrors the CROPS dict in garden_brief.py)
create table crops (
  id            serial primary key,
  slug          text unique not null,           -- e.g. "zucchini"
  name          text not null,                  -- display name
  water         text not null check (water in ('low', 'medium', 'high')),
  heat_stress_f integer not null,               -- °F where plant starts suffering
  notes         text not null
);

-- One row per garden (one user can have multiple gardens eventually)
create table gardens (
  id            serial primary key,
  name          text not null,
  lat           numeric(9,6) not null,
  lon           numeric(9,6) not null,
  location_name text not null,                  -- human-readable, e.g. "St. George, UT"
  irrigation    text,                           -- e.g. "Soaker hose drip on Hunter X2"
  created_at    timestamptz default now()
);

-- Raised beds belong to a garden
create table beds (
  id         serial primary key,
  garden_id  integer references gardens(id) on delete cascade,
  name       text not null,                     -- e.g. "Green bed 1 (Permade 8x2x1 ft)"
  sort_order integer default 0
);

-- What's planted where right now
create table plantings (
  id         serial primary key,
  bed_id     integer references beds(id) on delete cascade,
  crop_id    integer references crops(id),
  planted_at date,
  notes      text                               -- optional per-planting notes
);

-- ---------------------------------------------------------------------------
-- Seed data — Lauren's garden as of June 2026
-- ---------------------------------------------------------------------------

insert into crops (slug, name, water, heat_stress_f, notes) values
  ('zucchini',     'Zucchini',      'high',   100, 'Flowers drop / pollination fails over 100F. Morning deep water; afternoon shade cloth helps fruit set.'),
  ('yellow-squash','Yellow Squash', 'high',   100, 'Same as zucchini. Watch for sunscald on exposed fruit.'),
  ('cucumber',     'Cucumber',      'high',    95, 'Bitter fruit + blossom drop when heat-stressed. Most heat-sensitive crop in the garden. 30-40% shade cloth over 100F.'),
  ('basil',        'Basil',         'medium', 105, 'Loves heat but bolts fast. Pinch flower spikes weekly in summer.'),
  ('parsley',      'Parsley',       'medium',  90, 'Cool-season herb. Will bolt/sulk in desert summer; needs afternoon shade to survive at all.'),
  ('green-pepper', 'Green Pepper',  'medium',  95, 'Blossom drop above 95F. Fruit already set is fine; new flowers will abort during a heat wave.'),
  ('jalapeno',     'Jalapeño',      'medium', 100, 'Tougher than bells. Heat stress = hotter peppers but fewer of them.'),
  ('rosemary',     'Rosemary',      'low',    115, 'Desert-proof. Biggest risk is overwatering it on a schedule built for the vegetables.'),
  ('sweet-potato', 'Sweet Potato',  'medium', 110, 'Thrives in heat. Vines wilt midday and recover by evening — that''s normal, don''t panic-water.');

insert into gardens (name, lat, lon, location_name, irrigation) values
  ('Desert Garden', 37.096500, -113.568400, 'St. George, UT', 'Soaker hose drip on Hunter X2 controller');

insert into beds (garden_id, name, sort_order) values
  (1, 'Green bed 1 (Permade 8x2x1 ft)', 1),
  (1, 'Green bed 2 (Permade 8x2x1 ft)', 2),
  (1, 'Tan bed (Land Guard 8x4x2 ft)',   3);

insert into plantings (bed_id, crop_id) values
  -- Green bed 1: zucchini, yellow squash
  (1, (select id from crops where slug = 'zucchini')),
  (1, (select id from crops where slug = 'yellow-squash')),
  -- Green bed 2: cucumber, basil, parsley
  (2, (select id from crops where slug = 'cucumber')),
  (2, (select id from crops where slug = 'basil')),
  (2, (select id from crops where slug = 'parsley')),
  -- Tan bed: green pepper, jalapeno, rosemary, sweet potato
  (3, (select id from crops where slug = 'green-pepper')),
  (3, (select id from crops where slug = 'jalapeno')),
  (3, (select id from crops where slug = 'rosemary')),
  (3, (select id from crops where slug = 'sweet-potato'));
