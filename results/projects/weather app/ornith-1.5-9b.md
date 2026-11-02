# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: Weather App Planning
Created: 11/02/2026, 03:39:46 AM
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

Got it — plan received and understood. I've read through the full Weather PWA development plan (the October 25 merged version) and I'm standing by for your next instruction.

A few things I noted that may be worth deciding now, since they'll ripple into later parts:

- **Version policy** is flagged as a decision to make before scaffolding (React 18 vs latest majors). If you want, we can settle this early so Parts 2–6 stay consistent; otherwise I'll defer it.
- The plan already handles Open-Meteo's non-commercial attribution via the footer credit — good call, since you're deploying publicly to Vercel. Worth keeping that constraint in mind if any future part (e.g., Part 7/8) involves monetization or third-party keys.
- You've kept state management intentionally lightweight (Context + hooks only), which fits your dependency-minimal philosophy. The caching/freshness logic will be the main place this gets interesting — happy to help design that shape when we get there.

When you're ready, I can help with any of:
- Project scaffolding and folder structure
- Component ideas / architecture for specific parts
- IndexedDB schema examples
- Service worker caching strategy
- Or anything else on your list

Just let me know what you'd like to tackle first.

114 t/s, 879 tokens, 8s, 21%

> #### 💬 User

What do you think about the app plan? Does it sound good, any issues, any improvements?

> #### 🤖 Assistant

Overall this is a strong, mature plan — detailed enough to act on directly, with real-world concerns (Open-Meteo attribution, timezone handling, iOS Safari quirks) already baked in rather than bolted on later. The lightweight/dependency-minimal philosophy is coherent throughout and genuinely impressive for a portfolio piece. I'll flag the things that would actually bite you, though.

## What's working well
- **Open-Meteo as the API** — free, no key, reliable. Perfect for a portfolio (no commercial use = fine here). The only real constraint is it stays non-commercial; worth keeping in mind if Part 7/8 ever pivots toward monetization or user-provided keys.
- **Custom SVG/canvas visuals instead of icon libraries** — this is your main differentiator and it's the right call.
- **Accessibility treated as ongoing, not a final pass** — mature approach; most people do it wrong by treating it as an afterthought.
- **Spike-first validation of geocoding assumptions** — good engineering discipline before you build on shaky ground.
- **Testing business logic (cache freshness, data mapping) with Vitest rather than over-testing UI** — correct prioritization given your lightweight stance.
- **Banner-based SW update flow keeping user control** — good UX decision; dismissing shouldn't strand them on stale assets.

## Issues and improvements

**1. Scope vs. time is the real risk.** Parts 4 (visuals) and 5 (offline/PWA) are both substantial, and offline/service-worker polish genuinely eats days of debugging. The plan marks nice-to-haves as optional but doesn't clearly mark Parts 4–6 themselves as "nice to have." My advice: get Parts 1–3 deployable *first*, then invest in polish. Don't build the full caching architecture before you have something working end-to-end — it's tempting, and it usually backfires.

**2. Reconsider "custom flexbox only."** Flexbox handles one-dimensional layouts (rows *or* columns), but your 10-day forecast overview is a natural two-dimensional card grid that reflows across breakpoints. Pure flexbox will make this painful. I'd allow CSS Grid for page-level layout while keeping flexbox for component internals — or at least flag it now so you don't hit friction mid-build in Parts 2–3.

**3. Error boundaries won't catch your fetches.** This is a common gotcha: error boundaries catch synchronous render errors, but unhandled promise rejections from `fetch` calls in event handlers or `useEffect` still need explicit try/catch. Your plan wants error boundaries around views *and* clear error messages for failed fetches — make sure the try/catch lives where the fetch happens, not just relying on the boundary.

**4. Version policy affects more than React.** You're deciding latest vs. older majors, but react-router-dom's major matters too: v7 (current) has meaningful API differences from v6 (route loaders, `useNavigation`, data routers). If you go latest, expect to learn those; if you stay on v6, the plan's assumptions hold. This is worth folding into your version decision now so routing in Parts 2–3 isn't a surprise later.

