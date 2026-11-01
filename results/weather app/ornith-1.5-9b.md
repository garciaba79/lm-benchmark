# Ornith 1.5 9B
Model: ornith-1.5-9b
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

Got it — I've read through your Weather PWA plan carefully and I'm standing by for your next instructions. Here's a quick summary of what I understand so you can confirm or redirect:

**Scope & stack**
- Vanilla React + TypeScript, Vite build tool, react-router-dom routing, Context/hooks state (no external state libs)
- Open-Meteo as the weather API (free tier, non-commercial, attribution required)
- IndexedDB via `idb` for caching/storage, manual PWA setup (manifest + service worker), Biome + Vitest + GitHub Actions tooling

**Phasing**
- Phase 1: MVP foundation — Parts 1–3 (setup, daily view, 10-day forecast → deploy to Vercel)
- Phase 2: Polish & PWA — Part 4 (visuals), then Parts 5–6 (caching/offline, installability)
- Future modular parts (7–12) as stretch goals

**Key decisions flagged in the plan that I'll respect when you ask me to dig in:**
- Version policy: deliberate React/Vite/react-router major choice (not just `latest`)
- Geocoding spike first — postal code coverage is inconsistent, so city + coordinates fallbacks are expected
- Time zones via `timezone=auto` from Open-Meteo, not the browser's local zone
- Reduced-motion support throughout; transform-based parallax instead of `background-attachment: fixed`
- Error boundaries wrapping views; reusable loading/empty/error states

**One thing worth flagging for when we get to scaffolding:** since you're on Windows 11 with Git Bash, a couple of the tooling choices (Biome config format, service worker registration in Vite) have small gotchas that are easy to trip over early — but I'll only raise these if they come up as part of your next instruction.

I'm ready whenever you'd like to start. A few ways we could begin:
- Scaffold the project structure and folder layout first
- Work through the Open-Meteo geocoding spike (search strategy, fallbacks)
- Draft the IndexedDB schema or service worker caching strategy
- Brainstorm component/view ideas

Just tell me where you'd like to start.

118 t/s, 601 tokens, 6s, 19%

> #### 💬 User

What do you think about the app plan? Does it sound good, any issues, any improvements?

> #### 🤖 Assistant

Overall this is a strong, well-thought-out plan — genuinely portfolio-grade in ambition and clarity. You've done the hard part: scoping something realistic while still hitting the things that look good on a resume (custom visuals, PWA/offline, accessibility, CI). I'll give you my honest read though, because "does it sound good" deserves more than agreement.

## What's working well

- **The phased structure is smart.** MVP-first with deploy + CI at the milestone means you always have something shareable, and polish/PWA come later when they're lower-risk to add incrementally.
- **Open-Meteo is a great choice** for this — no key, free tier, and it handles time zones natively via `timezone=auto`, which saves you real work in Part 2. Your instinct to test with a location in a different zone than yours is exactly right; that's one of the trickier bits and you've flagged it correctly.
- **Accessibility as ongoing work** rather than a final pass is the mature approach — most people bolt it on at the end and it shows.
- **Custom SVG/canvas over libraries** is a genuine portfolio differentiator, and avoiding `background-attachment: fixed` shows you know your mobile constraints.

## Real concerns worth thinking about

**1. Scope creep risk in Phase 2.** Parts 4–6 are a lot for one project — custom visuals *and* full caching *and* service worker *and* offline *and* installability. PWA is where projects tend to balloon: iOS Safari install testing, the update-prompt flow, and pull-to-refresh fallbacks are all fiddly and can eat time unexpectedly. My suggestion: treat Parts 5–6 as "nice if you have time" rather than a hard Phase 2 deliverable. Better to ship a polished daily view + forecast that works online than a half-finished offline system.

**2. The version policy note is more consequential than it reads.** You say "either latest or older is fine," but there are real compatibility landmines:
   - If you go **latest React (19)**, react-router-dom v6 has known issues with the new router API — and react-router **v7** now exists specifically for React 19. Mixing v6 + React 19 is a footgun.
   - `vite-plugin-pwa` has had compatibility friction with newer Vite majors, which matters since you list it as an optional fallback in Part 6.
   
   So "check current versions" should really be "check version *compatibility*," not just "what's newest."

**3. Open-Meteo reliability.** It's a public research API — occasionally slow or flaky, and the free tier has rate limits. For a portfolio piece you want it to look reliable. I'd at least build in awareness of this (and your Part 7 plan is the right long-term answer), even if you don't implement multi-API support now.

**4. IndexedDB caching adds real complexity.** The freshness logic is cleanly testable, but serving from cache on load across a service worker + `idb` combo — especially in Vite's dev environment with HMR — can get subtle and hard to debug. It's fine for a portfolio piece, just be ready to spend time here.

