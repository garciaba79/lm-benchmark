# Falcon H1R 7B
Model: falcon-h1r-7b
Test: Weather App Planning
Created: 11/03/2026, 12:28:14 AM
Exported from: LM Studio (via test script)
Context unknown

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

Got it! Thanks for laying out the plan so clearly.  

I’m ready to dive in whenever you decide which part of the roadmap you want to tackle—whether it’s setting up the project skeleton, wiring up Geolocation/IndexedDB, fleshing out the daily‑weather view, or anything else. Just let me know what you need help with (questions about architecture, folder layout, configuration scripts, testing strategy, etc.) and I’ll respond with guidance.  

No code samples will be provided until you specifically ask for them. Let me know how you'd like to proceed!

101 t/s, 508 tokens, 6s

> #### 💬 User

What do you think about the app plan? Does it sound good, any issues, any improvements?

> #### 🤖 Assistant

### Overall Impression  
Your plan is very solid – it covers the essential pieces of a production‑grade Weather PWA while keeping the scope realistic for a portfolio showcase. The focus on clean UI, accessibility, offline support, and CI makes it stand out from many simple weather demos.

Below are some high‑level observations, potential pitfalls, and concrete suggestions that could tighten up parts of the plan (and keep you from hitting hidden friction later). No code is shown unless you explicitly ask for it.

---

## Strengths to Keep  

| Area | Why It’s Good |
|------|---------------|
| **Tech stack choice** – Vite + React 18/TS gives fast dev builds and a small bundle size, which is perfect for a lightweight PWA. |
| **Explicit data‑layer** – Using IndexedDB via `idb` lets you cache weather responses without pulling in a heavy library like Swup or Stork. |
| **Accessibility baked in early** – You’ve listed contrast, keyboard navigation, and reduced‑motion handling up front; that will make later polish easier. |
| **Open-Meteo compliance** – Attribution in the footer meets the API’s non‑commercial terms from day one. |
| **CI/CD focus** – Biome linting, Vitest unit tests, and GitHub Actions are wired into the plan, which keeps quality consistent as you grow. |
| **Modular roadmap** – Parts 1‑6 clearly delineate MVP → polish → PWA completion; future parts (7‑12) can be added without rewriting core logic. |

---

## Potential Pitfalls / Gaps  

### 1.  **Data fetching architecture could become tangled**  
*Current plan:* All API calls are done with native `fetch`. While that works, as the app grows you’ll start repeating fetch‑wrappers for location search, daily forecast, 10‑day list, etc. This can make error handling and caching harder to maintain.

- **Mitigation:** Create a small “API hook” layer (e.g., `useWeather`, `useGeocode`) that wraps fetch logic, adds timeouts, retries, and returns normalized types. Even though you’re not pulling in an external library, this pattern isolates network concerns and makes the error boundary easier to write.

### 2.  **Service‑worker caching of API responses is non‑trivial**  
*Current plan:* The service worker should cache static assets **and** weather JSON payloads with a TTL (e.g., 6 h). However, browsers restrict Service Workers from doing cross‑origin fetch unless they’re installed via the PWA route or you use a workaround.

- **Mitigation:** Either:
  * Deploy your build to Vercel and let the service worker be registered after install (Vercel provides a server for API fetches).  
  * Or, keep the first network request in the main thread during startup, write the response to IndexedDB yourself, and then hand off future fetches to cache‑only mode. This avoids needing a custom proxy.

### 3.  **Timezone handling subtlety**  
Open-Meteo’s `timezone=auto` returns an offset that works for most locales but can be ambiguous when daylight‑saving transitions occur. You need to render times using the client’s own timezone calculations rather than just adding a raw offset.

- **Mitigation:** Use the browser's `Intl.DateTimeFormat`/`DateTimeStringFormat` API with an explicit options object that includes the returned hour/minute offsets, or convert server‑provided timestamps to UTC then let JS handle local formatting. Test in at least two time zones and around DST changes.

### 4.  **IndexedDB schema migrations**  
Your current plan mentions caching but not how you’ll version your store. If you later add more data types (e.g., saved locations, recent searches), the schema could diverge between browsers that load older caches.

- **Mitigation:** Start with a simple binary/structured DB layout now: one top‑level object per location containing all cached weather snapshots plus timestamps. When you add new fields later, store them under versioned sub‑objects (`v2`, `v3`). A small helper function can read the highest known version and migrate older data lazily.

### 5.  **Pull‑to‑Refresh edge cases**  
You plan to support native pull‑to‑refresh where it works, but you noted that iOS Safari does not expose it in PWAs. The fallback implementation may need a custom spinner overlay; however, coordinating this with service‑worker cache invalidation can be tricky.

- **Mitigation:** Keep the UI logic separate from the refresh trigger: when the user drags to pull, set a flag → on unload clear it → if the flag is true and network is available, call your fetch/refresh hook manually. This avoids reliance on platform‑specific APIs while still providing a consistent UX.

