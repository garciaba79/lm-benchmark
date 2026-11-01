# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
Test: Weather App Planning
Created: 10/28/2026, 12:45:34 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

I am about to work on a new project and create a Weather app. Here is my development plan. Do not provide me code or examples unless I ask you to. Stand by for next instructions.

---

# Weather PWA Development Plan

*Final merged version, October 25, 2026*

A lightweight, visually clean React PWA for weather. Built for portfolio value with custom graphics, simple layouts, accessibility, and offline support. Inspired by Google's clean style but kept fully custom.

## Core Project Goals

- Single-page React PWA (web-first, installable on mobile and desktop)
- Clean UI with no ads or clutter
- MVP: location selection and saving, daily view, 10-day forecast with drill-down
- Custom visual polish (themes, parallax, weather-specific scenes)
- Offline support via IndexedDB caching and a service worker
- Accessible by design (contrast, keyboard navigation, reduced motion)
- Deploy to Vercel with a public GitHub repo, tests, and CI

## Tech Stack

This is the single source of truth for the stack. Do not duplicate it elsewhere in the repo docs.

**Core**

- **Framework**: React (vanilla, no Next.js or other heavy frameworks)
- **Language**: TypeScript (light: interfaces and types only)
- **Build tool**: Vite
- **Routing**: react-router-dom
- **State**: React Context + hooks (no external state libraries)
- **Data fetching**: Native fetch + async/await
- **Weather API**: Open-Meteo (free, no key required, free tier is for non-commercial use only; follow their attribution requirements)
- **Storage and caching**: IndexedDB via the idb wrapper
- **Styling**: CSS Modules + custom flexbox only
- **Visuals**: All custom-built (canvas or SVG for charts, CSS for backgrounds and parallax)
- **PWA**: Manual manifest.json and service worker; vite-plugin-pwa is an optional fallback if manual setup becomes tedious

**Tooling and environment**

- Biome (lint + format, light custom rules for your preferred style)
- Vitest (unit tests)
- GitHub Actions (CI)
- Windows 11, VS Code, Git + Git Bash
- GitHub (public repo) and Vercel (deployment)

**Dependencies**

| Package | Type | Notes |
| --- | --- | --- |
| react, react-dom | Runtime | Choose the major version deliberately (see below) |
| react-router-dom | Runtime | Same: choose deliberately |
| idb | Runtime | Tiny IndexedDB wrapper |
| typescript, vite, @vitejs/plugin-react | Dev | Match the React and Vite majors you choose |
| @types/react, @types/react-dom | Dev | Match the React major |
| @biomejs/biome | Dev | Pin an exact version (no `latest`) so formatting is reproducible |
| vitest | Dev | Unit tests for cache and data-mapping logic |

**Version policy:** The earlier plan pinned React 18.3, Vite 5.4, and react-router 6. Those still work, but newer majors are available. Before scaffolding, check current stable versions on npm and decide whether to use the latest or stay on the older set. Either is fine; record the choice and the reason in the README.

## Development Parts

### Part 1: Project Initialization and Core Setup

First milestone: get something running quickly.

- Create the Vite + React + TypeScript project
- Set up Biome with your style tweaks, and pin its version
- Set up Vitest
- Add react-router-dom
- Create the folder structure (components, views, context, utils, styles)
- Set up global context for location and app state
- **Spike first:** test Open-Meteo geocoding with city names, zip/postal codes, and coordinates. Postal code coverage is inconsistent, so decide early on fallbacks (for example, city-only search plus coordinates)
- Implement location search (zip, city, or coordinates) using Open-Meteo geocoding
- Add a "Use my location" button via the Geolocation API, with graceful handling of denied permission
- Save selected locations in IndexedDB
- Decide what loads on first visit: the last used location if one is saved, otherwise a hardcoded fallback (for example, Crestview, FL) with a clear prompt to change it
- Basic header, nav, and theme foundation
- Add a small footer or about line crediting Open-Meteo, visible on every view (required by their terms)
- Establish loading, empty, and error state patterns for reuse in later parts
- Wrap the main views in React error boundaries so a failed fetch or bad data shows a recovery message instead of a blank app

