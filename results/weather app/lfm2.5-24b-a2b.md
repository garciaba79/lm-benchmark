# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
Test: Weather App Planning
Created: 10/27/2026, 07:27:03 AM
Exported from: LM Studio (via test script)
Context 16K

### User

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

### Assistant

I've read through your complete Weather PWA development plan — from the core goals (single-page React + PWA, custom visuals, offline caching, accessibility) down to each phase (initialization, daily/10-day views, visual polish, PWA completion). I understand the tech stack decisions (React, TypeScript, Vite, react-router-dom, idb, CSS Modules, Biome, Vitest, GitHub Actions, Vercel deployment) and that we're committing to custom SVG/cancel-drawn graphics with transform-based parallax, time zone-aware data, unit toggles, geocoding via Open-Meteo, IndexedDB caching, service worker registration in Part 5, manifest.json for installability, and an accessibility-first approach throughout.

I'm standing by for the next instruction — whether that's starting with project scaffolding (initializing the Vite + React + TypeScript project with Biome setup), or proceeding to whichever phase you'd like to tackle first. Just let me know what you'd like to do.

106 t/s, 387 tokens, 6s, 18%

### User

What do you think about the app plan? Does it sound good, any issues, any improvements?

### Assistant

Your plan is solid — well-scoped, realistic for a portfolio project, and the progressive-enhancement flow makes it easy to make incremental progress without getting bogged down in one phase. Here's my read:

---

### What I think works well

1. **Clean, honest scope.** Single-page React + PWA, no Next.js bloat, custom SVGs/cancel-drawn visuals, and a real free weather API (Open-Meteo) with no API key — all of this is impressive on a resume and practical for shipping.
2. **Accessibility baked in from the start**, not bolted on later. Keyboard nav, focus states, semantic HTML, reduced-motion handling, color contrast — good call.
3. **Practical tech choices.** Vite + TypeScript + React Context is a lightweight combo that's easy to explain and maintain.
4. **Smart phasing.** MVP first (daily + 10-day views), then polish PWA + visuals. The milestone structure keeps each chunk shippable.
5. **Real-world edge cases handled:** geocoding fallbacks, denied geolocation, stale cache, pull-to-refresh caveats on iOS.

---

### Issues and improvements to consider

**1. Service worker strategy — use `vite-plugin-pwa`**
You flagged manual service worker setup as optional, but for a project where the goal is reliability (offline behavior needs to actually work), I'd strongly recommend using the plugin instead of writing it by hand. It handles caching strategies, precache manifest generation, and update registration out of the box. Your plan even lists `vite-plugin-pwa` as an "optional fallback" — making it the default would reduce risk on Part 5 when you're also doing other PWA work.

**2. Define a simple IndexedDB schema upfront**
Parts 1–2 talk about saving locations and caching API responses, but the exact store structure isn't written down yet. I'd recommend two small stores:
- **Locations:** `id`, `name`, `lat`, `lon`, `address` (optional)
- **WeatherCache:** `key` (e.g., `"current:{date}"`), `data`, `timestamp`

Having this defined before implementation saves you from a refactor later.

**3. Geocoding approach — be explicit about the endpoint**
The plan mentions "geocoding spike with city names, zip/postal codes, and coordinates" but Open-Meteo's dedicated geocoding API (`/v1/search`) is straightforward for cities and postal codes, while coordinates are always reliable. I'd make that the documented approach in Part 1 so you don't end up with a half-baked fallback.

**4. Remove or implement "rain levels"**
Your notes list "restores... rain levels," but it's not clear if this is a planned feature for the MVP or an old Version B left over from a previous iteration. Either commit to it (as a small visual/UI element) or delete that line — dangling references like this can confuse reviewers.

**5. Error recovery flow**
You've covered error boundaries, loading states, and empty states. One thing worth adding: when geolocation is denied, show a clear inline message ("Location access was blocked") with an immediate "Try again" button rather than relying solely on the fallback UI.

**6. Test coverage beyond unit tests**
Vitest for cache/API logic is good. If your scope allows, even one or two integration tests (e.g., "cache hits when fresh," "indexedDB read/write round-trip") would strengthen the portfolio significantly. Not mandatory — just a suggestion for polish.

**7. Lighthouse targets are ambitious but fine**
90+ on PWA/performance/accessibility is aggressive for a custom-crafted small app, but it's a good north star. If you miss one score, focus on the easy wins: smaller bundle, no heavy scripts, proper viewport sizing.

---

### Bottom line

Your plan is portfolio-ready as-is — I don't see any red flags. The main adjustments are pragmatic:

- **Use `vite-plugin-pwa`** instead of hand-writing a service worker
- **Lock in the IndexedDB schema early**
- **Pin the geocoding method** to Open-Meteo's `/v1/search`
- **Clarify or remove "rain levels"** so it doesn't read as an unfinished thought

If you want, we can start on Phase 1 (project initialization and folder structure) whenever you're ready. Just say the word.

103 t/s, 1962 tokens, 19s, 30%

### User

What tech documentation would help you understand the app plan better?

### Assistant

The plan itself is strong, so my answer is: **the plan covers more than enough of what I need to start implementation.** That said, here's where a small amount of additional context would make the first phase smoother:

---

### Already well-covered (no extra docs needed)

- Full stack of features and milestones
- Tech stack with exact versions and rationale
- State management strategy
- Accessibility requirements
- Offline behavior expectations

I can work from this as-is.

---

### Information that would be genuinely useful to see in a separate doc (or ask you about) before I start scaffolding:

**1. Open-Meteo API contract**
You're using the free tier, and I want to lock down exactly which endpoints and response shapes:
- `https://api.open-meteo.com/v1/forecast` — what are all the supported parameters for location search vs. daily forecast?
- What does a successful current-conditions response look like? (temperature, feels-like wind/humidity, sunrise/sunset, etc.)
- How is the 10-day data formatted per day?
- Are there rate limits or usage warnings I should be aware of?

**2. IndexedDB schema**
You have two small stores in mind (locations + weather cache). A short description of the exact shape — e.g., for a location record: `{ id, name, lat, lon, address?, savedAt }` and for the cache: `{ key, data, timestamp }` — would save me from guessing when I implement.

**3. Caching freshness logic**
You mentioned "serve from cache if fresh (under 3–6 hours, same day)." What's the threshold in practice? Is it a fixed window (e.g., 4 hours) or does it vary by data type (current conditions vs. 10-day forecast)? And should the app prefer live data when stale even if offline is off?

**4. PWA manifest details**
- Icon sizes and formats for Android/iOS install
- Theme colors — do you want a specific palette, or is Open-Meteo's attribution text enough?
- Display mode (standalone) — already implied

**5. CI pipeline shape**
What should the GitHub Actions workflow include? Just: lint → test → build? Or do you also want a deploy-to-preview step to Vercel in CI?

---

### How I'd actually ask for these

I don't think any of this needs to be written up as a separate document. In practice, when I start the project:

1. First commit = scaffolding + folder structure (per your plan)
2. Once location search is done, I'll verify the Open-Meteo response shape and confirm it against your spec
3. If anything's ambiguous at that point, I'll ask right then

---

### Bottom line on documentation

**The plan itself is enough to start.** The main decision still pending from me before Phase 1 begins is: **React major version (18.x)** — you noted both the older pinned versions and "newer majors are available" as an option. If I want to record a reason in the README, it's a quick call (I'd go with whatever's stable on npm today). Just say which one you prefer.

Beyond that, the project is self-documenting from your plan — no separate tech docs needed unless something changes mid-stream. Ready when you are.

101 t/s, 950 tokens, 10s, 29%

### User

Provide me an example react component for the daily view.

### Assistant

Here's an example DailyWeatherView component that demonstrates the patterns in your plan: loading/error states, unit toggle (F/C, mph/km/h), canvas-drawn hourly chart, flexbox layout for current conditions, caching awareness, and last-updated timestamp.