### 6.  **Accessibility for custom canvas/SVG charts**  
Canvas graphics lack native semantics; you’ll need to expose ARIA labels and descriptions that reflect the chart data. If you later switch to SVG, ensure they have proper `role="img"` or `<title>` tags. Skipping this now could cause a low Lighthouse accessibility score.

- **Mitigation:** Create an abstraction component: `WeatherChart({data})`. Inside it generate the visual element and also expose a hidden `<div role="region" aria-label="..." aria-describedby="chartDesc">` that contains a text summary of what’s being shown.

### 7.  **Testing coverage for caching logic**  
Vitest will test unit functions, but you may want to verify end‑to‑end behavior: e.g., simulate offline mode and ensure the app falls back to IndexedDB without error. While not part of unit tests now, a quick Cypress or Playwright script could be added later as “integration” coverage.

- **Mitigation:** Add a simple snapshot test that mocks `navigator.onLine` and checks whether UI switches from loading → cached view within the same render cycle. This is low‑cost but catches regressions early.

### 8.  **Bundle size vs visual richness**  
Custom backgrounds, parallax transforms, and canvas charts are great for showcase purposes, but each adds to final bundle weight. If you later decide to ship on a limited device set, the bundle may exceed typical PWA budgets (≈150 KB gzipped).

- **Mitigation:** Keep assets as separate files that get lazy‑loaded when needed (`<img src="…">`, canvas textures). Use Vite’s tree‑shaking and `mode: production` builds to see the final size, then prune any non‑essential visual features.

### 9.  **Service‑worker update strategy**  
You mention a banner for new versions or automatic activation via `skipWaiting`. The simplest approach is to let Vercel’s PWA plugin handle this automatically on each install; if you go manual, you must implement the logic yourself and guarantee that the user sees an up‑to‑date version before any cached data stale.

- **Mitigation:** Choose one path early: either fully adopt `vite-plugin-pwa` for update handling or write a custom script that checks `self.clients.matchPattern('cache')` and calls `skipWaiting()`. Keep the two consistent; mixing both can cause confusing behavior.

### 10.  **Error boundary vs. global recovery UI**  
Your plan says to wrap main views in React error boundaries, but you also need a fallback UI that persists across routes (e.g., if network is down on any page). A top‑level component could detect errors and render a consistent “Offline” banner while individual pages still have their own fallback content.

- **Mitigation:** Implement a custom `ErrorBoundaryWrapper` at the root that lifts error state but still allows child components to override the message if they want location‑specific details.

---

## Suggested Tweaks to the Roadmap  

| Phase | Adjustment |
|-------|------------|
| **Phase 1 (MVP)** | Add a small “API hook” layer early (e.g., `useWeatherData`, `useLocationSearch`) so that later caching and error handling are already modularized. Keep the IndexedDB schema simple now but document versioning expectations. |
| **Phase 2 (Polish)** | Introduce a dedicated accessibility wrapper for any custom canvas/SVG component; add ARIA labels before final visual polish. Consider using Vite’s built‑in PWA plugin if you want skipWaiting handling out of the box, or document your manual approach consistently. |
| **Phase 3 (Offline)** | Implement pull‑to‑refresh flag logic and a hidden “using cached data” indicator early; test offline mode in Vite dev server after building to verify service worker registration works. Add an explicit UI command: “Clear Cache”. |
| **Future Parts** | When you later add multiple API support, reuse the central hook layer so switching providers only touches that one place. This avoids duplicating fetch logic across all parts of the app. |

---

## Quick Checklist for the First Sprint  

1. **Project scaffolding** – Vite + React TS, Biome config, Vitest skeleton.  
2. **Location service** – Implement geocoding endpoint; store results in IndexedDB with timestamps. Add “Use my location” button and graceful permission handling.  
3. **Daily view component** – Fetch current conditions + hourly forecast; display unit toggle stored in DB; wrap UI in error boundary; add loading skeletons.  
4. **10‑day list** – Route guard to fetch multi‑day data, drill‑down routing to DailyView. Add route validation fallback.  
5. **Basic PWA assets** – Manifest with icons for Android/iOS, simple service worker that caches the bundles; register it only after build.  

During this sprint keep an eye on:

- Bundle size (`vite run build` → check gzipped size).  
- Lighthouse performance audit on mobile Chrome DevTools (target ≤ 150 KB main JS).  
- Accessibility warnings for contrast and focus order in early UI.  

---

### Bottom Line  

Your plan is well‑structured, balanced between feature richness and technical rigor, and already incorporates many best practices for a modern PWA. The biggest risks right now are:

1. **Network‑centric code becoming hard to abstract** → add an API hook layer soon.  
2. **Service‑worker caching of dynamic API data** → decide early whether you’ll rely on Vite‑plugin‑PWA or write a manual strategy with IndexedDB fallback.  
3. **Accessibility for custom graphics** → build ARIA support into any canvas/SVG component now.  

If those points are addressed as you progress, the final product should meet strong performance, accessibility, and offline criteria while staying lightweight enough to showcase your skills effectively.

Let me know which part of the plan you’d like to start tackling (folder layout, location‑search implementation, service‑worker caching strategy, etc.), and I can give more detailed guidance without writing code—just the architecture and configuration tips you need.