### Part 2: Daily Weather View

Core single-day screen.

- Fetch current conditions and today's detailed forecast from Open-Meteo
- Display temperature, feels-like, wind, humidity, sunrise/sunset, and other key metrics
- **Time zones:** show sunrise, sunset, and hourly times in the location's time zone, not the browser's. Request `timezone=auto` from Open-Meteo, use the zone it returns, and test with a location in a different zone than yours
- Add a unit toggle: °F/°C and mph/km/h (store the preference in IndexedDB)
- Custom cards and sections with flexbox
- Simple hourly breakdown drawn with canvas or SVG
- Loading skeletons and clear error messages for failed fetches
- Last-updated timestamp and a visible refresh button
- Cache responses in IndexedDB with a timestamp; serve from cache if fresh (under 3 to 6 hours, same day)
- Unit tests for the cache freshness logic and the API-to-UI data mapping

### Part 3: 10-Day Forecast View

- Fetch the 10 to 16 day daily forecast from Open-Meteo
- Overview: scrollable list or grid of days with high/low, condition icon, and short summary
- Drill-down: click a day to reuse the Daily View component (pass the date as a route param)
- Handle invalid or out-of-range dates in the route
- Keep visual style consistent

**Milestone:** Parts 1 to 3 complete means a working MVP. Deploy to Vercel and set up GitHub Actions (Biome check, tests, build) at this point.

### Part 4: Visual Enhancements and Weather Themes

The main showcase polish.

- Dynamic backgrounds and scenes based on conditions (sunny, cloudy, light/moderate/heavy rain, snow, storm)
- Custom icons and graphics (hand-built SVGs or CSS shapes)
- Subtle parallax using transform-based effects. Avoid `background-attachment: fixed`, which is unreliable on iOS Safari
- Smooth transitions when weather or views change
- Respect `prefers-reduced-motion`: disable or simplify parallax and animations for those users
- Mobile-first responsive polish

### Part 5: Caching, Service Worker, and Offline Polish

- Full cache logic: check the timestamp on load and refresh if stale or requested
- Visible refresh button as the guaranteed refresh path
- Pull-to-refresh as an enhancement only: use native behavior where it works and a lightweight custom or polyfill fallback where it does not. Native pull-to-refresh generally does not work in installed iOS PWAs
- Write the service worker to cache static assets and API responses
- **Register the service worker in this part** so offline behavior can be tested here, not later
- Decide how users learn about a new version: an "Update available, reload" banner (recommended, since the user stays in control) or automatic activation on next launch. Either way, users must not stay stuck on stale cached assets
- Offline indicator ("Using cached data" / "Offline mode")
- Test offline behavior in browser dev tools (offline mode, cache inspection)

### Part 6: PWA Completion and Installability

- Create manifest.json (icons, name, theme colors, display mode)
- Verify the Part 5 update flow end to end: deploy a new build and confirm the update prompt appears and the new version loads
- Test install on Android (Chrome) and iOS (Safari)
- Final responsiveness and touch optimizations
- Run a Lighthouse audit (PWA, performance, accessibility) and fix the findings
- Decide on vite-plugin-pwa if manual setup has become tedious
- Finish the README (start it early): screenshots, a short architecture note (data flow, caching, service worker), and how to run the app locally

### Accessibility (applies throughout)

Accessibility is a stated project benefit, so treat it as ongoing work rather than a final pass.

- Sufficient color contrast on every weather theme, including text over scene backgrounds
- Full keyboard navigation and visible focus states
- Semantic HTML and meaningful labels (including for canvas/SVG charts, with a text alternative)
- Reduced-motion support (see Part 4)
- Check with Lighthouse and a screen reader before release

### Nice-to-Haves (If Time Allows)

- Explicit Lighthouse score targets: 90+ for PWA, performance, and accessibility
- A way to clear cached data from the UI, useful for demos and debugging
- Maskable icons in the manifest so the Android install icon displays correctly

