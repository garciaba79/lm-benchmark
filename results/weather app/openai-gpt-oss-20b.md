# GPT-OSS 20B
Model: openai/gpt-oss-20b
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

Got it! I’ll hold off on any code or detailed examples until you’re ready to dive in. Just let me know when you’d like to start, and I’m here to help with the next steps.

118 t/s, 94 tokens, 2s, 16%

> #### 💬 User

What do you think about the app plan? Does it sound good, any issues, any improvements?

> #### 🤖 Assistant

Your weather‑PWA roadmap is solid and covers all the essential pieces for a production‑ready, portfolio‑worthy app.  Below are my observations, a few quick sanity checks, and some incremental improvements you might consider before you hit “scaffold.”

---

## ✔️ What’s Working Well

| Category | Why it’s good |
|----------|---------------|
| **Scope** | You’ve split the work into clear, deliverable parts (MVP → polish → PWA).  That keeps risk low and lets you ship a usable app early. |
| **Technology choices** | React + Vite + TypeScript gives a fast dev experience; `react-router-dom` for navigation is lightweight enough to avoid Next.js bloat. |
| **State & data flow** | Context + hooks for global location / unit prefs keeps the tree shallow, and IndexedDB via `idb` is a proven pattern for offline persistence. |
| **Testing** | Vitest for unit tests of cache logic and data‑mapping is great; you could add component snapshot or integration tests later if needed. |
| **CI/CD** | GitHub Actions + Biome lint/format ensures code quality without manual steps. |
| **Accessibility focus** | Explicit requirements (contrast, reduced motion, keyboard nav) show you’re building for inclusivity from the start. |
| **PWA fundamentals** | Manual service worker + manifest gives you control; fallback to `vite-plugin-pwa` is a smart “if‑we‑get stuck” safety net. |
| **Documentation** | The README checklist (screenshots, architecture note, run instructions) will impress recruiters. |

---

## ⚠️ Potential Pitfalls & Quick Fixes

| Issue | Why it matters | Suggested Mitigation |
|-------|----------------|----------------------|
| **Open‑Meteo rate limits** | Free tier may throttle if you hit the API from many users or during dev tests. | Cache all responses aggressively (3–6 h window) and add a “mock” mode for local dev that serves static JSON. |
| **Geocoding fallback logic** | Postal code coverage is spotty; if you rely solely on `search` endpoint, you may get ambiguous results. | Keep the “city‑only search + coordinates” fallback as a separate path.  Offer an “advanced search” UI where users can manually adjust lat/lng when auto‑detect fails. |
| **Timezone handling** | You’re requesting `timezone=auto`; be careful that you always display times using the returned zone, not the browser’s default. | Use a small helper (`date-fns-tz` or plain Intl.DateTimeFormat with a custom timeZone) and memoize the zone per location to avoid repeated conversions. |
| **IndexedDB schema evolution** | If you add new fields (e.g., unit prefs, favorite locations), migrations can break older users. | Adopt a simple versioning strategy (`idb-keyval` style or `dexie`) that runs migration scripts on open. |
| **Service worker update flow** | The “Update available” banner is great, but you need to make sure the new assets are fetched *before* the user clicks reload. | Use `self.skipWaiting()` and `clients.claim()` in a dedicated “activate” event; test with multiple tabs. |
| **Accessibility of dynamic charts** | Canvas/SVG needs ARIA labels or text alternatives. | Wrap your chart component in `<figure>` + `<figcaption>` that describes the data, and add `role="img"` + `aria-label` on the SVG element. |
| **Testing offline scenarios** | Vitest runs in Node; you won’t hit service worker logic. | Add a small integration test with `msw` (Mock Service Worker) to simulate network failures and ensure your UI falls back correctly. |

---

## 🔧 Incremental Enhancements

1. **Feature‑flag for API switching**  
   Even if the current scope is Open‑Meteo only, add a tiny context value (`apiProvider`) that can be toggled in dev mode.  That makes future “Part 7” (multiple APIs) trivial.