**5. Two layers of caching need clear separation.** You're doing app-level IndexedDB caching *and* service worker caching. That can work well (SW handles offline asset loading + background sync; IndexedDB gives fast access to recent data even when online), but if the two aren't deliberately separated you'll end up confused about which serves what and possibly double-fetching. Design this boundary early rather than letting it emerge in Part 5.

**6. Local dev gotcha for geolocation.** The Geolocation button needs HTTPS — fine on Vercel, but during local `vite` dev you'll need the localhost exception or a cert. Minor, but worth knowing before Part 1 so you don't get stuck testing "use my location."

## One thing I'd add
For the canvas-drawn hourly forecast, an `aria-label` isn't enough — screen reader users need to actually navigate and read the data (a keyboard-accessible list alternative). Your plan says "with a text alternative," which is the right direction; just make sure it's genuinely usable, not just labeled.

---

Net: keep the architecture and sequencing as-is, but tighten the scope expectations around Parts 4–6, loosen the flexbox-only constraint for grids, and get the error-boundary/async distinction right. Want me to help draft the folder structure or IndexedDB schema next?

113 t/s, 4881 tokens, 43s, 47%

> #### 💬 User

What tech documentation would help you understand the app plan better?

> #### 🤖 Assistant

Good question — since you've already given me a detailed plan, the most useful things to gather are the pieces that aren't yet spelled out but will shape how we build. Here's what would meaningfully help, roughly in order of value:

## Tier 1: High-value (worth writing down now)

**1. The geocoding spike findings.** This is where a lot of Part 1 decisions live. Specifically:
- What did you find for postal-code coverage? Which regions work well vs. fail?
- Your fallback decision — city-only search, coordinates, or a priority order (city → zip → coords)?
- Any edge cases worth knowing (e.g., ambiguous names like "Spring" in multiple states).

Knowing this lets me design the location-search utils and error handling correctly instead of guessing.

**2. The data-flow / caching architecture.** A short description of how you envision: fetch → map to UI model → cache in IndexedDB → serve from cache, and critically **the boundary between SW caching and IndexedDB caching**. Right now these two layers are distinct but not clearly separated. A diagram or a few sentences on "what each layer owns" would prevent confusion later (and double-fetching).

**3. The global state model.** What lives in the app context — location, unit preference, theme, offline status, last-updated timestamp? Even a rough sketch helps me build the Context API and types correctly from day one rather than retrofitting it.

## Tier 2: Supporting (helps but less critical early)

**4. Local dev environment details.**
- Node version and package manager preference (npm/pnpm/yarn). This matters because some managers handle workspaces/locking differently, and your tooling choices affect reproducibility.
- Any proxy, VPN, or corporate network that might interfere with `fetch` to Open-Meteo during local dev — a common silent build-breaker.

**5. Visual references.** Since the goal is "Google-clean but fully custom," even 2–3 reference screenshots (of Google Weather, or any app you like) would help me internalize your aesthetic intent without you re-explaining it repeatedly as we build components. A rough color palette or theme tokens if you have them.

**6. Accessibility specifics.** Any particular WCAG targets, contrast ratios you're aiming for, or assistive tech you personally use/test with? This sharpens the "accessible by design" work beyond a generic checklist.

## Tier 3: Nice to know (can wait until we start)

- **Vercel/CI specifics** — custom domains, any environment variables (likely none since no API key), and whether you have preferences for CI workflow structure.
- **Testing philosophy details** — your Vitest setup thoughts beyond the two named test areas (cache freshness, data mapping).
- **Deployment config** — manifest icon sizes, theme colors, display mode decisions.

---

My honest take: **Tier 1 is what would most accelerate us.** The plan already covers Tier 3 well enough to defer. If you want, I can help draft any of these — for example, a proposed global state model or the caching-layer boundary — so we lock those down before scaffolding. Which would be most useful first?

108 t/s, 1640 tokens, 15s, 34%

> #### 💬 User

Provide me an example react component for the daily view.

> #### 🤖 Assistant