## Smaller things I'd add or sharpen

- **First-visit UX matters most.** Crestview, FL as the default is fine as placeholder, but that prompt-to-change interaction is literally the user's first touch with your app — make it feel good there and it sets the tone for everything else.
- **Denied geolocation needs a graceful path**, not just an error state. Since location is central to this app, denial should immediately offer search rather than leaving them stuck. You flagged handling it; I'd push on making the fallback UX clean.
- **Consider one e2e test** (Playwright) for the offline/refresh flow — unit tests cover logic well, but the service worker + IndexedDB behavior is exactly the kind of thing that's hard to catch without an integration pass. Optional, but high value for a PWA.
- **SEO/meta tags** are cheap wins for a publicly deployed SPA (Open Graph, descriptions) even though they don't affect your stated goals — worth 15 minutes.

## My honest bottom line

The plan is good and I'd lean into it as-is. If I were picking where to spend my energy first, I'd **trim Phase 2 scope** (Parts 4–6 are the riskiest) and **resolve the version compatibility question deliberately before scaffolding**, since that decision ripples through every dependency choice. Everything else is solid — you've thought about the right edge cases (time zones, reduced motion, error boundaries, attribution).

Want me to dig into any of these next? For example, I could help you reason through the React/Vite/react-router version matrix so you make that call with confidence, or sketch out how to keep Phase 2 scope realistic.

102 t/s, 2412 tokens, 24s, 34%

> #### 💬 User

What tech documentation would help you understand the app plan better?

> #### 🤖 Assistant

Good question — and since you've already given me a thorough plan, I'd rather tell you what's genuinely missing than ask for the basics that are already covered. Here's what would meaningfully sharpen my understanding, roughly in order of value:

## 1. The version decision (highest priority)
The plan deliberately defers this ("check npm and decide"), but it's actually the single most consequential unknown because it ripples through every dependency. Specifically I'd want to know once you've decided:
- **React 18 vs 19** — this matters a lot, since React 19 has known friction with react-router-dom v6 (and v7 now exists specifically for React 19). Picking the wrong combo is a footgun.
- **Vite 5 vs 6**, and whether you've checked `vite-plugin-pwa` compatibility with whichever Vite major you land on — since that plugin is your optional fallback in Part 6.

If you'd rather not decide yet, I can research the current stable versions and their compatibility matrix for you so the decision is informed rather than arbitrary.

## 2. Visual direction
"Google's clean style" is a starting point but pretty vague — and since Part 4 is all custom visuals, matching your actual taste matters more than guessing. A quick reference would help:
- **A link or screenshot** of something you like (a real app, a design you admire). Even one image tells me a lot about spacing, density, and tone.
- Rough preferences on **color palette**, **typography feel**, and **layout density**.

## 3. The complete data surface
You listed the core metrics per view (temp, feels-like, wind, humidity, sunrise/sunset), but I'd want the full list to scope the mapping logic correctly — things like precipitation probability, UV index, pressure, visibility, cloud cover, etc. Knowing exactly what you intend to display on each screen prevents scope creep and clarifies what "daily view" vs "forecast drill-down" should contain.

## 4. PWA specifics (for Parts 5–6)
A few concrete decisions that affect implementation:
- **Display mode** — standalone vs fullscreen?
- **Theme color / accent colors**, and whether you want maskable icons.
- Your preference on the **update flow** — banner ("reload to update") vs auto-activate-on-next-launch.

## 5. Testing philosophy (optional)
I suggested adding an e2e test for the offline/refresh flow beyond Vitest unit tests. Knowing whether you're open to that, or want strictly unit-level testing, helps me plan realistically.

---

**What I'd skip asking about:** folder structure conventions, exact Biome rules, and most of the accessibility specifics — those are things we can decide together as we build, and they don't block understanding the plan itself.

If you want to move fast, the two that matter most right now are **#1 (versions)** and **#2 (a visual reference)**. Want me to go research current React/Vite/react-router compatibility so you have a concrete recommendation for #1?

110 t/s, 1973 tokens, 18s, 38%

> #### 💬 User

Provide me an example react component for the daily view.

> #### 🤖 Assistant

Here's a representative Daily View component built to match your stack — vanilla React + TypeScript, Context-driven props, CSS Modules, flexbox layout. I've kept the component presentational (it receives typed data rather than doing its own fetching), which keeps it testable and matches how you'd want Part 2 structured.

## Types (`types/weather.ts`)