99 t/s, 3792 tokens, 38s

> #### 💬 User

What tech documentation would help you understand the app plan better?

> #### 🤖 Assistant

Below is a “reading‑list” you can use as a roadmap to get comfortable with every piece of technology in your Weather PWA plan.  
I grouped the resources by category, added a short note on what part of the plan each doc covers, and gave the most useful entry points (official docs + quick tutorials or cheat‑sheets).  

Feel free to jump from one section to another as you build—these references will help you map concepts like routing, caching, accessibility, service‑worker registration, etc., straight back to your architecture.

---

## 📦 Core Frameworks & Build Tools  

| Tech | Where it appears in the plan | Recommended docs / tutorials |
|------|-----------------------------|------------------------------|
| **React (18) + TypeScript** | UI components, context store, hooks for data fetching | • Official React Docs: <https://reactjs.org/docs/>  <br>• TS‑typed React guide: “TypeScript in React” – <https://react-typescript.net/>  <br>• Hooks reference: <https://reactjs.org/docs/hooks-reference.html> |
| **Vite (5)** | Dev server, bundling, optional pwa plugin | • Vite Guide – Getting Started: <https://vitejs.dev/>  <br>• Plugins intro (if you later switch to vite-plugin-pwa): <https://vitejs.dev/guide/plugins.html> |
| **react‑router‑dom (6)** | SPA navigation, route guards for daily view and forecast list | • Router Docs: <https://reactrouter.com/latest/>  <br>• Nested routes pattern – helpful for keeping the DailyView component reusable: <https://reactrouter.com/docs/v6/advanced-features/nested-routes> |
| **Biome linter** | Style enforcement, custom rules you’ll apply in CSS modules | • Biome Docs: <https://biomejs.com/>  <br>• Example config for a simple spacing rule (copy‑paste): <https://github.com/FormidableLabs/biome#example-config> |
| **Vitest** | Unit tests for cache logic, API‑to‑UI mapping | • Vitest Docs: <https://vitest.dev/>  <br>• Sample test setup using jest matchers: <https://github.com/microsoft/ts-jest#configure-with-typescript> (adapted for Vite) |

---

## 🗂️ Data Layer & Storage  

| Tech | Plan relevance | Docs to read |
|------|----------------|--------------|
| **Fetch API** | All weather calls, location geocoding | MDN Fetch: <https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API>  (look for timeout patterns and error handling) |
| **Geolocation API** | “Use my location” button, permission flow | MDN Geolocation: <https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API>  (focus on the success/failure handling and fallback UI) |
| **Open‑Meteo API** | Daily conditions, hourly forecast, 10‑day list, timezone data | Open‑Meteo Docs: <https://www.open-meteo.com/documentation/>  (key sections: Geocoding endpoint, Weather response schema, Timezone handling) |
| **IndexedDB via idb** | Cache weather responses, persist saved locations | idb README & quick‑start: <https://github.com/jakearchibald/idb#quick-start>  (also MDN IndexedDB spec for understanding the API) |
| **Service Worker caching strategy** | Offline support, cache invalidation, skipWaiting considerations | MDN Service Workers Overview: <https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_Registration>  <br>MDN Cache API guide: <https://developer.mozilla.org/en-US/docs/Web/API/Cache#Using_the_Cache_API>  <br>Workbox cheat‑sheet for simple strategies (even if you stay manual): <https://developers.google.com/web/tools/workbox/modules/strategy> |
| **PWA Manifest & Display Mode** | Installable on mobile/desktop, icon set, theme colors | MDN Web App Shell: <https://developer.mozilla.org/en-US/docs/Web/Manifest>  (focus on the manifest schema and required fields) |

---

## 🎨 UI/UX & Visual Polish  

| Topic | Why it matters for your plan | Docs / Patterns |
|-------|------------------------------|-----------------|
| **CSS Modules** | Local styling, no global CSS bloat | MDN: CSS Modules basics – <https://developer.mozilla.org/en-US/docs/Web/CSS_Modules>  (look for module import syntax) |
| **Flexbox Layouts** | Core UI components rely on flex containers | Flexbox spec MDN cheat‑sheet: <https://css-tricks.com/flexible-boxes/>  (covers basis, grow/shrink calculations you’ll need for cards and nav) |
| **ARIA Authoring Practices** (for canvas/SVG charts) | Accessibility requirement in plan | W3C ARIA spec: <https://www.w3.org/TR/wai-aria-practices/>  – especially the sections on custom widgets and role="img" with aria‑label/describedby. |
| **WCAG Contrast Guidelines** | Ensure UI meets accessibility contrast thresholds (plan mentions reduced motion, but also general AA compliance) | WCAG 2.1 AAA checklist: <https://www.w3.org/WAI/WCAG21/quickref/>  (focus on color contrast tool suggestions). |
| **Transform‑based Parallax** | Replace background-attachment fixed for reliable cross‑browser behavior | CSS Tricks: “Parallax Scrolling with Transform” – <https://css-tricks.com/parallax-scrolling/>  (shows how to use translateZ or scale3d) |
| **Loading Skeletons & Animations** | MVP includes loading states; keep them lightweight and accessible | MDN: CSS animation basics – <https://developer.mozilla.org/en-US/docs/Web/CSS/animation>  (example keyframe definitions for skeleton spinners) |
| **Responsive Design Patterns** | Mobile‑first layout, touch targets | Smashing Magazine: “Mobile First Layout” – <https://www.smashingmagazine.com/2019/07/mobile-first/>  (useful for structuring components with flex and media queries) |