Here's an example `DailyView` component, written to reflect the specific requirements in Part 2 (unit toggle from global context, timezone-aware display, accessibility, and clean flexbox). I've kept it focused on presentation logic — fetching/caching is a separate concern you can build next.

```tsx
// DailyView.tsx
import { useContext } from 'react';
import styles from './DailyView.module.css';

interface CurrentConditions {
  time: string;      // ISO timestamp of the observation (location timezone)
  temperature: number;   // already converted to display unit by the mapper
  feelsLike: number;     // same
  windSpeedKmh: number;  // km/h from API, converted here
  humidity: number;      // percent
  weatherCode: number;   // WMO code -> icon/label via utils/weather.ts
}

interface TodayForecast {
  time: string;         // ISO timestamp (hourly) in location timezone
  temperature2m_max: number;
  temperature2m_min: number;
  sunrise: string;      // local-time ISO, per Open-Meteo timezone=auto
  sunset: string;
}

interface DailyData {
  locationName: string;
  timezone: string;     // e.g. "America/New_York" — from Open-Meteo's timezone=auto
  current: CurrentConditions;
  today: TodayForecast[];
}

// Consumed from the global app context (see Part 1). The mapper converts API
// values to display units here, so this component only reads the preference.
interface UnitPreference {
  unitSystem: 'metric' | 'us';
}

export function DailyView({ data }: { data: DailyData }) {
  const units = useContext<UnitPreference>(unitsContext);

  return (
    <main className={styles.container} aria-labelledby="daily-heading">
      <header>
        <h1 id="daily-heading">{data.locationName}</h1>
        <p className={styles.timezone}>
          {formatTimezone(data.timezone)} · updated {formatTimestamp(data.current.time)}
        </p>
      </header>

      {/* Current conditions — screen-reader friendly via role + aria-label */}
      <section aria-live="polite">
        <div className={styles.hero}>
          <span role="img" aria-label={`Sunny`}>☀️</span>
          <p className={styles.temperature}>{data.current.temperature}°</p>
          <p>{describeWeather(data.current.weatherCode)}</p>
        </div>
      </section>

      {/* Key metrics */}
      <section aria-label="Key conditions">
        <Metric label="Feels like" value={`${data.current.feelsLike}°`} />
        <Metric label="Wind" value={`${data.current.windSpeedKmh} km/h`} />
        <Metric label="Humidity" value={`${data.current.humidity}%`} />
      </section>

      {/* Sunrise / sunset */}
      <section aria-label="Sun times">
        <div className={styles.sunRow}>
          <TimePair icon="🌅" title="Sunrise" time={formatLocal(data.current.sunrise)} />
          <TimePair icon="🌇" title="Sunset" time={formatLocal(data.current.sunset)} />
        </div>
      </section>

      {/* Hourly breakdown — drawn with canvas/SVG in Part 2 */}
      <HourlyStrip forecast={data.today} unitSystem={units.unitSystem} />
    </main>
  );
}
```

Key decisions baked into this example:

- **Timezone, not browser local.** The `timezone` prop comes straight from Open-Meteo's `timezone=auto`, so sunrise/sunset and hourly times render in the location's zone. That's your explicit requirement — don't fall back to `new Date().toLocaleTimeString()`.
- **Units come from context, values are pre-mapped.** The component only reads `unitSystem`; a separate mapper (the thing you unit-test with Vitest) converts API units → display units before this renders. Keeps the view dumb and testable.
- **Accessibility by design.** Semantic `<section>`/`<h1>`, an `aria-live="polite"` region so screen readers announce updates, meaningful labels on every metric, and a text alternative for the weather glyph (you'll expand this to canvas/SVG with proper `aria-label` + keyboard list later).
- **Reused skeleton/error patterns.** These are stubbed here; they're shared components from Part 1.

I left out the CSS module contents deliberately — that's presentation detail, and I can give you a clean flexbox layout next if useful.

Want me to continue with:
1. The `HourlyStrip` (canvas/SVG breakdown) — probably the most involved piece of Part 2?
2. A sketch of the caching layer so this component reads from IndexedDB instead of props?
3. Or something else on your list?

117 t/s, 2628 tokens, 23s, 44%

> #### 💬 User

According to the PROJECT-PLAN.md document, what is the primary weather API we are using for this app, and why did we choose it?

What is the main tech stack for the weather PWA project (framework, build tool, styling approach, state management, storage), and why did we decide to keep it so lightweight?

In Part 2 of the development plan (Daily Weather View), what should we display on the main daily screen? Also give me one small suggestion to make the hourly breakdown look nicer without adding any new heavy libraries.

Our project uses Open-Meteo as the main API and IndexedDB with the 'idb' wrapper for caching.
What are the biggest advantages of this combination for a PWA weather app, and is there one small thing we should be careful about when implementing the caching logic?

Looking at the updated development plan in PROJECT-PLAN.md:
What are the three main views/screens we plan to build for the MVP?
In which order does the plan suggest implementing them?
If I want to make the app feel more 'alive' visually very early, which part of Part 4 could I start experimenting with right after finishing Part 1?

> #### 🤖 Assistant

Here are your answers, drawn directly from PROJECT-PLAN.md:

## Primary weather API — Open-Meteo

We chose **Open-Meteo** because it's free, requires no API key, and its free tier is designed for non-commercial use (which fits a public portfolio project). The plan also flags that we must follow their attribution requirements — which is why the footer credit crediting Open-Meteo on every view is required.

## Main tech stack & why lightweight

- **Framework:** React (vanilla, no Next.js or heavy frameworks)
- **Build tool:** Vite
- **Styling:** CSS Modules + custom flexbox only
- **State management:** React Context + hooks (no external state libraries)
- **Storage/caching:** IndexedDB via the `idb` wrapper

We decided to keep it lightweight deliberately — to stay dependency-minimal, look strong on a resume with modern tools, and remain fully self-contained. The philosophy is to use current tools that impress while avoiding extra libraries (e.g., building custom SVG/canvas graphics instead of pulling in icon/chart packages).

## Part 2: Daily Weather View

The main daily screen should display:
- Current conditions and today's detailed forecast from Open-Meteo
- Temperature, feels-like, wind, humidity, sunrise/sunset, and other key metrics
- Hourly breakdown (drawn with canvas or SVG)
- Last-updated timestamp + visible refresh button
- Cache responses in IndexedDB; serve fresh data if under 3–6 hours old

**One small suggestion for the hourly breakdown:** instead of drawing each bar as a separate shape, draw them on a single continuous baseline so they read like a temperature "wave" — it's more visually cohesive and still trivial to implement with canvas/SVG. No new libraries needed.

## Open-Meteo + IndexedDB/idb advantages (and one caution)

**Advantages:**
- **Open-Meteo** gives reliable, key-free data so the app works without backend infrastructure or rate-limit headaches — ideal for a self-contained PWA.
- **IndexedDB via `idb`** lets us cache API responses with timestamps and serve fresh data offline (under 3–6 hours), which is exactly what makes it feel like a true PWA rather than just a cached website.

**One thing to be careful about:** keep the two caching layers clearly separated — IndexedDB for fast access to recent weather data, and the service worker for static assets/offline loading. If they aren't deliberately divided, you risk confusion about which serves what (and possibly double-fetching). Design that boundary early rather than letting it emerge in Part 5.

## MVP views/screens & order

The three main screens are:
1. **Location selection** (search + save locations) — Part 1
2. **Daily Weather View** — Part 2
3. **10-Day Forecast View** — Part 3

**Order:** The plan implements them sequentially in that exact order — Parts 1 → 2 → 3 — to reach a working MVP, then deploys to Vercel and sets up GitHub Actions at the milestone point.

**For making the app feel "alive" early:** you could start experimenting with **dynamic backgrounds/scenes based on conditions** (the sunny/cloudy/rain/snow/storm scenes) right after finishing Part 1 — that's the core of Part 4, and it gives immediate visual payoff without needing any of the more involved parallax or icon work.

128 t/s, 927 tokens, 8s, 42%