```typescript
// WMO weather codes mapped to human-readable conditions + rain levels
export type WeatherCondition = 'clear' | 'cloudy' | 'fog' | 'rain' | 'snow' | 'storm';

export interface DailyWeather {
  time: string;
  temperature_2m_max: number;
  temperature_2m_min: number;
  weather_code: number;
  apparent_temperature: number;
  relative_humidity_2m: number;
  wind_speed_10m: number;
  sunrise: string;
  sunset: string;
}

export interface UnitPreferences {
  temperatureUnit: 'C' | 'F';
  windUnit: 'kmh' | 'mph';
}

// Open-Meteo returns timezone info at the top of every response
export interface TimezoneInfo {
  tz: string; // e.g. "America/New_York" — this is what you display, not browser local time
  offset_string: string;
}
```

## Unit helper (`utils/units.ts`)

This one's small but worth isolating because it comes up repeatedly (daily view + forecast drill-down) and your plan wants it unit-tested.

```typescript
export function convertTemperature(celsius: number, unit: 'C' | 'F'): number {
  return unit === 'F' ? celsius * 9 / 5 + 32 : celsius;
}

export function formatWindSpeed(kmh: number, unit: 'kmh' | 'mph'): string {
  const value = unit === 'mph' ? kmh * 0.621371 : kmh;
  return `${value.toFixed(0)} ${unit}`;
}
```

## Daily View component (`views/DailyView.tsx`)

```tsx
import type { DailyWeather, TimezoneInfo } from '../types/weather';
import { convertTemperature, formatWindSpeed } from '../utils/units';
import './DailyView.module.css';

interface Props {
  locationName: string;
  timezone: TimezoneInfo;
  day: DailyWeather;
  unitPrefs: UnitPreferences;
}

export function DailyView({ locationName, timezone, day, unitPrefs }: Props) {
  const temp = convertTemperature(day.temperature_2m_max, unitPrefs.temperatureUnit);
  const feelsLike = convertTemperature(day.apparent_temperature, unitPrefs.temperatureUnit);

  return (
    <section aria-labelledby="daily-heading" className="daily-view">
      <header>
        <h1 id="daily-heading">{locationName}</h1>
        <p className="tz-label">
          {timezone.tz} · {day.time} local time
        </p>
      </header>

      <div className="hero-metrics" role="group" aria-label="Current conditions">
        <div className="temp-hero">
          <span className="sr-only">{Math.round(temp)} degrees</span>
          {temp.toFixed(1)}°
        </div>
        <p className="feels-like">Feels like {feelsLike.toFixed(1)}°</p>
      </div>

      <dl className="metrics-grid">
        <Metric title="High / Low" value={`${Math.round(temp)}° / ${Math.round(convertTemperature(day.temperature_2m_min, unitPrefs.temperatureUnit))}°`} />
        <Metric title="Humidity" value={`${day.relative_humidity_2m}%`} />
        <Metric title="Wind" value={formatWindSpeed(day.wind_speed_10m, unitPrefs.windUnit)} />
        <Metric title="Sunrise" value={day.sunrise} />
        <Metric title="Sunset" value={day.sunset} />
      </dl>
    </section>
  );
}

function Metric({ title, value }: { title: string; value: string }) {
  return (
    <div className="metric">
      <dt>{title}</dt>
      <dd>{value}</dd>
    </div>
  );
}
```

## `DailyView.module.css`

```css
.daily-view { padding: var(--spacing-lg); }

.hero-metrics { display: flex; align-items: baseline; gap: var(--spacing-md); }
.temp-hero { font-size: var(--font-display-xl); font-weight: 700; margin: 0; }
.feels-like { color: var(--text-muted); margin: 0; }

.metrics-grid {
  display: flex; flex-wrap: wrap; gap: var(--spacing-sm);
}
.metric { min-width: 120px; }
.metric dt { font-size: var(--font-caption); color: var(--text-muted); }
.metric dd { margin: 0; font-weight: 600; }

.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); border: 0; }
```

---

## How this maps to your plan's Part 2 requirements

- **Time zones** — Open-Meteo already returns `timezone.tz` via `timezone=auto`, so the component just displays it. No manual conversion needed (good news).
- **Unit toggle** — `unitPrefs` is passed in from Context; the actual storage lives in IndexedDB elsewhere, and this helper is exactly what your Vitest unit tests would cover.
- **Loading/error states** — I left those out of this component on purpose: they belong at the view/hook layer (e.g., a wrapper that renders skeletons while fetching). The component assumes valid data so it stays focused.

## A couple of things worth deciding before you build this

1. **Where does caching plug in?** This component is presentational, so the fetch + IndexedDB freshness logic lives in a hook or view layer above it. That's where Part 5's "check timestamp on load" belongs — I'd keep them separate rather than baking cache into the component.
2. **The hourly breakdown** (canvas/SVG) you mentioned is a natural next slice off this same structure — want me to sketch that too?

Want me to show the data-fetching layer/hook next, or move on to something else from your plan?

122 t/s, 2911 tokens, 24s, 47%