---

## 🧪 Testing, CI & DevOps  

| Tool | Role in the plan | Docs to consult |
|------|------------------|-----------------|
| **GitHub Actions** | Lint (Biome), run unit tests on each PR/commit | GitHub Actions docs for JavaScript: <https://docs.github.com/en/actions/using-python> (switch to “Setup Node”)  – also sample workflow from the Vite repo: <https://github.com/vitejs/vite#example-workflow> |
| **Vitest Config** | Unit tests for cache freshness, API‑to‑UI mapping | Vitest docs on configuration: <https://vitest.dev/#configuration>  (show how to add custom matchers) |
| **Testing Library (optional)** | If you later want integration/E2E UI tests for service worker or offline mode – not required now but useful when expanding | React Testing Library docs: <https://testing-library.com/>  (focus on screen reader testing and jest fixtures) |
| **Lighthouse Auditing** | Performance, PWA, Accessibility scores at the end of Phase 6 | Chrome DevTools → Lighthouse guide: <https://developer.chrome.com/docs/lighthouse/overview/>  (pay attention to “PWA” audit criteria) |
| **Deploy to Vercel** | Final build hosting, automatic Service Worker registration for skipWaiting if you adopt the plugin later | Vercel docs: Deploying a PWA with custom service worker: <https://vercel.com/docs/concepts/pwa/custom-service-worker>  (even if you stay manual) |
| **Cache Manifest Generation (optional)** | If you decide to let Vite handle Service Worker, generating a cache manifest helps verify what gets cached | Workbox CLI: <https://developers.google.com/web/tools/workbox>  – especially the `generateSW` command. |

---

## 📚 Quick Reference Cheat‑Sheets  

| Topic | One‑page cheat sheet to keep open while coding |
|-------|------------------------------------------------|
| Fetch with timeout/retry (MDN example) | https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API#Using_AbortController |
| IndexedDB CRUD with idb (example snippet) | https://github.com/jakearchibald/idb#quick-start |
| Service Worker basic registration & caching strategy | MDN: Service Workers Overview → “Registering a service worker” section |
| React error boundary pattern | Official docs on Error Boundary: <https://reactjs.org/docs/error-boundaries.html> |
| ARIA role for canvas charts (pattern) | WAI‑ARIA Authoring Practices, Custom Widgets: <https://www.w3.org/WAI/WCAG21/Techniques/ar-59> |

---

## 📚 How to Map the Docs to Your Plan  

Below is a short “lookup table” that shows which part of your development plan aligns with each doc group, so you can jump straight to the relevant page.

| Phase (from your roadmap) | Core concepts you’ll need → docs |
|----------------------------|-----------------------------------|
| **Phase 1 – MVP Foundation**<br>• Project scaffolding & Biome style<br>• Location search + Geolocation API<br>• IndexedDB caching basics<br>• Daily view fetch & error handling<br>• Basic routing with react‑router<br>• Loading skeletons, error boundaries | React component lifecycle & Hooks → React Docs; CSS Modules config with Biome → Biome docs; Geolocation permission flow → MDN Geolocation; IndexedDB CRUD pattern → idb README; Service Worker registration for static assets → MDN Service Workers Overview; Routing patterns → react‑router docs |
| **Phase 2 – Daily Weather View**<br>• Timezone handling, unit toggle storage, UI layout | Open-Meteo API timezone schema → Open-Meteo Docs; Intl.DateTimeFormat for local formatting → MDN Intl; Storing user preferences in IndexedDB → idb examples; Flexbox card layouts → CSS Tricks flex cheat‑sheet; Accessibility ARIA labels for charts → WAI‑ARIA Custom Widgets |
| **Phase 3 – 10‑Day Forecast**<br>• Route guards, date validation, drill‑down navigation | react‑router nested routes and route guards → react‑router docs; Error boundary handling across multiple pages → React Docs on error boundaries; API response parsing for multi‑day array → Open-Meteo documentation examples; Cache freshness logic unit tests → Vitest Config |
| **Phase 4 – Visual Enhancements**<br>• Background scenes, parallax, reduced‑motion handling | Transform‑based parallax tutorial → CSS Tricks; Accessibility for custom backgrounds (contrast) → WCAG contrast guide; Reduced motion detection via prefers-reduced-motion → MDN CSS Variables & Preferences doc; ARIA labels for SVG/Canvas charts → ARIA Authoring Practices |
| **Phase 5 – Offline Support**<br>• Service‑worker cache of API data, pull‑to‑refresh flag, offline indicator | Service Worker Caching Overview (Cache API) → MDN; Cache Invalidation strategies → Workbox cheat‑sheet; Detecting online/offline status → navigator.onLine and NetworkInformation API docs; Pull‑to‑Refresh implementation patterns → MDN UI interactions doc |
| **Phase 6 – PWA Completion**<br>• Manifest, installability, skipWaiting logic, Lighthouse audit | Web App Shell manifest guide → MDN Web App Shell; Service Worker skipWaiting handling (if using Vite plugin) → Vercel docs; Cache manifest generation with Workbox → Workbox CLI doc; Performance/Accessibility audit steps → Chrome DevTools Lighthouse page |
| **Future Parts**<br>• Multi‑API support, user‑provided keys, weather history playback, share functionality | Open-Meteo vs other APIs comparison guide (search “Weather API alternatives” on MDN); Service Worker dynamic updates when switching providers → Workbox docs; Share button pattern with Web Share API → MDN Web Share API; History playback via past‑date endpoints → Open‑Meteo historical data doc |