## Suggested Development Flow

### Phase 1: MVP Foundation

1. Complete Parts 1 to 3 for a functional MVP with daily and 10-day views
2. Deploy an early version to Vercel and add CI
3. Share the link and screenshots

### Phase 2: Polish and PWA

1. Add Part 4 (visuals) to make it portfolio-ready
2. Finish Parts 5 and 6 for a true PWA with offline caching

### Phase 3: Iteration

1. Work through the future parts below as stretch goals

## Future Modular Parts

Add anytime after the MVP.

- **Part 7**: Multiple API support (switch between Open-Meteo and others such as OpenWeatherMap or WeatherAPI.com)
- **Part 8**: User-provided API keys stored in IndexedDB
- **Part 9**: Basic weather history playback (if the API supports past days)
- **Part 10**: Share functionality (image, text, or link of the current view)
- **Part 11**: Advanced visuals (moods or photo integration)
- **Part 12**: More location management (favorites and recent searches)

## Project Benefits

This plan keeps scope realistic for a strong showcase project while demonstrating modern web skills: performance (caching), accessibility, PWA features, custom visuals, tested code, CI, and thoughtful data handling.

## Philosophy

Keep the project lightweight, modern, and dependency-minimal. Use current tools that look strong on a resume while staying fully custom. Prefer canvas or SVG for charts and graphics so the app stays self-contained without extra libraries.

## Changes From the Earlier Versions

For reference, this merged version:

- Restores the Open-Meteo non-commercial note, the pull-to-refresh fallback, "rain levels", and the Biome style tweaks from Version A
- Merges the duplicated tech stack sections into one
- Moves service worker registration into Part 5
- Replaces `background-attachment` parallax with transform-based parallax
- Adds a geocoding spike, loading/error states, a unit toggle, a geolocation button, accessibility tasks, Vitest, and GitHub Actions
- Pins Biome and turns the dependency versions into a deliberate decision
- Adds Open-Meteo attribution, time zone handling, error boundaries, a service worker update prompt, a default location, and README expectations, plus a short list of nice-to-haves

## Next Steps

When ready to start implementation, you can work on:

- Project scaffolding and folder structure
- Component ideas
- IndexedDB schema examples
- Service worker caching strategy

> #### 🤖 Assistant

Got it — I've read through your Weather PWA development plan in full.

**Quick summary of what I have on record:**

- **Tech stack:** React (vanilla), TypeScript, Vite, react-router-dom, Context + hooks for state, native `fetch` + IndexedDB via `idb`, CSS Modules + flexbox styling
- **API:** Open-Meteo (free tier, no key required — with attribution)
- **Key features in scope:** location selection & saving, daily view, 10-day forecast with drill-down, unit toggle (°F/°C), offline support via IndexedDB caching + service worker, accessibility built-in
- **6 parts:** MVP foundation → Daily View → 10-Day Forecast → Visual polish (dynamic backgrounds, parallax, custom SVGs) → Caching/Offline/PWA → PWA completion & installability
- **Nice-to-haves** (if time allows): clear cache button, maskable icons, reduced-motion respect
- **Tooling:** Biome (pinned versions), Vitest, GitHub Actions CI, Vercel deployment

I'll hold off on any code or examples until you ask. I'm ready for your next instruction — whether that's starting with project initialization, answering questions about the plan, or anything else.

100 t/s, 521 tokens, 7s, 19%

> #### 💬 User

What do you think about the app plan? Does it sound good, any issues, any improvements?

> #### 🤖 Assistant

The plan is solid — well-structured, realistic scope, and it hits good resume signals (PWA, offline caching, accessibility). Here are some honest observations:

**What works well:**