2. **Progressive enhancement of geolocation**  
   Use `navigator.geolocation.watchPosition` to keep the location fresh while the user is on the app.  Show a subtle spinner or "updating…" label when you’re re‑fetching data.

3. **Theme persistence via CSS custom properties**  
   Instead of hard‑coding color palettes, expose them as `--primary`, `--bg`, etc., and let each weather scene adjust those values.  That keeps the visual theme logic in one place and eases future dark‑mode work.

4. **Accessibility audit automation**  
   Add a GitHub Action that runs `axe-core` or `pa11y` against your built app.  You’ll catch focus‑order or ARIA mistakes early.

5. **CI cache for node_modules**  
   If build times become an issue, cache the Vite/Node modules in GitHub Actions to speed up PR checks.

6. **LocalStorage fallback**  
   For environments where IndexedDB isn’t available (e.g., Safari on iOS 12), provide a graceful degradation using `localStorage`.  Keep the API surface identical.

---

## 📌 Quick Checklist Before You Scaffold

- [ ] Decide whether to stay on React 18.x / Vite 5.x or upgrade now.  
- [ ] Pin Biome to an exact version (e.g., `0.3.1`).  
- [ ] Create a minimal `tsconfig.json` that includes `"esModuleInterop": true`.  
- [ ] Draft the IndexedDB schema: `{ locations: [...], prefs: { unit, theme }, cache: [{ key, data, timestamp }] }`.  
- [ ] Sketch the folder tree (already in your plan) and create a placeholder `index.tsx` that mounts `<App />`.  
- [ ] Write a tiny “hello world” test for Vitest to confirm it’s wired up.  

Once those are in place you can start implementing Part 1 and have a runnable skeleton quickly.

---

### Bottom Line

Your plan is *excellent*—it balances ambition with pragmatism, prioritizes UX (offline + accessibility), and leaves room for future growth without bloating the core stack.  Just keep an eye on API limits, schema migrations, and the service worker update flow, and you’ll have a clean, deployable portfolio piece in no time.

Let me know which part you’d like to tackle first or if you need help fleshing out any of the above!

117 t/s, 1396 tokens, 12s, 25%

> #### 💬 User

What tech documentation would help you understand the app plan better?

> #### 🤖 Assistant

Below is a “cheat‑sheet” list of technical documents (or sections of a single document) that will give me—your assistant—a clear, unambiguous view of every moving part in your Weather PWA plan.  I’ll use these when we start scaffolding, writing tests, or troubleshooting later on.