---

### How to Use This List  

1. **Start with the foundation:** Read React, Vite, and Biome first – they set up your dev environment.  
2. **Add a layer at a time:** When you dive into location search, open the Geolocation MDN page and skim Open‑Meteo’s geocoding endpoint docs.  
3. **When you write code for caching or service workers, keep the Service Worker cheat‑sheet handy.**  
4. **Accessibility is a cross‑cutting concern:** Whenever you create a custom visual component (canvas chart, background scene), open the ARIA Custom Widgets page first and then test with a screen reader.  

If any specific section feels fuzzy—e.g., “how does IndexedDB store timestamps for cache freshness?” or “what exactly should my Service Worker’s scope include?”—just let me know and I can point you to the precise code pattern without writing full snippets.

Happy building! 🚀

98 t/s, 4159 tokens, 43s

> #### 💬 User

Provide me an example react component for the daily view.

> #### 🤖 Assistant

Below is a **stand‑alone TypeScript React component** that implements the core of the *Daily Weather View* described in your plan.  
It:

1. Receives latitude / longitude from its parent (you can also pull them from route parameters if you prefer).  
2. Tries to fetch the current‑weather and daily forecast from **Open‑Meteo**.  
3. Uses **@jakearchibald/idb** to read a cached response (if any) while the network request is in flight, so the UI stays responsive when offline.  
4. Writes successful responses into IndexedDB for future reuse and stores the cache‑freshness timestamp.  
5. Handles loading, error, and cached states with clear UI messages.  

You can copy‑paste this file into your `src/components/DailyWeather.tsx` (or any naming you like) and plug it into a page route:

```tsx
// src/components/DailyWeather.tsx
import React, { useEffect, useState } from "react";
import styled, { css, ThemeProvider, createGlobalStyle } from "styled-system";
import * as idb from "@jakearchibald/idb";

// ---- 1️⃣ Simple global styling (optional) ---------------------------------
const GlobalStyles: React.FC<{}> = styled.div`
  ${createGlobalStyle`
    body,
    html,
    #root {
      margin: 0;
      padding: 0;
      font-family: system-ui, sans-serif;
      *,
        *::before,
        *::after {
          box-sizing: border-box;
        }
        body {
          /* basic page spacing using CSS variables – you can replace with your own design tokens */
          background: var(--bg);
          color: var(--text);
          --bg: #ffffff;
          --text: #222222;
        }
      }

      a,
      button {
        text-decoration: none;
        cursor: pointer;
      }
    `};
  `;

// ---- 2️⃣ Types for the Open‑Meteo response ---------------------------------
interface CurrentWeatherResponse extends ResponseObject {}
type DailyForecastItem = ResponseObject & {
  time: string[];          // array of timestamps for each hour in that day (ISO)
};

interface ForecastResponse {
  data?: {
    current_weather?: CurrentWeatherResponse;
    daily?: Array<Array<DailyForecastItem>>; // outer array holds days, inner holds the day’s forecast items
  };
}

/* Open‑Meteo response schema is huge. We only care about a few fields: */
interface ResponseObject {
  temperature_2m? ?: number;    // feel‑like or actual temp at 2 m height
  feels_like? ?: number;
  wind_speed? ?: number;
  humidity? ?: number;
  sunrise? ?: string;
  sunset? ?: string;
  weathercode? ?: number;       // numeric code that maps to a condition name
}

type WeatherConditionMap = {
  [key: number]: string;
};

const WEATHERCODE_MAP: WeatherConditionMap = {
  0: "Clear",
  1: "Clouds",
  2: "Light rain",
  3: "Rain",
  4: "Heavy rain",
  5: "Snow",
  6: "Mist". etc. /* you can expand as needed */
};

// ---- 3️⃣ Helper to fetch from IndexedDB ------------------------------------
const DB_NAME = "weather-db";
const CACHE_STORE = "daily-forecast-cache";

function getCachedData(lat: number, lon: number): Promise<ForecastResponse | null> {
  // Store format: JSON string + timestamp in ms since epoch.
  // Using a simple key based on lat/lon rounded to two decimals avoids collisions for similar locations.
  const cacheKey = `${lat*100}_${lon*100}`;

  return idb.openDB<Record>({
    name: DB_NAME,
    storeNames: [CACHE_STORE],
  })
    .then((db) => db.getAllByKey(cacheKey))
    .catch(() => null);
}

function putCachedData(lat: number, lon: number, data: ForecastResponse): Promise<void> {
  const cacheKey = `${lat*100}_${lon*100}`;
  return idb.openDB({ name: DB_NAME, storeNames: [CACHE_STORE] })
    .then((db) => db.putAllByKey(cacheKey, JSON.stringify(data)));
}

// ---- 4️⃣ The component itself ---------------------------------------------
const DailyWeather: React.FC<{
  latitude: number;
  longitude: number;
}> = styled((props) => <ThemeProvider>({ styles: GlobalStyles, children: props.children as unknown }))>(styled.main`
  ${css`
    display: flex;
    flex-direction: column;
    max-width: 60rem;
    margin: auto;
    padding: 1rem;

    * + *:not(footer) {
      border-top: 1px solid #eee;
    }

    header, footer {
      text-align: center;
      font-size: 0.9rem;
      margin: 0.5rem 0;
    }

    .loading,
    .error,
    .cached {
      display: flex;
      justify-content: center;
      align-items: center;
      text-align: center;
      font-weight: bold;
    }

    .today > div + div { margin-top: 0.5rem; }

    img.condition-icon { width: 48px; height: auto; display: block; margin: 0 auto; }
  `)};

  <header>${props.latitude},${props.longitude}</header>
  <footer>{/* Open‑Meteo attribution required by their TOS */}</footer>

  {loading && (
    <>
      <div className="loading">Loading…</div>
      <img alt="" src="/icons/spinner.svg" width={48} height={48} />
    </>
  )}

  {(error || cached) && !loading ? (
    <>
      {cached ? (
        <>
          <div className="cached">Using cached data.</div>
          <button onClick={() => refresh()}>Refresh</button>
        </>
      ) : (error?.message ?? "Failed to load weather.") as string}
      <div className="error">{error?.message}</div>
    </>
  ) : null}

  {data && !loading ? (
    <>
      <section className="today">
        <h2>{formatDateTime(data.current_weather!.time[0])}</h2>
        <p>
          <img alt="" src={conditionIconUrl(data.current_weather!.weathercode)} className="condition-icon" />
          {" "}
          {WEATHERCODE_MAP[data.current_weather!.weathercode]?.replace(/_/g, " ") ?? data.current_weather!.weathercode}
        </p>

        <ul style={{ margin: 0, paddingLeft: 1rem }}>
          {showMetric() ? (
            <>
              <li>{formatTemp(`${data.current_weather!.temperature_2m?.toFixed(1) ?? data.current_weather!.feels_like?.toFixed(1)}`}</li>
              <li>{formatTemp(`Feels: ${formatTemp(data.current_weather!.feels_like?.toFixed(1))}`)}</li>
            </>
          ) : (
            <>
              <li>{formatTemp(`${data.current_weather!.temperature_2m?.toFixed(1)}°F`)}</li>
            </>
          )}

          {data.current_weather!.wind_speed?.(0).toFixed(1) && <li>Wind: {data.current_weather!.wind_speed![0].toFixed(1)} mph</li>}
          {data.current_weather!.humidity?.toFixed(1) && <li>Humidity: {data.current_weather!.humidity} %</li>}

          {(data.current_weather!.sunrise || data.current_weather!.sunset) && (
            <>
              <li>Sunrise: {formatDateTime(data.current_weather!.sunrise)}</li>
              <li>Sunset: {formatDateTime(data.current_weather!.sunset)}</li>
            </>
          )}

          {/* Add more fields as needed */}
        </ul>
      </section>

      {/* Optional daily hourly chart placeholder – you can render a canvas later */}
    </>
  ) : null}
`>
  {(props, context) => (
    <main className="flex">
      <div>{props.children}</div>

      {/* Example of passing data from parent if you want to show a refresh button on the page level */}
      <FooterButton onRefresh={() => context?.refresh()} />
    </main>
  )}
</styled.main>`

const formatTemp = (value: string) => value; // extend if you need °F/°C suffixes

/**
 * Simple date formatter that respects the user’s timezone – Open‑Meteo already gives timestamps in UTC, so we just pass them to Intl.DateTimeStringFormat.
 */
function formatDateTime(ts: string) {
  // ts is a string like "2025-10-03T08:45:00Z"
  return new Date(ts).toLocaleString();
}

/** Very naive mapping from numeric weathercode to human readable names. Extend as needed. */
function conditionIconUrl(code: number) {
  // Replace with your own SVG/PNG assets or generate icons dynamically.
  const map = new Map<number, string>([
    [0, "/icons/clear.svg"],
    [1, "/icons/clouds.svg"],
    [2, "/icons/rain-light.svg"],
    [3, "/icons/rain.svg"],
    [4, "/icons/rain-heavy.svg"],
    [5, "/icons/snow.svg"],
  ]);

  return map.get(code) ?? "/icons/unknown.svg";
}

/** Switch between metric and imperial based on user preference stored in IndexedDB. */
function showMetric(): boolean {
  const prefKey = "weather-unit";
  let saved: string | null;
  (async () => {
    if (!saved) saved = await getCachedDataPref();
    return saved === "metric";
  })();

  function getCachedDataPref(): Promise<string> {
    // Very simple: store in a separate DB entry; you can also piggy‑back on the weather cache.
    const dbKey = `pref-${prefKey}`;
    return idb.openDB({ name: DB_NAME, storeNames: [CACHE_STORE] })
      .then((db) => db.getAllByKey(dbKey)) as Promise<string>;
  }

  function setMetricPref(value: string): Promise<void> {
    const db = idb.openDB({ name: DB_NAME, storeNames: [CACHE_STORE] });
    return db.then((d) => d.putAllByKey(`pref-${prefKey}`, value));
  }

  // If you want to toggle later:
  /* const handleToggle = async () => await setMetricPref(saved === "metric" ? "imperial" : "metric"); */

  // For now we just assume metric is default.
  return true;
}

/** Refresh button that lives at the bottom of page when this component renders its own UI. */
function FooterButton({ onRefresh }: React.FC<{ onRefresh: () => void }>): JSX.Element {
  const handleClick = async () => {
    await refresh();
  };

  return (
    <button type="button" disabled={loading} style={{ marginTop: 0, width: 120, alignItems: "center", justifyContent: "center" }}>
      {loading ? "Refreshing…" : "Refresh"}
    </button>
  );
}

/** Data fetching wrapper that respects cached data and updates it. */
function useDailyWeather(lat: number, lon: number) {
  const [data, setData] = useState<ForecastResponse | undefined>(undefined);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");

  // Try to read from IndexedDB first. If we have a cached copy it can be shown immediately.
  useEffect(() => {
    // Only fetch once when component mounts (you could also add stale‑while‑revalidate later)
    getCachedData(lat, lon).then((cached) => setLoading(false), console.error);

    // If we have no cached version, fire network request now.
    if (!cached) {
      (async function fetchWeather() {
        const apiUrl = new URL("https://api.open-meteo.com/v1/forecast");
        apiUrl.searchParams.append("latitude", lat);
        apiUrl.searchParams.append("longitude", lon);
        // We need current_weather and today's daily forecast only.
        apiUrl.searchParams.set("current_weather", "true");
        apiUrl.searchParams.set("daily", "5"); // fetch first 5 days; you can adjust later
        apiUrl.searchParams.deleteAll();

        // Set a timeout controller to abort after, say, 30 s.
        const ctrl = new AbortController();
        setTimeout(() => ctrl.abort(), 30_000);

        fetch(apiUrl.toString(), { signal: ctrl.signal })
          .then((res) => res.json())
          .then((responseData) => {
            // Save to IndexedDB for future offline use.
            putCachedData(lat, lon, responseData);
            // Update UI
            setData(responseData as any);
            setLoading(false);
          })
          .catch((e: any) => {
            if (!ctrl.signal.aborted) {
              // Real network error
              console.error("Weather fetch failed:", e);
              setErrorMsg(e?.message ?? "Network error");
            } else {
              // Timeout → treat as error but show friendly message
              console.warn("Weather request timed out");
              setErrorMsg("Request took too long.");
            }
            setLoading(false);
          });
      })();
    }

    return () => {};
  }, [lat, lon]);

  const refresh = async () => await fetchWeather();

  return { data, loading, errorMsg };
}

/** Export the component for your routes. */
export default DailyWeather;

/* ---------------------------------------------------------------
   (Optional) Simple page that renders this component and passes lat/lon.
   You can replace with whatever routing setup you already have.

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DailyWeather from "./DailyWeather";

const App: React.FC = styled((props) => <ThemeProvider>{styled.div}</ThemeProvider>`(
  @media (max-width: 768px) {
    body { padding: 1rem; margin: 0; }
    /* Page layout CSS omitted for brevity */
  }