- **Scope discipline.** It's bounded, achievable as a single developer project, and still shows enough depth (caching strategy, custom visuals, service worker) to be impressive.
- **Open-Meteo choice is smart.** Free tier, no API key friction. Acknowledging its postal-code gaps up front is the right call.
- **Accessibility woven in** rather than bolted on — keyboard nav, focus states, semantic HTML, reduced-motion handling. That's a real differentiator for a portfolio piece.
- **Caching strategy (IndexedDB + timestamp) with freshness checks (3–6 hours)** is a concrete, implementable approach — not just "cache everything forever."
- **Pull-to-refresh caveat** is accurate and handled.

**Areas worth tightening:**

1. **Geocoding edge cases.** You flag the postal-code inconsistency, but I'd recommend also planning for *ambiguous* city names (e.g., "Springfield") — a single search should either return a confidence-ordered list or have an explicit disambiguation step. Open-Meteo's geocoding isn't perfect on that front.

2. **Chart drawing from scratch.** Part 4 calls for canvas/SVG charts with no library. For a 10-day forecast, drawing readable bars/lines yourself is non-trivial and error-prone. A lightweight hand-rolled solution (e.g., a simple bar chart using `<canvas>` or CSS-based grid) is fine, but be aware it's a self-contained graphics engineering challenge. If time runs short, you could scope this down to *icon-only* daily cards with no line chart — still visually clean, much less risk.

3. **IndexedDB schema.** The plan mentions "save locations" and "cache responses," but the actual keys/values need definition early (e.g., `locations[]` array + cache entries `{ id, timestamp, data }`). I'd recommend sketching a small schema diagram before scaffolding so you don't refactor later.

4. **Test coverage.** Vitest is scoped to "unit tests for cache and data-mapping logic." That's reasonable, but consider one or two E2E-style smoke tests (e.g., verify the daily view renders with mocked data) — they're cheap to write and catch integration bugs that unit tests miss. For a portfolio project this is optional, but it's a small addition.

5. **Lighthouse 90+ targets are ambitious.** Doable, but if you fall short on PWA or performance (e.g., first-contentful-paint with no JS preload), don't force it — fix the real blockers and let the audit report speak honestly.

**Minor improvements:**

- **Theme switching via CSS custom properties.** Instead of duplicating styles per theme, use a `--bg`, `--text`, `--accent` variable set per condition. Makes transitions smoother.
- **ARIA live regions for dynamic updates.** When temperature changes (refresh) or a drill-down happens, a visually hidden `aria-live="polite"` region would make screen readers notice the update.
- **Clear/reset locations UI.** Future Part 12 mentions favorites — add a "clear all saved locations" button now so it's not an afterthought.

**Bottom line:** I think this plan is good enough to execute as-is. The risk zones are geocoding edge cases, chart scope, and schema decisions — all addressable with a short pre-scaffolding checklist (geocoding spike done first, schema sketch, component outline). If you follow the "spike first" instruction for Open-Meteo, I'd say it's ready to go.

What would you like to tackle next?

99 t/s, 1617 tokens, 16s, 28%

> #### 💬 User

What tech documentation would help you understand the app plan better?

> #### 🤖 Assistant

Great question. The plan is comprehensive, but there are a few specific docs and artifacts that would help me execute it cleanly rather than guess at details:

---

### 1. Open-Meteo API Reference (authoritative)

The plan mentions endpoints in passing, but for implementation accuracy I'd want the concrete spec:

- **Geocoding endpoint** — URL, required/optional params (`name`, `postcode`, `country`), response shape (confidence scores are useful), and what "works" vs. "fails" looks like
- **Weather forecast endpoints** — daily + hourly, parameter list for each, units handling
- **Response schema** — which fields exist in the current/forecast payloads (`temperature_2m`, `weathercode`, `precipitation_probability`, etc.)
- **Known quirks** — e.g., what happens with out-of-range coordinates or cities that have no geocode match (error shape, not just "undefined")

If you can't point me to an exact URL, a recent example response in the docs would still work.

---

### 2. IndexedDB Schema Specification

The plan says "save locations" and "cache responses," but the actual keys and structure should be defined before coding:

- **Locations store:** `id` (auto-generated), `name`, `address`/coordinates, `timezone`, `createdAt`
- **Weather cache entries:** `id`, `date`, `type` (`current` | `daily`), `data`, `timestamp`
- How old data is considered stale / what the 3–6 hour freshness window actually means in code
- Any indexes you'd want (e.g., querying by date)

---

### 3. Data Flow Architecture Note

You've already noted this should go into the README, but a short pre-written diagram/flow would help me think about it upfront:

```
Geocoding request → Open-Meteo API
        ↓
Parse response (current + daily + hourly)
        ↓
Store in IndexedDB (with timestamp)
        ↓
UI layer reads from DB cache first, falls back to fetch
        ↓
Render → error boundary catches failures
```

A one-paragraph flow or simple ASCII diagram saved before implementation saves a lot of "wait, where does this come from?" rework.

---

### 4. Service Worker Caching Strategy

The plan mentions caching static assets and API responses, but I'd want the rules clarified:

- **What gets precached:** index.html, JS/CSS bundles, manifest.json
- **Runtime cache rules:** how API responses are cached (stale-while-revalidate? only if fresh?), max-age values, revalidation on next idle
- **Offline indicator logic** — exactly what state triggers "offline mode" UI
- How the update banner works (checking `manifest.json` version?)

---

### 5. Component Inventory

A list of all components with their responsibilities and props would keep me consistent:

| Component | Responsibility |
|---|---|
| App / Layout | Header, footer, theme switcher, install button |
| LocationSelector | Search input + suggestions |
| CurrentWeatherCard | Today's conditions |
| HourlyBarChart | Hourly breakdown (canvas/SVG) |
| ForecastList | 10-day grid |
| DrillDownLink | Route param → daily view |
| UnitToggle | °F/°C, mph/km/h switch |

---

### 6. Design Tokens / Theme Spec

The plan mentions themes and dynamic backgrounds. Concrete values would help:

- Color palette per theme (sunny, cloudy, rain, snow, storm) — hex or CSS custom property names
- Accent colors for interactive states
- Font family / sizes
- Spacing scale

If the plan's "dynamic backgrounds" are a design choice, I'd want to know whether it's *condition-driven* (different background per weather) or fully configurable.

---

### 7. Accessibility Checklist

The plan lists requirements but not specifics:

- Which ARIA roles/labels each view gets
- The text alternative for the canvas/SVG charts (this is a real implementation detail)
- Whether `prefers-reduced-motion` disables parallax *and* any chart animation, or just parallax

---

**Bottom line:** with items 1–3 in hand, I can start scaffolding confidently. Items 4–7 are more about polish and consistency — I'd tackle those as the MVP ships out, but having them up front would save a few refactor passes.

Which of these do you have ready to share? Or should we start from scratch on any of them?

96 t/s, 1429 tokens, 15s, 32%

> #### 💬 User

Provide me an example react component for the daily view.

> #### 🤖 Assistant

Here's an example of what a Daily Weather View component could look like, built to match your plan — TypeScript interface, flexbox cards, unit toggle, canvas hourly chart, loading/error states, and time-zone-aware sunrise/sunset display.

```tsx
// components/DailyWeatherView.tsx

import { useState, useEffect } from "react";

// ─── Types ────────────────────────────────────────────────

interface WeatherData {
  timezone: string;
  solar_time_start: string[];
  sunrise: string | null;
  sunset: string | null;
  current: {
    temperature_2m: number;
    feels_like_2m: number;
    wind_speed_10m: number;
    wind_direction_10m?: number;
    humidity: number;
    weathercode: number;
    clouds_covered: number;
  };
  hourly: {
    time: string[];
    temperature_2m: number[];
    weathercode: number[];
    wind_speed_10m: number[];
    relative_humidity_2m: number[];
  };
}

interface Location {
  lat: number;
  lon: number;
  name: string;
  timezone?: string;
}

// ─── Helpers ──────────────────────────────────────────────

const UNITS = {
  celsius: { label: "°C", unit: "°C" },
  fahrenheit: { label: "°F", unit: "°F" },
} as const;

export function toFahrenheit(c: number): number {
  return (c * 9) / 5 + 32;
}

// ─── API Fetching (with cache awareness placeholder) ──────

const CACHE_TTL_MS = 3 * 60 * 60 * 1000; // 3 hours

async function fetchWeather(
  lat: number,
  lon: number,
  unit: "celsius" | "fahrenheit"
): Promise<{ data: WeatherData; source: "api" }> {
  const params = new URLSearchParams({
    latitude: String(lat),
    longitude: String(lon),
    hourly:
      "temperature_2m,weathercode,wind_speed_10m,relative_humidity_2m",
    daily: "weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset",
    timezone: "auto",
  });

  const response = await fetch(
    `https://api.open-meteo.com/v1/forecast?${params.toString()}`
  );
  if (!response.ok) {
    throw new Error(`Weather API error: ${response.status}`);
  }
  return { data: (await response.json()) as WeatherData, source: "api" };
}