```tsx
import { useState, useEffect, useRef } from 'react';

// ── Types ───────────────────────────────────────────────────────────
interface CurrentWeather {
  temperature: number;
  feels_like: number;
  wind_speed: number;
  wind_degrees: number;
  humidity: number;
}

interface HourlyRecord {
  time: string; // ISO 8601
  temperature: number;
  precipitation_probability: number;
  cloud_cover: number;
}

interface WeatherData {
  timezone: string;
  current: CurrentWeather;
  hourly: HourlyRecord[];
  last_updated: number; // Unix ms timestamp (location's local time)
}

// ── Configuration ───────────────────────────────────────────────────
const CACHE_TTL_MS = 3 * 60 * 60 * 1000; // 3 hours — same-day freshness window

const UNITS = {
  metric: { tempLabel: '°C', windLabel: 'km/h' },
  imperial: { tempLabel: '°F', windLabel: 'mph' },
} as const;

// ── Helpers ─────────────────────────────────────────────────────────
function displayTemp(temp: number, unit: 'metric' | 'imperial'): string {
  return unit === 'imperial'
    ? `${Math.round(temp)}°${UNITS.imperial.tempLabel}`
    : `${Math.round(temp)}°${UNITS.metric.tempLabel}`;
}

function displayWind(speed: number, unit: 'metric' | 'imperial'): string {
  return `${speed} ${unit === 'imperial' ? 'mph' : 'km/h'}`;
}

// ── Canvas Chart Component (hourly temperature line) ───────────────
function HourlyChart({
  data,
  units,
}: {
  records: HourlyRecord[];
  width: number;
  height: number;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const ctx = canvasRef.current.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, width, height);
    if (data.length < 2) return;

    const margin = { top: 10, right: 20, bottom: 30, left: 40 };
    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;

    // Extract temperatures
    const temps = data.map((r) => r.temperature);
    const minT = Math.min(...temps) - 2; // padding for axes
    const maxT = Math.max(...temps) + 2;
    const range = maxT - minT || 1;

    // X positions (evenly spaced)
    data.forEach((_, i) => {
      const x = margin.left + (i / (data.length - 1)) * plotW;
      const y = margin.top + ((maxT - temps[i]) / range) * plotH;

      ctx.beginPath();
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
      ctx.strokeStyle = '#4a9eff';
      ctx.lineWidth = 2;
      ctx.stroke();
    });

    // Draw X axis labels
    data.forEach((r, i) => {
      const x = margin.left + (i / (data.length - 1)) * plotW;
      if (x >= margin.left && x <= margin.left + plotW) {
        ctx.fillStyle = '#555';
        ctx.font = '10px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(r.time.slice(5), x, height - 8);
      }
    });
  }, [data]);

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      style={{ display: 'block', marginBottom: 10 }}
    />
  );
}

// ── Main View Component ─────────────────────────────────────────────
export function DailyWeatherView({ lat, lon }: { lat: number; lon: number }) {
  // State
  const [data, setData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [units, setUnits] = useState<'metric' | 'imperial'>('metric');

  // ── Fetch with cache awareness (simplified — IndexedDB layer in Part 5) ──
  useEffect(() => {
    let cancelled = false;

    async function fetchWeather() {
      try {
        setLoading(true);
        setError(null);

        // Check cached data first if available and fresh:
        const cached = await getCachedData(lat, lon);
        if (cached && !isStale(cached)) {
          setData(cached);
          return;
        }

        // Fetch from Open-Meteo
        const url =
          `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}` +
          `&hourly=temperature_2m,precipitation_probability,cloud_cover` +
          `&current_weather=true&timezone=auto`;

        const res = await fetch(url);
        if (!res.ok) throw new Error(`Weather API error: ${res.status}`);

        const json: WeatherData = await res.json();
        setData(json);

        // Cache for future offline loads (implemented in Part 5)
        saveToCache(lat, lon, json);
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchWeather();

    return () => { cancelled = true; };
  }, [lat, lon]);

  // ── Render helpers (loading / error / empty) ───────────────────────
  const renderSkeleton = () => (
    <div style={{ padding: '16px', textAlign: 'center' }}>
      {[...Array(6)].map((_, i) => (
        <div key={i} style={{ marginBottom: 8, height: 14, borderBottom: '1px dashed #ccc' }} />
      ))}
    </div>
  );

  const renderError = () => (
    <div
      role="alert"
      style={{
        padding: '16px',
        color: '#b00',
        background: '#fff5f5',
        borderRadius: 8,
        textAlign: 'center',
      }}
    >
      <strong>Could not load weather data.</strong>
      {error ? `Error: ${error}` : "Try tapping Refresh to retry."}
      <button
        onClick={() => window.location.reload()}
        style={{ marginTop: 8, padding: '6px 16px', cursor: 'pointer' }}
      >
        Refresh
      </button>
    </div>
  );

  // ── Render ────────────────────────────────────────────────────────
  return (
    <section style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 480, margin: '0 auto' }}>
      {/* Header */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: 12 }}>
        <h2 style={{ margin: 0, fontSize: '1.25rem' }}>Today's Weather</h2>

        {/* Unit toggle */}
        <div
          role="group"
          aria-label="Temperature and wind units"
          style={{
            display: 'flex',
            gap: 4,
            background: '#eee',
            borderRadius: 6,
            padding: '3px',
          }}
        >
          {(['metric', 'imperial'] as const).map((u) => (
            <button
              key={u}
              onClick={() => setUnits(u)}
              style={{
                padding: '4px 12px',
                border: 'none',
                borderRadius: 4,
                cursor: 'pointer',
                fontSize: '0.85rem',
                background: u === units ? '#4a9eff' : 'transparent',
                color: u === units ? '#fff' : '#333',
                fontWeight: u === units ? 600 : 400,
              }}
            >
              {u === 'metric' ? '°C / km/h' : '°F / mph'}
            </button>
          ))}
        </div>
      </header>

      {loading && renderSkeleton()}

      {error && renderError()}

      {data && !loading && (
        <article style={{ marginTop: 16 }}>
          {/* Current conditions card — flexbox */}
          <div
            role="region"
            aria-label="Current weather summary"
            style={{
              display: 'flex',
              gap: 20,
              padding: '14px',
              background: '#f4f6f8',
              borderRadius: 10,
              marginBottom: 16,
            }}
          >
            <div
              style={{
                flex: 1,
                textAlign: 'center',
                background: '#fff',
                border: '1px solid #ddd',
                borderRadius: 6,
                padding: 12,
                boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
              }}
            >
              <div
                style={{
                  fontSize: '2.5rem',
                  fontWeight: 700,
                  lineHeight: 1,
                  color: '#4a9eff',
                }}
              >
                {displayTemp(data.current.temperature, units)}
              </div>
              <div style={{ marginTop: 6 }}>
                <div style={{ fontSize: '0.8rem', color: '#555' }}>Feels like</div>
                <div style={{ fontWeight: 600 }}>{displayTemp(data.current.feels_like, units)}</div>
              </div>
            </div>

            <div
              style={{
                flex: 1,
                textAlign: 'right',
                background: '#fff',
                border: '1px solid #ddd',
                borderRadius: 6,
                padding: '12px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
              }}
            >
              <div style={{ fontSize: '0.85rem', color: '#777' }}>Wind</div>
              <div style={{ fontWeight: 600 }}>{displayWind(data.current.wind_speed, units)}</div>
              <div style={{ marginTop: 4 }}>Feels like {data.current.humidity}% humidity</div>
            </div>
          </div>

          {/* Sunrise / sunset */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-around',
              padding: '8px 0',
              fontSize: '0.9rem',
              color: '#555',
            }}
          >
            <span>🌅 Sunrise {new Date(data.timezone === 'auto' ? data.last_updated : data.last_updated).toLocaleTimeString([], {
              hour: 'numeric', minute: '2-digit',
            })}</span>
            <span>🌇 Sunset {new Date(data.timezone === 'auto' ? data.last_updated : data.last_updated).toLocaleTimeString([], {
              hour: 'numeric', minute: '2-digit',
            })}</span>
          </div>

          {/* Hourly breakdown — canvas chart */}
          <div style={{ marginTop: 16 }}>
            <h3 style={{ fontSize: '0.95rem', marginBottom: 8 }}>Hourly (next 24 h)</h3>
            <div
              role="img"
              aria-label="Temperature line chart of the next 24 hours"
              style={{
                width: '100%',
                height: 120,
              }}
            >
              <HourlyChart records={data.hourly} units={units} width={400} height={120} />
            </div>
          </div>

          {/* Last updated */}
          <p
            style={{
              marginTop: 12,
              fontSize: '0.8rem',
              color: '#888',
            }}
          >
            Updated {new Date(data.last_updated).toLocaleTimeString([], {
              hour: 'numeric', minute: '2-digit',
            })}
          </p>
        </article>
      )}
    </section>
  );
}

// ── Utility helpers (would connect to IndexedDB in Part 5) ───────────
async function getCachedData(lat: number, lon: number): Promise<WeatherData | null> {
  // In Part 5: query IndexedDB store "weatherCache" by key `${lat}:${lon}`
  // Return data if timestamp is within CACHE_TTL_MS
  return null;
}

async function saveToCache(
  lat: number,
  lon: number,
  data: WeatherData
): Promise<void> {
  // In Part 5: write to IndexedDB store "weatherCache"
}
```

**Key patterns demonstrated in this example:**

1. **Loading state** — skeleton placeholders with a refresh button on error.
2. **Unit toggle** — F/C and mph/km/h switch, persisted in local state (would be saved in IndexedDB per the cache strategy).
3. **Canvas hourly chart** — a self-contained `<canvas>` drawing temperature line from the API's hourly data; flexbox layout for surrounding cards.
4. **Flexbox layout** — current conditions split into two cards, responsive padding and border-radius styles.
5. **Error boundary friendly** — error state with an explicit retry action (`window.location.reload()` as a simple fallback; in production you'd wrap views in React error boundaries per the plan).
6. **Cache-aware fetch pattern** — checks IndexedDB cache before hitting the network, and records freshness via `last_updated`. The actual storage/retrieval is stubbed so it's clear where Part 5 hooks in.
7. **Accessibility** — `role="region"`, `aria-label` on chart canvas, text alternatives for visual data.

When you're ready to start scaffolding, I'll create the project structure and build from here.

93 t/s, 6045 tokens, 65s, 65%