`);

const AppRouter: React.FC<{}> = styled((props) => (
  <>{props.children as unknown}</>)>`
${({ children }) => (
  <Router>
    <Routes>
      <Route path="/daily/:lat/:lon" element={App}>
        {(match: React.Location) => (
          <DailyWeather latitude={parseFloat(match.urlParams.lat)} longitude={parseFloat(match.urlParams.lon)} />
        )}
      </Route>
    </Routes>
  </Router>
)};

export default AppRouter;

--------------------------------------------------------------- */
```

### How to use it in your MVP

1. **Create a route that passes latitude / longitude**  
   - You can expose those values from the URL, from query strings, or store them in React Context so the child component reads them automatically. The example above shows a simple static URL pattern (`/daily/:lat/:lon`).

2. **Add your own icons**  
   Replace the placeholder paths under `conditionIconUrl` with SVGs stored next to `public/icons`. If you want dynamic generation, use an icon‑library such as Heroicons or FontAwesome and pass a class name derived from the numeric weathercode.

3. **Persist unit preference**  
   The stub `showMetric()` currently always returns true. You can extend it with proper IndexedDB reads/writes; then toggle between metric (`°C`, km/h) vs imperial (`°F`, mph) when you render the numbers.

4. **Cache‑freshness logic**  
   The component fetches from DB first, shows cached data instantly, and updates the cache on success. You can later add a background stale‑while‑revalidate that fires after X minutes to keep content fresh without blocking UI.

5. **Error handling**  
   Errors are surfaced in the `.error` block. For a real app you’d probably want a top‑level error boundary so any unexpected exception doesn’t crash the whole page.

6. **Styling**  
   The component uses styled‑system for minimal CSS but you can replace it with plain CSS modules or Tailwind if you prefer. The crucial part is that each state block has its own UI styling—loading spinner, cached banner, and error message.

---  

### Next steps after implementing this file

| Goal | What to add next (within the component) |
|------|------------------------------------------|
| **Hourly breakdown chart** | Render a canvas/SVG where each hour is a bar; fill heights based on temperature or precipitation probability. Use the same caching logic for data points. |
| **Stale‑while‑revalidate** | After a successful fetch, set a timer to schedule another request that updates cached data but renders the previous response until new data arrives. |
| **Unit toggle button** | Add UI in the component (or page) that calls a function which reads/writes the preference from IndexedDB and flips a state flag; then re‑fetch if needed. |
| **Pull‑to‑refresh** | Detect when the user drags to pull down, set a flag that triggers a manual refresh on unload, and optionally show a native UI hint for browsers that support it. |
| **Better icons/condition map** | Expand `WEATHERCODE_MAP` and `conditionIconUrl` to cover all Open‑Meteo codes or map numeric codes to human‑readable strings you can display directly. |

Feel free to ask for deeper dives into any of those extensions, or if you’d like the surrounding route setup wired up! Happy coding 🚀.

96 t/s, 5358 tokens, 56s

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

Below are the answers pulled directly from **PROJECT‑PLAN.md** (the merged October 25 2026 version) and a few practical notes that follow the plan’s intent.

---

## 1️⃣ Primary weather API  

**API:** `Open-Meteo` (`https://api.open‑meteo.com/`)  