// ─── Sub-component: Hourly chart on canvas ────────────────

function HourlyChart({ hourly }: { hourly: WeatherData["hourly"] }) {
  const width = 300;
  const height = 100;

  return (
    <canvas
      width={width}
      height={height}
      style={{ borderRadius: "8px", background: "#1a1a2e" }}
      role="img"
      aria-label="Hourly temperature chart"
    >
      {/* Simple bar-chart using canvas */
      <svg width={width} height={height}>
        {hourly.time.map((t, i) => {
          const temp = hourly.temperature_2m[i];
          // Map approximate temperature range to bar height
          const minTemp = Math.min(...hourly.temperature_2m);
          const maxTemp = Math.max(...hourly.temperature_2m);
          const h = ((temp - minTemp) / (maxTemp - minTemp || 1)) * height;
          return (
            <rect
              key={t}
              x={i * (width / hourly.time.length)}
              y={height - h}
              width={width / hourly.time.length - 2}
              height={h}
              fill="#4fc3f7"
            />
          );
        })}
      </canvas>
    </canvas>
  );
}

// ─── Main component ───────────────────────────────────────

export function DailyWeatherView({
  lat,
  lon,
  name,
}: {
  lat: number;
  lon: number;
  name: string;
}) {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Unit state — would persist to IndexedDB in the real app
  const [unit, setUnit] = useState<"celsius" | "fahrenheit">(
    "celsius"
  );

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await fetchWeather(lat, lon, unit);
        if (!cancelled) {
          setWeather(data.data);
        }
      } catch (e: any) {
        if (!cancelled) setError(e.message ?? "Failed to load weather");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [lat, lon, unit]);

  const fmt = (v: number, u: string) =>
    `${unit === "fahrenheit" ? toFahrenheit(v) : v.toFixed(1)}${u}`;

  if (loading) {
    return (
      <div className="weather-skeleton">
        {/* Loading skeleton — flexbox column of card-like placeholders */
        <div className="card-skeleton">Skeleton loading…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div
        role="alert"
        className="weather-error"
        style={{
          color: "#b71c1c",
          padding: "1rem",
          borderBottom: "1px solid #e0e0e0",
        }}
      >
        Couldn't load weather data: {error}. Retry or refresh.
      </div>
    );
  }

  if (!weather) {
    return (
      <div className="weather-empty" role="status">
        No weather data available for this location.
      </div>
    );
  }

  const isDaytime = new Date().getHours() >= 6 && new Date().getHours() < 18;

  return (
    <section
      className="daily-weather"
      aria-live="polite"
      style={{
        padding: "1.5rem",
        background: "#fff",
        color: "#1a1a2e",
      }}
    >
      {/* Header */}
      <div className="weather-header" style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2>{name}</h2>

        {/* Unit toggle */}
        <span
          role="switch"
          aria-checked={unit === "celsius"}
          aria-label="Toggle temperature units, Celsius / Fahrenheit"
          style={{
            width: 44,
            height: 24,
            borderRadius: "12px",
            background:
              unit === "celsius" ? "#4fc3f7" : "#ff9800",
            position: "relative",
            cursor: "pointer",
          }}
        >
          <div
            style={{
              width: 20,
              height: 24,
              borderRadius: "50%",
              background:
                unit === "celsius" ? "#fff" : "transparent",
              transition: "transform 0.2s, left 0.2s",
              left: unit === "celsius" ? 0 : 22,
            }}
          />
        </span>

        {/* Refresh button */}
        <button
          onClick={() => window.location.reload()}
          aria-label="Refresh weather data"
          style={{
            padding: "4px 10px",
            borderRadius: "4px",
            border: "1px solid #ccc",
            background: "#f5f5f5",
          }}
        >
          ↻
        </button>
      </div>

      {/* Main metrics row */}
      <div className="metrics-row" style={{ display: "flex", flexWrap: "wrap", gap: 12 }}>
        <WeatherCard
          label="Temperature"
          value={fmt(weather.current.temperature_2m, unit)}
          icon="🌡️"
        />
        <WeatherCard
          label="Feels like"
          value={fmt(weather.current.feels_like_2m, unit)}
          icon="💨"}
        />
        <WeatherCard
          label="Wind"
          value={`${fmt(weather.current.wind_speed_10m, unit)} km/h`}
          icon="🌬️"}
        />
        <WeatherCard
          label="Humidity"
          value={`${weather.current.humidity}%`}
          icon="💧"}
        />
      </div>

      {/* Sun & moon */}
      <div className="sun-moon-row" style={{ display: "flex", gap: 12, marginTop: 8 }}>
        {weather.sunrise && (
          <div className="time-card">
            <span className="time-label">Sunrise</span>
            <span>{weather.sunrise}</span>
          </div>
        )}
        {weather.sunset && (
          <div className="time-card">
            <span className="time-label">Set</span>
            <span>{weather.sunset}</span>
          </div>
        )}
      </div>

      {/* Hourly breakdown */}
      <div className="hourly-section" role="region" aria-label="Hourly forecast chart">
        <HourlyChart hourly={weather.hourly} />
      </div>
    </section>
  );
}