| Doc / Section | Why it matters | What to include |
|---------------|----------------|-----------------|
| **1️⃣ Project README (Architecture)** | First‑hand source of truth for anyone reading the repo. | • High‑level overview<br>• Data flow diagram (Geocoding → Weather API ↔ IndexedDB ↔ UI)<br>• State diagram (Context trees, provider order)<br>• Build & dev scripts |
| **2️⃣ `package.json` / lockfile** | Guarantees exact versions of every dependency. | • Exact React, Vite, react‑router, idb, Vitest, Biome, etc.<br>• Scripts: `dev`, `build`, `test`, `lint`, `format` |
| **3️⃣ `tsconfig.json` & TypeScript settings** | Avoids “it works locally but not in CI” surprises. | • Target (ES2022 or newer), module (`esnext`), strictness flags, lib list |
| **4️⃣ Biome config (`biome.json`)** | Keeps linting/formatting consistent across contributors. | • Exact rule set (e.g., `no-unused-vars`, `semi:never`) |
| **5️⃣ Vite config (`vite.config.ts`)** | Central place for dev server, alias, build options, PWA plugin flags. | • Resolve aliases (`@/*` → `src/`)<br>• CSS module settings<br>• Plugin list (React, PWA optional) |
| **6️⃣ Folder & file map** | Gives a quick mental model of the codebase layout. | • `/src/components`, `/views`, `/context`, `/utils`, `/styles`, `/data`, `/assets` |
| **7️⃣ IndexedDB schema spec** | Prevents runtime crashes when you change fields or add migrations. | • `locations`: `{ id, name, lat, lon, lastUsed }`<br>• `prefs`: `{ unit: 'c'|'f', theme: 'light'|'dark' }`<br>• `cache`: `{ key, data, timestamp }` |
| **8️⃣ Open‑Meteo API contract** | Clarifies request/response shapes and limits. | • Base URLs (`/forecast`, `/geocoding/search`) <br>• Required query params (`latitude`, `longitude`, `timezone=auto`) <br>• Response JSON schema (e.g., `daily: { time, temperature_2m_max }`) |
| **9️⃣ Geolocation & geocoding flow diagram** | Visualizes the “search → use my location” UX path. | • Steps: user input → API call → parse → store in IndexedDB → set context → fetch weather |
| 🔟 Service Worker strategy (offline caching) | Shows how assets and API responses are cached, stale‑while‑revalidate logic, update flow. | • Cache names (`static-v1`, `api-weather-v1`) <br>• `fetch` handler pseudocode <br>• Activation & skipWaiting steps |
| 1️⃣1️⃣ Accessibility checklist** | Keeps focus on WCAG compliance throughout development. | • Color contrast table per theme<br>• Keyboard navigation map (tab order, focus styles)<br>• ARIA roles for charts and dynamic lists |
| 1️⃣2️⃣ Testing strategy document** | Guides unit/integration tests coverage. | • Vitest config (coverage thresholds) <br>• Mock server (msw) setup <br>• Key test cases: cache freshness, error boundary rendering, unit toggle logic |
| 1️⃣3️⃣ GitHub Actions workflow files** | Demonstrates CI pipeline expectations. | • `biome.yml` – lint/format<br>• `test.yml` – run Vitest & coverage <br>• `build.yml` – Vite build and artifact upload |
| 1️⃣4️⃣ Deployment notes (Vercel)** | Ensures build works on target host. | • Environment variables (none for Open‑Meteo, but note if you add API keys later) <br>• Build command (`vite build`) <br>• Output directory (`dist/`) |
| 1️⃣5️⃣ Manifest & icons spec** | Guarantees installability and brand consistency. | • `manifest.json` fields (name, short_name, start_url, display, background_color, theme_color) <br>• Icon sizes & maskable flag |

---

### How to Use These Docs

1. **Create a single “Technical Overview” markdown file** in the repo root (e.g., `TECH_OVERVIEW.md`).  
2. Copy/paste each section above and flesh it out with your specific values, URLs, and diagrams.  
3. Link this file from the top of your main `README.md` so anyone can jump straight to the details.  
4. Whenever you change a major piece (e.g., upgrade Vite or add a new IndexedDB field), update the relevant section—this keeps future developers (or yourself) from hunting down hidden bugs.

Having these documents in place will let me:

* Quickly answer “what version of React are we on?” without digging into `package.json`.  
* Understand the exact shape of data coming from Open‑Meteo and how it maps to UI.  
* Reproduce the offline caching logic or debug a stale‑data issue by looking at the service‑worker spec.  
* Know where to add tests for new features (e.g., Part 7 API switching) without reinventing the wheel.

Feel free to let me know which of these you’d like help fleshing out first, or if there’s a particular area you’re unsure about—happy to dive deeper!

113 t/s, 1267 tokens, 12s, 32%

> #### 💬 User

Provide me an example react component for the daily view.

> #### 🤖 Assistant

Below is a **minimal, self‑contained** Daily View component that demonstrates the core patterns you’ll need:

```tsx
// src/views/DailyView.tsx
import React, { useEffect, useState, useContext } from 'react';
import { useParams, Link } from 'react-router-dom';

import { LocationContext } from '@/context/LocationProvider';
import { WeatherCache, fetchWeatherForDay } from '@/utils/weatherApi';
import { formatDateTime } from '@/utils/dateHelpers';
import styles from './DailyView.module.css';

// ------------------------------------------------------------------
// Types (you’ll likely have a richer domain model elsewhere)
// ------------------------------------------------------------------
type DailyData = {
  date: string;          // ISO YYYY‑MM‑DD
  tempMax: number;
  tempMin: number;
  sunrise: string;       // ISO string
  sunset: string;        // ISO string
  description: string;
};

export const DailyView: React.FC = () => {
  const { date } = useParams<{ date: string }>();
  const { location, unitPrefs } = useContext(LocationContext);

  const [data, setData] = useState<DailyData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // ------------------------------------------------------------------
  // Fetch logic – uses cache first, then falls back to network
  // ------------------------------------------------------------------
  useEffect(() => {
    if (!location || !date) return;

    let cancelled = false;
    const key = `${location.id}-daily-${date}`;

    async function load() {
      setLoading(true);
      try {
        const cached = await WeatherCache.get<DailyData>(key);
        if (cached && !WeatherCache.isStale(cached.timestamp)) {
          if (!cancelled) setData(cached.data);
          return;
        }

        const fresh = await fetchWeatherForDay(location, date);
        if (!cancelled) {
          setData(fresh);
          WeatherCache.set(key, { data: fresh, timestamp: Date.now() });
        }
      } catch (e: any) {
        if (!cancelled) setError(e.message || 'Unknown error');
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, [location, date]);

  // ------------------------------------------------------------------
  // Render helpers
  // ------------------------------------------------------------------
  const renderTemp = (value: number) =>
    `${value.toFixed(1)}°${unitPrefs.temp === 'c' ? 'C' : 'F'}`;

  if (loading)
    return <div className={styles.skeleton}>Loading…</div>;

  if (error)
    return (
      <div className={styles.error}>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );

  if (!data) return null; // shouldn't happen

  return (
    <article className={styles.container} aria-labelledby="daily-title">
      <header>
        <h1 id="daily-title">{formatDateTime(data.date, 'PPP')}</h1>
        <p>{data.description}</p>
      </header>

      <section className={styles.metrics}>
        <div>
          <strong>High:</strong> {renderTemp(data.tempMax)}
        </div>
        <div>
          <strong>Low:</strong> {renderTemp(data.tempMin)}
        </div>
        <div>
          <strong>Sunrise:</strong>{' '}
          {formatDateTime(data.sunrise, 'p')}
        </div>
        <div>
          <strong>Sunset:</strong>{' '}
          {formatDateTime(data.sunset, 'p')}
        </div>
      </section>

      {/* Example of a simple SVG chart – replace with your own */}
      <figure className={styles.chart}>
        <svg viewBox="0 0 100 50" role="img" aria-label={`Temperature trend for ${data.date}`}>
          {/* Dummy line; you’ll compute points from hourly data */}
          <polyline
            fill="none"
            stroke="#0077ff"
            strokeWidth="2"
            points="10,40 30,20 50,35 70,15 90,25"
          />
        </svg>
      </figure>

      {/* Navigation to next/prev day */}
      <nav className={styles.nav}>
        <Link to={`/daily/${new Date(data.date).setDate(new Date(data.date).getDate() - 1)}`}>
          &larr; Previous
        </Link>
        <Link to={`/daily/${new Date(data.date).setDate(new Date(data.date).getDate() + 1)}`}>
          Next &rarr;
        </Link>
      </nav>
    </article>
  );
};
```

### What this snippet shows

| Feature | How it’s handled |
|---------|-----------------|
| **Context** – pulls the current location and unit preferences. |
| **React Router param** – reads `date` from the URL. |
| **Cache‑first fetch** – checks IndexedDB (`WeatherCache`) before hitting the network. |
| **Stale‑check** – uses a simple timestamp comparison; you can tweak the freshness window in `WeatherCache.isStale`. |
| **Loading / error states** – skeleton and retry button. |
| **Accessibility** – ARIA labels on SVG, semantic `<article>`, focusable links. |
| **Unit toggle** – renders temperatures according to user preference. |
| **Navigation** – simple prev/next day links (you’ll want to guard against out‑of‑range dates in production). |

Feel free to adapt the styles (`DailyView.module.css`) and the SVG chart logic to match your custom graphics. If you need a deeper dive into any helper functions (`fetchWeatherForDay`, `WeatherCache`), just let me know!

108 t/s, 1308 tokens, 12s, 40%