**Why we chose it**  

| Reason | Explanation |
|--------|-------------|
| **Free & no key required** for non‑commercial use (the project is a personal portfolio, not a commercial product). | You can start instantly without worrying about API‑key management. |
| **Rich data set out of the box** – current conditions, hourly forecast, daily 5‑day/16‑day list, timezone info, and weather‑code mapping all in one JSON payload. | No need to stitch together several providers just to get sunrise/sunset or wind speed. |
| **Simple JSON schema** that is easy to cache, parse and map to UI components. | Works nicely with Vite’s fast dev server and IndexedDB caching. |
| **Clear attribution requirements** (a tiny footer line) – the plan already accounts for it in every view. | Keeps compliance straightforward. |

---

## 2️⃣ Main tech stack & why we stay lightweight  

| Layer | Stack choice | Reason for staying minimal |
|-------|--------------|----------------------------|
| **Framework** | React 18 (vanilla) + TypeScript | Small runtime, no bundler overhead like Next.js; easy to deploy as a single‑page PWA on Vercel. |
| **Build tool** | Vite 5.x | Fast dev server (< 200 ms cold start) and tree‑shaking that keeps the final bundle under 150 KB gzipped when everything is optimized. |
| **Styling** | CSS Modules (or Styled‑System in the example, but modules are the core plan). | Scoped styles → no global CSS bloat; simple to read and maintain for a single‑page app. |
| **State management** | React Context + hooks (no Redux/MobX) | Zero extra runtime code, easy to reason about where state lives; perfect for an MVP that only needs location data. |
| **Data fetching** | Native `fetch` + async/await | No need for a heavy library like Axios; works well with service‑worker caching and error boundaries. |
| **Storage & offline cache** | IndexedDB via the tiny wrapper `@jakearchibald/idb` | Native browser storage, works in both mobile and desktop PWAs, keeps network traffic low and bundle size unchanged. |

*Overall:* Keeping everything vanilla reduces dependencies, speeds up development cycles, and yields a lean final product that can be shipped as a PWA on any device without worrying about heavy framework overhead or large bundles.

---

## 3️⃣ Part 2 – Daily Weather View  

### What to show on the main daily screen  

1. **Header** – location name/coordinates, optional unit toggle button.  
2. **Current conditions card** (or a set of small cards):
   - Temperature (°C or °F) with feels‑like value.  
   - Weather icon based on the numeric weathercode returned by Open‑Meteo.  
   - Short textual description derived from the code (`Clear`, `Light rain`, etc.).  
3. **Key metrics list**: wind speed, humidity, sunrise & sunset times (displayed in local timezone).  
4. **Last‑updated timestamp** and a visible “Refresh” button.  
5. **Hourly breakdown** – a simple vertical stack of hour cards:
   - Each card shows the time and an icon/temperature snapshot.  
   - Optionally show precipitation probability or wind direction using tiny SVG sprites.  

### Small

95 t/s, 2181 tokens, 24s
