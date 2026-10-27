# Ornith 1.5 9B
Model: ornith-1.5-9b
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

Got it — I've read through your Weather PWA plan carefully and I'm standing by for your next instructions. No code or examples unless you ask.

A few things I want to flag so we're aligned when you do start:

**On the version decision (Part 1)** — Your plan leaves this deliberately open, which is good. When you get there, my recommendation would be to check current stable majors on npm and lean toward the latest React/Vite/react-router set *if* they're compatible with each other, since that reads as more current on a resume. But staying on 18/5.4 is perfectly defensible if it keeps things stable. Either way, record the reasoning in the README as you've planned.

**On scope sequencing** — Your flow (MVP first via Parts 1–3, then polish/PWA) is sound and realistic. One thing worth keeping in mind: Part 5 says to register the service worker *in that part*, not later — good call, because offline behavior can't be tested until it exists.

**On Open-Meteo compliance** — You've correctly captured the non-commercial/free-tier attribution requirement, which is easy to trip over and worth getting right early (the footer credit in Part 1 handles this).

**A couple of things I'll watch for when you start:**
- The geocoding spike (Part 1) will likely surface real-world gaps in postal-code coverage — your fallback plan (city + coordinates) is the pragmatic move.
- Time zone handling (`timezone=auto`) is a common source of subtle bugs, so testing with a location outside your own zone early is smart.

I'm ready whenever you are. You can start with anything from:
- Project scaffolding and folder structure
- Component ideas
- IndexedDB schema examples
- Service worker caching strategy
- Or any other part of the plan you'd like to tackle first

Just let me know what you want to work on next, and whether you'd like code/examples or continued planning.

118 t/s, 535 tokens, 5s, 19%

### User

What do you think about the app plan? Does it sound good, any issues, any improvements?

### Assistant

Overall, this is a strong plan — well-scoped, realistic for a portfolio piece, and thoughtful in ways that most projects aren't (accessibility as ongoing work, testing + CI included, deliberate version policy). Here's my honest read on where the risks are and what I'd adjust.

## What's genuinely good

- **Accessibility throughout, not as a final pass.** This is rare and worth keeping.
- **Version policy left open** — leaning latest in 2026 reads better on a resume than pinning to 18/5.4 unless there's a real reason not to. Good instinct.
- **Two caching layers are acknowledged**, which is the honest way to do it (SW for static/offline assets, IndexedDB for structured app data + freshness logic).
- **Geocoding spike before committing** — smart, because postal-code gaps will bite you otherwise.

## The real risks I'd flag

**1. Part 4 is your biggest time trap.** "Dynamic scenes," hand-built SVGs/icons for *every* condition (rain levels, snow, storm), plus parallax across all of them — that's a lot of custom visual work crammed into one part. Parallax especially tends to consume disproportionate effort and can eat Parts 1–3 combined. My suggestion: treat Part 4 as "impressive but bounded." A few clean SVG icons + CSS gradient scenes get you portfolio-ready faster than a full parallax scene system. Keep parallax as the *showcase* element, not the foundation.

**2. Weather staleness UX is a design decision you should make now.** This matters more for your app than almost any other because weather's entire point is *current* conditions. If offline mode serves yesterday's forecast, showing "Using cached data" can actively mislead someone about what to wear. Decide early: does cached weather show with clear staleness labeling and a prominent refresh? Or degrade gracefully (e.g., last-known + big "stale" indicator)? Don't defer this — it shapes the Part 5/6 UX.

**3. Two caching layers need crisp division of labor.** SW caches network responses; IndexedDB caches API data with freshness logic. If these overlap, you'll end up double-caching or fighting each other (e.g., SW serves a cached weather response while IndexedDB has its own). Document the split explicitly in your architecture note before coding — it prevents rework later.

## Smaller things to watch

- **Canvas/SVG vs accessibility tension.** Your philosophy says custom graphics, but your accessibility section demands meaningful labels + text alternatives for charts/graphics. Be deliberate about which visuals are decorative (`aria-hidden`) vs. informative (real labels). Parallax transforms on interactive elements also complicate focus management — worth planning now.
- **Time zone edge cases.** `timezone=auto` is fine, but DST transitions and multi-zone locations can surprise you. Sunrise/sunset near extreme latitudes can be weird too. Your "test with a location in another zone" plan covers this well.
- **Geolocation needs secure context.** Vercel gives you HTTPS so production's fine; just remember it won't fire on plain `http://localhost` unless your dev setup handles that (Vite + modern browsers treat localhost as secure, so likely OK).
- **The SW update flow is a real learning curve.** The "update available" banner requires intercepting activation events and getting `skipWaiting`/`clients.claim` right. It's doable but non-trivial — budget time for it in Part 5 rather than assuming it'll be easy.

## Minor additions worth considering

- Add an explicit **data-layer diagram** to your README/architecture note early (SW vs IndexedDB responsibilities) — directly addresses risk #3 above.
- Since freshness logic is time-based, a small unit test on the staleness boundary (e.g., exactly at 6 hours) will catch subtle off-by-one bugs cheaply.

---

Bottom line: keep it as-is structurally, but **watch Part 4 scope and make the offline-staleness decision early** — those are the two things most likely to derail a smooth MVP→polish flow. Want me to dig into any of these next?

107 t/s, 2935 tokens, 28s, 36%

### User

What tech documentation would help you understand the app plan better?

### Assistant

Good question — since you've already given me a detailed plan, here's where the gaps are that would most improve my understanding when we start implementing:

## 1. Design & visual direction (highest value)
This is your portfolio centerpiece (Part 4), and visuals are subjective, so this matters more than anything else for avoiding rework. Specifically:
- **Reference images or screenshots** of apps/websites you like *and* dislike — even rough mockups help me match the "clean Google-style" feel to something concrete rather than guessing.
- **Color palette preferences** — do you have specific colors, or should I propose one? Weather scenes (sunny/cloudy/rain/snow) will drive your whole visual language.
- **Typography choices** — font families, sizes, spacing rhythm.

## 2. Environment & tooling specifics
You've listed the tools but not the setup details that affect scaffolding:
- **Node.js version** on your machine (affects which Vite/React majors are compatible).
- Whether you have a **GitHub account and Vercel set up**, or if we should plan for those.
- Your comfort level with **command-line / Git Bash workflows**.

## 3. Open-Meteo API exploration status
The geocoding spike (Part 1) is the first real technical decision point:
- Have you already **explored the Open-Meteo endpoints** and seen response shapes, or should we plan to do that together?
- Any specific fields/metrics you're *excited* about beyond what's in the plan (e.g., UV index, precipitation probability)?

## 4. Constraints & priorities
These shape how we sequence work:
- **Timeline** — is there a deadline or portfolio submission date?
- **Effort per week** and whether this is solo.
- Any features you're *particularly* excited about that aren't in the plan yet (nice-to-haves like share functionality, weather history).

## 5. Testing depth & comfort level
You've included Vitest + CI, but:
- How comfortable are you with **writing unit tests**? This determines how much I should guide vs. just provide test structure.
- Do you want to prioritize testing the **caching/freshness logic** (which is time-based and error-prone) or cover more broadly?

## 6. Accessibility target
You treat this as ongoing, which is great — but a concrete target helps:
- Are you aiming for **WCAG 2.1 AA**? Do you have a screen reader to test with, or will Lighthouse be your main check?

---

If I had to prioritize, the first three (design references, Node version, and Open-Meteo exploration status) would give me the biggest lift when we start. The rest can come as we go.

Want to walk through any of these now, or shall we just dive into Part 1 scaffolding and figure out the environment details then?

111 t/s, 1531 tokens, 14s, 33%

### User

Provide me an example react component for the daily view.

### Assistant

Since you've explicitly asked for one now, here's an example. I'll keep it focused rather than dumping the entire daily view into a single component — Part 2 has several concerns (units, time zones, accessibility), so this slice demonstrates those patterns without becoming unwieldy. It's illustrative, not production-ready.

```tsx
import type { ReactNode } from "react";

interface WeatherMetricsProps {
  // Values come from the Open-Meteo daily response; units are resolved by the app.
  temperature: number | null;   // °C from API (convert to °F client-side)
  feelsLike: number | null;
  windSpeedKmh: number | null;
  humidity: number | null;      // percent, 0–100
  sunrise: string | null;       // ISO local-time string in the location's zone
  sunset: string | null;
  timezone: string;             // e.g. "America/New_York" from timezone=auto
  unitSystem: "metric" | "imperial";
}

function WeatherMetrics({ ... }: WeatherMetricsProps) {
  const fmt = (value: number, kind: "temp" | "wind") => {
    if (unitSystem === "metric") return `${Math.round(value)} ${kind === "temp" ? "°C" : "km/h"}`;
    // Convert °C→°F and km/h→mph here so the API stays unit-agnostic.
    const f = kind === "temp" ? (value * 9) / 5 + 32 : value * 0.621371;
    return `${Math.round(f)} ${kind === "temp" ? "°F" : "mph"}`;
  };

  const fmtTime = (iso: string | null, label: string) => {
    if (!iso) return null;
    // Render in the location's own zone, not the browser's.
    return new Intl.DateTimeFormat("medium", {
      timeZone: timezone,
      hour: "numeric",
      minute: "2-digit",
    }).format(new Date(iso));
  };

  const metric = (label: string, value: ReactNode) => (
    <div className="metric">
      <dt>{label}</dt>
      <dd aria-hidden="true">{value}</dd>
    </div>
  );

  return (
    <section className="metrics" aria-label="Current conditions">
      {metric("Temperature", fmt(temperature!, "temp"))}
      {metric("Feels like", fmt(feelsLike!, "temp"))}
      {metric("Wind", fmt(windSpeedKmh!, "wind"))}
      {metric("Humidity", `${humidity ?? 0}%`)}
      <div className="sun">
        <dt>Sunrise</dt>
        <dd>{fmtTime(sunrise, "Sunrise")}</dd>
        <dt>Sunset</dt>
        <dd>{fmtTime(sunset, "Sunset")}</dd>
      </div>
    </section>
  );
}

export default WeatherMetrics;
```

A few deliberate choices worth flagging:

- **Unit conversion happens client-side.** The API always returns metric values, so the component takes a `unitSystem` prop and converts on display. This keeps your data layer unit-agnostic — you store one set of numbers in IndexedDB regardless of user preference.
- **Timezone is passed as a prop**, not read from `Intl.DateTimeFormat().timeZone`. That's because Open-Meteo returns the location's zone via `timezone=auto`, and you want to render in *that* zone, not the browser's.
- **`aria-hidden` on decorative values** — the metric labels are `<dt>`/`<dd>` pairs (semantic), but the numeric display is visually hidden from assistive tech since it's redundant with the label. Adjust if your design needs the value announced separately.

Given you're still in planning and haven't scaffolded yet, I'd suggest we don't lock into this exact shape until Part 1 establishes your folder structure and context — e.g., where `unitSystem` comes from (Context) and how props flow down to an hourly breakdown component.

Want me to show the **hourly breakdown** piece next (canvas/SVG), or something else?

118 t/s, 1730 tokens, 15s, 39%