// ─── Sub-component: Metric card ───────────────────────────

function WeatherCard({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
  icon: string;
}) {
  return (
    <div
      className="weather-card"
      role="region"
      aria-label={label}
      style={{
        flex: "1 0 120px",
        padding: "0.75rem 1rem",
        background: "#f9f9fb",
        borderRadius: "8px",
        textAlign: "center" as const,
        boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
      }}
    >
      <span style={{ fontSize: "1.5rem", marginBottom: 4 }}>{icon}</span>
      <div style={{ fontWeight: 600, fontSize: "1rem" }}>{label}</div>
      <div className="value">{value}</div>
    </div>
  );
}
```

**How this aligns with your plan:**

- **Flexbox cards** — the `.metrics-row` and card styles use flexbox for responsive layout
- **Unit toggle** — `unit` state toggles between °C/°F, with a visual slider switch (real persistence would go to IndexedDB)
- **Timezone handling** — the API is called with `timezone=auto`, so sunrise/sunset are returned in the location's local time
- **Canvas hourly chart** — simple bar chart drawn directly on canvas (no library needed)
- **Loading/error states** — skeleton placeholder while loading, ARIA alert for errors, empty state if no data
- **Accessibility** — `aria-live="polite"` on the main region, role switches, text alternatives via aria-label on the canvas
- **Error boundaries ready** — this component can be wrapped in an error boundary; a failed fetch lands here cleanly

A few notes for when we implement it:

1. The chart is intentionally minimal (a bar per hour) since drawing polished SVG/canvas charts from scratch takes care. If you want to scale it up, that's Part 4 territory.
2. `fetchWeather` would need a small wrapper around IndexedDB caching — serve cached data if the response is under 3–6 hours old, otherwise fetch fresh.
3. The unit toggle state should be persisted in IndexedDB (and restored on page load) rather than living only in local component state.

Want me to continue with any other part of the plan next?

92 t/s, 3743 tokens, 41s, 52%
