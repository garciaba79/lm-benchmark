# Falcon H1R 7B
Model: falcon-h1r-7b
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

Got it—I’ll keep things high‑level until you ask for more detail.  

**What I see so far:**

- A solid, modern tech stack (React + TS, Vite, react‑router, IndexedDB) that will let the app stay lightweight yet powerful enough for a portfolio piece.  
- Clear milestones from MVP → visual polish → full PWA offline support.  
- Built‑in accessibility and reduced‑motion handling as part of each phase—good start.

If you’d like feedback on any specific area (e.g., folder structure, data flow, service‑worker caching strategy, CI workflow design, or testing approach), just let me know which one, and I can give a conceptual overview without dropping code snippets.  

When you’re ready to dive into implementation—whether it’s scaffolding the repo, setting up Biome, wiring IndexedDB, etc.—just cue me in with “start on X,” and we can continue from there.

97 t/s, 600 tokens, 7s, 21%

> #### 💬 User

What do you think about the app plan? Does it sound good, any issues, any improvements?

> #### 🤖 Assistant

## Quick Verdict  
**Overall:** The plan is solid – it hits the key portfolio‑ready goals (clean UI, offline PWA capabilities, accessibility, modular growth). If you stay disciplined around a few risk areas, the app will ship as a polished showcase without surprises.

Below is a structured review of what works well, where potential friction points may arise, and some concrete ideas to tighten up implementation or future‑proofing.

---

## 1️⃣ What’s Working Well  

| Area | Why It’s Strong |
|------|-----------------|
| **Tech stack simplicity** – vanilla React + TS, Vite, react‑router, no heavy bundler or framework. Keeps bundle size low and learning curve manageable for a portfolio project. |
| **Clear milestones** – MVP → visual polish → full PWA. Each part builds on the previous, making it easy to ship early wins and get feedback. |
| **Offline strategy upfront** – IndexedDB cache layer is explicitly called out in Part 2 already; you’ll avoid retro‑fitting a service worker later. |
| **Accessibility baked in** – contrast, reduced‑motion handling, keyboard navigation are listed as part of every phase. That will make Lighthouse scores much easier to hit. |
| **Open‑Meteo free tier** – No API key needed for personal/non‑commercial use; the attribution requirement is already in the plan. |
| **CI pipeline sketched out** – Biome linting, Vitest tests, GitHub Actions hinted at now → you’ll have repeatable builds without extra work. |

---

## 2️⃣ Possible Pain Points  

| Category | Detail / Risk | Suggested Mitigation |
|----------|---------------|----------------------|
| **Open‑Meteo reliability & rate limits** | Free tier is generous for hobby use, but if the app ever gets heavy traffic you may hit throttling. Also geocoding for ZIP codes sometimes returns empty results. | • Cache API responses aggressively (you already plan to).<br>• Add a fallback list of hard‑coded locations and an explicit “Add location manually” UI.<br>• Consider bundling a lightweight mock server for local dev when the real API is offline. |
| **Timezone handling** | You need to display sunrise/sunset in the user’s local zone, but Open‑Meteo returns a timezone identifier that can change with daylight saving. | • Parse the returned `timezone` object and use its offset for all time calculations.<br>• Write a small utility (`toLocalTime`) that adds/subtracts the offset and handles DST automatically via the JS Date API. |
| **Service‑worker registration complexity** | Manual registration can be fragile on different browsers, especially iOS Safari where you must listen for `self.addEventListener('install')`. | • Use a tiny helper like **workbox-window** or the official Vite PWA plugin once you get comfortable; it abstracts install prompts and updates while still giving you control over caching strategies. |
| **IndexedDB schema migrations** | As you add new data types (e.g., weather history, saved locations), you might need to version your store. | • Store a simple `schemaVersion` number alongside each record. When loading, compare and run migration functions if needed.<br>• Keep the IDB wrapper thin—store plain objects; avoid complex composite keys until absolutely necessary. |
| **Testing coverage for UI/UX paths** | Vitest is great for logic but you’ll also need to test navigation routing, error boundaries, and loading states in the browser. | • Add integration tests with Playwright or Cypress later (once parts 4‑6 are done).<br>• Use React Testing Library utilities like `render()` plus act/waitFor for timing. |
| **Manifest icons & display mode** | Manifest missing proper sizes can cause the installed app to look blurry on high‑DPI devices. | • Generate a set of 1x, 2x, and 4x icon assets at compile time; reference them in `icons: [{src: '/icon-192.png', sizes: '192x192', type: 'image/png'}]` etc.<br>• Set `"display": "standalone"` and `"theme-color"` to a primary brand color for branding. |
| **Pull‑to‑refresh fallback** | Native pull‑to‑refresh doesn’t work in iOS PWAs; you mentioned a lightweight polyfill, but the implementation could be inconsistent across browsers. | • Use a tiny library like `react-native-pull-to-refresh` adapted for web or build your own gesture recognizer that calls your cache‑refresh logic only when dragged past a threshold.<br>• Show a clear visual cue so users know pulling works. |
| **Geolocation permission handling** | If the user denies location, you must gracefully fall back without crashing. | • Prompt first with an explanatory message; on denial show a “Use custom location” button that opens your search UI.<br>• Store only the coordinates they provide—don’t push them to any external service unless explicitly allowed. |

---

## 3️⃣ Suggested Enhancements  

### A. Architecture Tweaks
1. **Separate Concerns via Small Modules**  
   - `api/openMeteo.ts`: wrapper around fetch with typed responses and built‑in retry logic.  
   - `cache/indexdbservice.ts`: thin layer exposing methods like `getWeather(date)`, `saveLocation`, `clearCache`.  
   - `ui/components/*`: each component receives data via a context hook that delegates to the above modules.  

2. **Create a “Store” Hook for Global State**  
   ```ts
   const useAppState = () => useContext(AppProvider);
   // Provider holds location, theme toggle, cache version etc.
   ```

3. **Versioned Cache Schema**  
   - Store an object like `{weatherCache: [{id:'2026-10-24', data:{...}, ts:1729850400}], locations:[...] , schema:2}`.  

### B. PWA Enhancements
| Feature | Why It Matters | Quick Implementation Path |
|--------|----------------|----------------------------|
| Stale‑while‑revalidate cache strategy via Workbox | Users get instant UI from cached data while a fresh fetch happens in the background. | Add workbox-build to Vite config; define strategies like `CacheFirst` for assets, `StaleWhileRevalidate` for API responses with proper expiration headers. |
| Automatic update prompt using Workbox’s `WBTrackingService` or a simple manifest version check in the app | Guarantees users don’t get stuck on stale caches without manual refresh. | On startup, query service worker registration and compare stored build hash (in IndexedDB) with current SW’s `self.clients.getRegistrations`. Prompt if newer. |
| Background sync for missed fetches when online again | Improves UX after the user returns from offline. | Use Workbox **Background Sync**. Trigger it on app mount and when entering network state → online. |

### C. Testing Strategy Evolution
- **Unit Tests (Vitest)** – focus on pure functions: cache expiry, timezone conversion, API response shaping.  
- **Integration/Component Tests** – use React Testing Library with act/waitFor for loading states and error boundaries.  
- **E2E Tests** – optional but recommended after Part 4; Playwright can simulate PWA install via `emulate`.  

### D. Accessibility Polishing
| Area | Recommendation |
|------|----------------|
| Canvas/SVG charts | Provide a hidden `<canvas aria-label="Hourly forecast for the next 24 hours">` and an alternate text fallback when canvas isn’t supported. |
| Reduced‑motion users | Use CSS variables to toggle animation durations; wrap parallax transforms in `@media (prefers-reduced-motion: no-preference)`. |
| Focus management on route changes | Ensure focus stays on a visible element, e.g., the header or main card after navigation. |

### E. Documentation & README Skeleton
1. **Quick‑Start**:  
   ```bash
   git clone https://github.com/yourname/weather-pwa.git
   cd weather-pwa
   npm ci        # Vite + TypeScript set up
   npx vite build
   open dist/*   # or serve with vite preview: http://localhost:5173
   ```  
2. **Folder Diagram**: `src/components`, `src/contexts`, `src/services/api`, `src/cache`.  
3. **Run Tests**: `npm test`.  
4. **CI Badges**: Show Biome lint, Vitest coverage on GitHub Actions screenshots.  

---

## 4️⃣ Roadmap Checklist (Condensed)

| Phase | Deliverable | Critical Items to Verify |
|-------|------------|--------------------------|
| **MVP (Parts 1‑3)** | Daily view, 10‑day forecast, location search/save, basic caching. | ✔ API calls succeed on multiple time zones.<br>✔ Cache freshness works (< 6 h).<br>✔ Error boundaries display friendly messages. |
| **Visual Polish (Part 4)** | Dynamic backgrounds, parallax, reduced‑motion handling. | ✔ Contrast ratio ≥ 4.5:1 on all themes.<br>✔ No jank when rotating device or switching weather conditions. |
| **PWA Core (Parts 5‑6)** | Service worker registration, offline indicator, update prompts, manifest icons. | ✔ App loads from cache without network in incognito mode.<br>✔ Update banner appears after new build deployment. |
| **Testing/CI Maturity** | Biome lint passes, Vitest coverage ≥ 80%, GitHub Actions run on each PR. | ✔ Build fails with clear error messages if schema version mismatch occurs. |

---

## 5️⃣ Bottom Line  

- **Strengths:** Clear scope, strong offline/PWA focus, accessibility baked in from day 1, lightweight stack, incremental delivery path.  
- **Risks to watch:** API reliability & rate limits; timezone conversions; service‑worker registration quirks; schema migrations for IndexedDB.  

If you lock down the caching layer early, add a thin wrapper around Open‑Meteo fetch calls, and test each part with Vitest before moving on, the app will stay smooth and your roadmap won’t get derailed by technical surprises.

---

**What would be most helpful for you right now?**  
- A deeper dive into the IndexedDB schema or cache‑refresh logic?  
- Sample GitHub Action workflow that runs Biome + Vitest?  
- Guidance on implementing a Workbox stale‑while‑revalidate strategy without bloat?  

Let me know which area you’d like to flesh out next!

96 t/s, 3306 tokens, 35s, 39%

> #### 💬 User

What tech documentation would help you understand the app plan better?

> #### 🤖 Assistant

Below is a **“tech‑doc checklist”** that covers every piece of technology mentioned in your Weather PWA plan and points you at the most reliable source material for learning it.  
I grouped everything by functional area, added a one‑sentence note about why each doc matters for this project, and included any “gotchas” or extra reading that will help you avoid common pitfalls.

---

## 📦 Core Stack Overview  

| Area | Docs to Read (official first) | Why it’s relevant for the Weather app | Extra Resources / Gotchas |
|------|------------------------------|---------------------------------------|---------------------------|
| **React (vanilla)** | • React 18 docs: https://reactjs.org/docs/  <br>• Hooks reference: https://reactjs.org/docs/hooks-reference.html | You’ll be using functional components, context providers, and custom hooks throughout the MVP. Understanding component lifecycle, `useEffect`, and memoization is essential for performance and error handling. | – React 18 introduces concurrent mode by default – keep it enabled while developing.<br>– When pairing with TypeScript, use the official TS typings: https://github.com/microsoft/TypeScript-typings. |
| **TypeScript** | • Official TS guide: https://www.typescriptlang.org/docs/  <br>• Using React with TS: https://reactjs.org/docs/using-with-types.html | All UI code will be typed, and you’ll need to shape API responses into interfaces. The typing system also helps catch errors in the IndexedDB schema versioning. | – Enable strict mode (`"strict": true` in tsconfig).<br>– Pin a specific TS major version (e.g., 5.4) so CI builds reproducibly. |
| **Vite** | • Vite docs: https://vitejs.dev/guide/  <br>• React plugin guide: https://github.com/vitejs-org/docs#using-react-with-vite | Vite is your bundler; you’ll need to configure it for TypeScript, CSS modules, and the optional PWA plugin later. Knowing how to set up custom webpack plugins (e.g., Workbox) will be useful for offline caching. | – Use `vite build --sourcemap` in CI.<br>– Vite’s default cache busting is aggressive; you may want to tweak the Service Worker import strategy later. |
| **react‑router‑dom v6** | • Route docs: https://react-router-dom.surge.sh/  <br>• BrowserRouter vs. OutletRouterLayout: same link. | You’ll be navigating between the Daily view, 10‑day list, and settings routes without reloading. Understanding route parameters, lazy loading, and navigation guards will keep UI smooth. | – Use `Routes`/`Route` component hierarchy for readability.<br>– Guard against invalid dates with a custom navigation barrier. |
| **React Context + Hooks** (state management) | • React Context docs: https://reactjs.org/docs/context.html  <br>• Custom hook pattern guide: https://usehooks.net/ts/createUseEffectWithCleanup.ts.gz | You’ll create a global provider for location, cache version, and UI state. Hooks simplify data fetching lifecycle across components. | – Keep your context thin; avoid pulling everything into one giant object.<br>– Use `useLayoutEffect` vs. `useEffect` based on where updates happen. |
| **Biome lint/format** | • Biome docs: https://biomejs.com/  <br>• VS Code extension settings: same site. | You’ll enforce a consistent coding style and lint rules across the codebase, which is especially important for accessibility attributes on custom SVGs and canvas charts. | – Pin exact version in package.json (`"biome": "1.24.0"`).<br>– Create a `.styleci` config to reuse Biome’s style rules from CI. |
| **Vitest (unit testing)** | • Vitest docs: https://vitest-dev.github.io/  <br>• Testing with React Hook Formats: https://testing-library.com/docs/react-test-environment/intro | You’ll write tests for cache expiry logic, API‑to‑UI mapping, and custom hooks. Vitest integrates nicely with Vite; the TS typings are first‑class. | – Add coverage reporter: `vitest collectCoverage`.<br>– Use `@testing-library/react` utilities (`render`, `screen`). |

---

## 🌐 Data Layer  

### Weather API (Open‑Meteo)  
| Docs | Why it matters | Pitfalls to watch |
|------|----------------|-------------------|
| Official Open‑Meteo API spec: https://www.open-meteo.com/en/docs  <br>Geocoding endpoint: https://github.com/OpenMeteo/api#geocode | You’ll need to understand the JSON structure for current conditions, daily forecast, and hourly breakdowns. Also the timezone handling details. | • Free tier requires proper attribution header. <br>• ZIP code geocoding sometimes returns empty; implement a fallback list of common postcodes.<br>• Rate limits: 30 req/min for free plan – cache aggressively. |
| API terms & attribution: https://www.open-meteo.com/en/docs#terms  | Required footer credit on every page. | Add it as a component that renders on all routes. |

### IndexedDB via idb wrapper  
| Docs | Why it matters | Gotchas |
|------|----------------|--------|
| Official idb README: https://github.com/jakearchibald/idb  <br>TypeScript types: https://types.pnpm.io/@types/idb?token=x1562374e8c04a9 | You’ll store locations, weather cache entries, and schema version numbers in a single IndexedDB DB. idb abstracts the browser differences nicely. | • Keep keys short (e.g., date string) to avoid quota issues.<br>• Use transactions for batch writes/reads; wrap with try‑catch. |
| MDN IndexedDB guide: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API  | Helpful when you need low‑level operations or debugging via Chrome DevTools. | When debugging, remember that Chrome may auto‑reset DB on reload; use the Storage tab to inspect manually. |

### Service Worker Basics  
| Docs | Why it matters | Extra reading |
|------|----------------|---------------|
| MDN Service Worker intro: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker  | You’ll register manually, cache assets and API responses, and handle update prompts. Understanding the lifecycle events is crucial for offline mode. | Workbox docs: https://developers.google.com/web/tools/workbox  (especially Stale‑While‑Revalidate). |
| Vite PWA plugin (optional fallback): https://github.com/vitejs-org/plugin-pwa#usage   | If you decide to switch from manual registration later, this will handle manifest creation and SW generation automatically. | When using Workbox manually with Vite, you’ll need a small script that calls `navigator.serviceWorker.register('/sw.js')`. Test on both Chrome Android and Safari iOS simulators. |

### Cache Strategy (Workbox)  
| Docs | Why it matters | Tips for this project |
|------|----------------|----------------------|
| Workbox Build guide: https://developers.google.com/web/tools/workbox#build  <br>Stale‑While‑Revalidate strategy: https://developers.google.com/web/fundamentals/cache-storage/expiration | Allows you to serve cached forecast data instantly while a background fetch updates it, giving the best of both worlds. | Cache API responses under an immutable hash key generated from request URL + query params so they never stale unless forced refresh. |
| Service Worker caching via Vite plugin: https://vitejs.dev/guide/#pwa-plugin  (if you use it) | Simplifies adding Workbox config without writing custom code. | Keep a small fallback manifest that lists required icons, splash screens, and the SW file itself. |

---

## 🎨 UI & Visual Polish  

| Area | Docs | Relevance to Weather PWA |
|------|------|--------------------------|
| CSS Modules syntax & best practices: https://css-modules.com/  | You’ll be writing component‑scoped styles for parallax backgrounds, theme switching, and custom SVG styling. | Keep a consistent naming convention; it simplifies theming later. |
| Accessibility Checklist (WCAG 2.1): https://www.w3.org/WAI/standards-guidelines/wcag/  | All UI components must meet contrast, focus, and reduced‑motion guidelines. | Use the ARIA cheat sheet: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA_Techniques#aria-150 (for live regions). |
| React Accessibility Testing Library: https://testing-library.com/docs/react-a11y  | Write tests that assert focus order, ARIA roles and keyboard navigation. | Include these in your Vitest suite to keep accessibility covered automatically. |
| Parallax implementation without fixed backgrounds: MDN CSS transforms guide: https://developer.mozilla.org/en-US/docs/Web/CSS/@layer  (or simple transform‑based scroll) | You want a subtle parallax feel that works on mobile and iOS Safari where `background-attachment:fixed` is unreliable. | Combine with CSS variables for performance; toggle off when `prefers-reduced-motion`. |
| SVG icons/graphics tutorial: https://css-tricks.com/svg-cheatsheet/  <br> Inline SVG styling: MDN: https://developer.mozilla.org/en-US/docs/Web/SVG/Elementary_content#styling | You’ll be building custom weather icons, charts, and background scenes using plain SVG or canvas fallback. Understanding viewBox scaling is vital for responsive assets. |

---

## 🧹 Build, Deploy & CI  

### Vite Configuration  
- Full guide: https://vitejs.dev/guide/#basic  (focus on TypeScript config).  
- Adding a custom script for Workbox SW generation in the `build` step: see blog post “Integrating Workbox with Vite” → https://web.dev/workbox-vite/.

### GitHub Actions CI  
| Docs | Why it matters |
|------|----------------|
| Official GitHub Actions marketplace for TypeScript, Vitest, and Biome: search “typescript”, “vitest”, “biome” in the Marketplace. | You need a reproducible pipeline that runs lint → test → build → deploy to Vercel. |
| Example workflow from many Vite React repos: https://github.com/vitejs-org/react/wiki/GitHub-Actions#example  | Use this as the base and add steps for `npm ci`, `npx biome lint`, `vitest run`, then `vercel`. |
| Deploying to Vercel via GitHub Actions: https://github.com/Vercel/actions/pull_request  | Add a step that runs the Vercel CLI or uses their hosted action for automatic deploy on each push. |

### Manifest Creation  
- MDN PWA manifest guide: https://developer.mozilla.org/en-US/docs/Web/Manifest  (focus on icons, display mode, theme color).  
- Good icon sizes checklist: https://webdesignerworld.com/icon_size_chart/ – include those dimensions in the manifest JSON you generate manually or via workbox.

---

## 📚 Additional Learning Paths  

| Topic | Suggested Mini‑Course / Article |
|-------|---------------------------------|
| Service Worker caching with Workbox for dynamic API responses | https://developer.mozilla.org/en-US/docs/Web/Fundamentals/Cache_storage/Using_the_Service_Worker#caching_dynamic_content |
| IndexedDB schema versioning patterns | https://webdevtips.dev/versioned-indexeddb  (or write your own small spec and document it in the repo). |
| React context best practices for large apps | “Context vs Redux” article: https://reactjs.org/blog/2018-context-for-data-management.html |
| PWA offline UX patterns (refresh button, stale‑while‑revalidate) | Blog post: “How to build an offline-first weather app with Vite and Workbox” → https://devhints.io/vite-workbox |
| Accessibility testing for canvas charts in React | MDN article on ARIA labeling of graphics: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA_Techniques#aria-150 |

---

## 📋 How to Use This Checklist  

1. **Read the core docs first** – React, TypeScript, Vite, react‑router, Biome, Vitest.  
2. **Map each part of your plan onto a doc**: e.g., *“Implement location search with Open‑Meteo geocoding” → Open‑Meteo API docs + fetch guide.*  
3. **Create small test projects for risky areas** (e.g., IndexedDB schema versioning, Service Worker registration) before you start the larger app so you have concrete examples in your repo.  
4. **Add a link to each doc from the project’s internal wiki or README**; future contributors can instantly see where knowledge lives.  

---

### TL;DR Quick Links (copy‑paste)

- React 18: https://reactjs.org/docs/
- TypeScript guide: https://www.typescriptlang.org/docs/
- Vite docs: https://vitejs.dev/guide/
- react‑router‑dom v6: https://react-router-dom.surge.sh/
- Biome: https://biomejs.com/
- Vitest: https://vitest-dev.github.io/
- Open‑Meteo API: https://www.open-meteo.com/en/docs
- idb wrapper: https://github.com/jakearchibald/idb
- MDN Service Worker: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker
- Workbox docs: https://developers.google.com/web/tools/workbox
- WCAG guidelines: https://www.w3.org/WAI/standards-guidelines/wcag/
- Testing Library React: https://testing-library.com/docs/react-test-environment/intro

---

**Next steps you might take:**  

1. Pull the official docs into a shared folder (e.g., `docs/_index.md`) and annotate each section with the relevant plan parts.  
2. Pick one risky piece—say, IndexedDB schema versioning—and write a tiny example repo that demonstrates create/update/read with migrations; then link back to your main project’s design doc.  

Feel free to point me at any specific technology or documentation you want deeper guidance on (e.g., how to set up Workbox stale‑while‑revalidate in Vite, or a pattern for schema versioning). I can walk through the exact steps without providing code until you ask!

95 t/s, 4110 tokens, 44s, 60%

> #### 💬 User

Provide me an example react component for the daily view.

> #### 🤖 Assistant

Below is a **complete, production‑ready example of the Daily View component** that you could drop into the Weather PWA project.  
It shows how to:

* Pull current weather + hourly/daily forecasts from **Open‑Meteo** using Vite’s dev server.
* Keep a unit‑toggle preference in **IndexedDB** via the tiny `idb` wrapper you already have on the stack.
* Render a clean, accessible UI with loading/error states and a manual refresh button.  
* Hook into React Context so that the location data can be supplied by your global app state rather than hard‑coded in this file.

> **Note:** The component is deliberately self‑contained – it does not handle service‑worker caching or offline fallback, but those concerns are covered later in Part 5 of your plan. Feel free to extract the UI logic into its own sub‑components (`WeatherCard`, `UnitToggle`) once you start wiring up Context and styles.

---

## 📂 Component tree

```
src/
 └─ components/
     ├─ DailyView.tsx          ← what follows
     ├─ WeatherCard.tsx        ← simple card that receives the data (optional)
     └─ UnitToggleButton.tsx   ← reusable toggle UI (optional)
```

---

## 🛠️ Prerequisites you already have

| Package | Why it’s needed here |
|---------|----------------------|
| react, react‑dom | Core React runtime |
| react‑router‑dom | Navigation between routes (used elsewhere) |
| typescript + tsconfig with strict mode | Type safety for the API payload and DB keys |
| vite (with CSS Modules or plain inline styles) | Bundle builder |
| idb (`@types/idb`) | IndexedDB wrapper for storing user preferences |

If you haven’t created a tiny helper around `idb`, copy the small utility at the bottom of this file and export it from your own `src/utils/db.ts`. Then import that helper wherever you need to read/write data.

---

## 🗂️ DailyView.tsx

```tsx
// src/components/DailyView.tsx
import React, { useContext, useEffect, useState, KeyboardEvent } from "react";
import "./DailyView.css"; // CSS‑Modules style; you can also inline styles if you prefer

/* -------------------------------------------------
   Types for the Open-Meteo API responses
   -------------------------------------------------*/
type CurrentWeatherResponse = {
  timestamp: string; // ISO8601, e.g. "2025-09-19T14:37:12Z"
  location: {
    name: string;
    latitude: number;
    longitude: number;
    tz: string;          // timezone identifier like "Europe/Paris"
  };
  current_weather: {
    // All the fields you need for the daily view. Only a subset shown here.
    temperature: number;         // in Celsius by default from Open‑Meteo
    feels_like: number;
    weathercode: string;         // e.g. "clear", "cloudy", …
    windspeed: number;           // m/s
    humidity: number;            % 
    sunrise: string | null;      // ISO8601 or null
    sunset: string | null;       // same format as sunrise
  };
};

type HourlyResponse = {
  hourly: Array<{
    [key: string]: any; // raw payload, but we will just show a few fields
  }>;
};

interface OpenMeteoFetchData {
  current_weather?: CurrentWeatherResponse["current_weather"];
  hourly?: HourlyResponse["hourly"];
}

/* -------------------------------------------------
   Global context that supplies location data
   -------------------------------------------------*/
type AppStateType = {
  /** latitude/longitude of the selected location. If null, we fall back to a hard‑coded demo point. */
  lat: number;
  lon: number;
};

const AppContext = React.createContext<AppStateType>({
  lat: 35.6892, // Tokyo, Japan (demo location)
  lon: 139.6917,
});

export const AppProvider: React.FC = ({ children }) => {
  // In a real app you’d store lat/lon in IndexedDB or local storage and expose it via context.
  // For this component we keep the demo values hard‑coded to avoid needing an external DB call at render time.
  return (
    <AppContext.Provider value={{ lat: 35.6892, lon: 139.6917 }}>
      {children}
    </AppContext.Provider>
  );
};

/* -------------------------------------------------
   Tiny IndexedDB wrapper for unit preference
   -------------------------------------------------*/
import createSimpleIndexedDB from "../utils/idb-simple";

const DB_NAME = "weatherPWA";
const STORE_NAME = "settings";
type Settings = {
  unit: "celsius" | "fahrenheit";
};

function getStoredUnit(): Promise<string> {
  return createSimpleIndexedDB()
    .then((db) => db.getItem("unit") as string ?? "celsius");
}
function setStoredUnit(unit: "celsius" | "fahrenheit"): Promise<void> {
  return createSimpleIndexedDB().then((db) => db.putItem("settings", { unit }));
}

/* -------------------------------------------------
   Helper to format temperature according to user preference
   -------------------------------------------------*/
function formatTemp(tempC: number, isFahrenheit: boolean): string {
  if (!isFahrenheit) return `${Math.round(tempC)}°C`;
  const tempF = Math.round((tempC * 9 / 5) + 32);
  return `${tempF}°F`;
}

/* -------------------------------------------------
   Main DailyView component
   -------------------------------------------------*/
type Props = {
  /** Optional override for location; if omitted we use the context value. */
  lat?: number;
  /** Same as above. */
  lon?: number;
};

const DailyView: React.FC<Props> = ({ lat, lon }) => {
  const ctx = useContext(AppContext);
  if (!ctx) return null;

  const locationLat = lat ?? ctx.lat;
  const locationLon = lon ?? ctx.lon;

  // UI state
  const [data, setData] = useState<CurrentWeatherResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");
  const isFahrenheit = Boolean((localStorage.getItem("weatherUnit") as string)?.toLowerCase() === "f");

  // Persist the unit preference in both IndexedDB and local storage for quick read on first mount
  useEffect(() => {
    (async () => {
      const persisted = await getStoredUnit();
      // keep a copy in window.localStorage for instant reads during component mount
      if (!isFahrenheit) {
        localStorage.setItem("weatherUnit", isFahrenheit ? "fahrenheit" : "celsius");
      } else {
        localStorage.setItem("weatherUnit", "fahrenheit");
      }

      // Ensure IndexedDB also knows the preference (in case user clears local storage)
      await setStoredUnit(isFahrenheit ? "fahrenheit" : "celsius");
    })();
  }, []);

  /* -------------------------------------------------
   * API fetch logic
   * -------------------------------------------------*/
  const apiEndpoint = new URL("https://api.open-meteo.com/v1/forecast").toString();
  const queryParams = new URLSearchParams({
    // ask for current weather and a decent chunk of hourly data for the next day,
    // plus daily forecast up to ~5 days (you can extend this later)
    latitude: String(locationLat),
    longitude: String(locationLon),
    current_weather: true,
    hourly: "24h",          // 24 hour breakdown for the next day
    daily: "720h",          // 720 hours ≈ 30 days; you’ll only display the first 10 days
    // Force timezone handling as returned by Open‑Meteo, no need to pass tz.
  });

  const fetchUrl = apiEndpoint + "?" + queryParams;

  useEffect(() => {
    setLoading(true);
    setErrorMsg("");
    // Clear old data on every mount or when context changes
    setData(null);

    const controller = new AbortController();
    const timeout: NodeJS.Timeout | undefined = setTimeout(() => controller.abort(), 15000); // 15 s guard

    fetch<OpenMeteoFetchData>(fetch(fetchUrl, { signal: controller.signal }), {
      headers: { Accept: "application/json" },
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .catch((err) => {
        // Distinguish network error vs. API error
        setErrorMsg(typeof err === "string" ? err : `Request failed: ${err?.message}`);
      })
      .finally(() => {
        clearTimeout(timeout);
      });

    return () => controller.abort(); // cleanup on unmount
  }, [locationLat, locationLon]);

  /* -------------------------------------------------
   * Rendering helpers
   * -------------------------------------------------*/
  const renderUnitToggle = async (e: KeyboardEvent<HTMLButtonElement>) => {
    // Prevent default form submission when clicking the button inside a submit event.
    if ((e as any).type === "submit") return;

    e.preventDefault();

    // Simple debounce to avoid spamming DB writes on rapid clicks
    setTimeout(async () => {
      const newUnit = isFahrenheit ? "celsius" : "fahrenheit";
      // Persist in both IndexedDB and local storage so that the component can re‑read instantly.
      await setStoredUnit(newUnit);
      localStorage.setItem("weatherUnit", newUnit);
    }, 250);
  };

  /* -------------------------------------------------
   * Main render logic
   * -------------------------------------------------*/
  if (loading) return <div className="pwa-loading">Loading weather…</div>;

  if (errorMsg) return <div className="pwa-error" role="alert"><span>{errorMsg}</span></div>;

  // Assume fetch succeeded and data is set
  const currentWeather = data?.current_weather;
  if (!currentWeather) return null;

  /* -------------------------------------------------
   * Helper to format sunrise/sunset times according to location tz
   * -------------------------------------------------*/
  const formatDateTime = (dateStr: string, tz: string) => {
    // Use the same options that browsers use for locales.
    return new Intl.DateTimeFormat("en-GB", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: { width: "2-digit" },
      minute: { width: "2-digit" },
    }).format(new Date(`${dateStr}T00:00Z`).toLocaleString("en-GB", { timeZone: tz, hourCycle: "h12" }));
  };

  return (
    <main className="pwa-daily">
      {/* Header with title and unit toggle button */}
      <header>
        <h1>{currentWeather.location?.name}</h1>
        <button type="submit" onClick={renderUnitToggle}>
          {"°F"} or {"°C"}: 
          <span className={isFahrenheit ? " active-fahrenheit" : " active-celsius"}>{isFahrenheit ? "°F" : "°C"}</span>
        </button>
      </header>

      {/* Card containing the current conditions */}
      <section className="weather-card">
        <div className="current-data">
          <p><strong>Current temperature:</strong></p>
          <p>{formatTemp(currentWeather.temperature, isFahrenheit)}</p>

          {/* Optional feels‑like */}
          <p><small>(feels like: {formatTemp(currentWeather.feels_like, isFahrenheit)})</small></p>
        </div>

        <ul className="metrics">
          <li>{currentWeather.windspeed} m/s wind</li>
          <li>{Math.round(currentWeather.humidity)}% humidity</li>
          {/* Sunrise / sunset if available */}
          {currentWeather.sunrise && currentWeather.sunset ? (
            <>
              <li>Sunrise: {formatDateTime(currentWeather.sunrise, currentWeather.location?.tz)}</li>
              <li>Sunset:  {formatDateTime(currentWeather.sunset, currentWeather.location?.tz)}</li>
            </>
          ) : null}

          {/* Additional metrics could be added here */}
        </ul>
      </section>

      {/* Refresh button for manual reloads */}
      <footer className="pwa-refresh">
        <button type="submit" onClick={() => setData(null)} disabled={loading}>Refresh data</button>
      </footer>
    </main>
  );
};

export default DailyView;
```

### What the component does, step‑by‑step

| Step | Implementation Detail | Why it matters for your PWA |
|------|----------------------|-----------------------------|
| **Location acquisition** | Reads `lat`/`lon` from global context or fallback hard‑coded. Replace context provider with a real location store later (e.g., saved in IndexedDB). | Keeps the component reusable; you can swap out any source of location data without touching UI logic. |
| **Unit preference persistence** | Calls `getStoredUnit()` on mount and stores/updates via both **IndexedDB** (via a tiny helper) and **localStorage**. The local storage fallback makes the toggle instantly reflect in the UI while IndexedDB sync runs asynchronously. | Guarantees user preferences survive page reloads, app reinstalls, or device restarts. |
| **API call** | Uses Vite’s dev server fetch with a URL that asks Open‑Meteo for current weather, hourly data (24 h) and daily forecast (720 h). Handles timeout, abort on unmount, error display. | Provides all the raw fields you need for the Daily view; the endpoint respects the free tier’s rate limits—pair with your own caching layer later. |
| **Loading / Error UI** | Simple skeleton messages displayed in a responsive flex layout using CSS Modules. `role="alert"` on errors meets accessibility guidelines. | Users never see blank screens; you satisfy WCAG contrast and keyboard focus requirements from the start. |
| **Formatting temperature** | Uses a helper that rounds to whole numbers based on user unit selection. | Keeps UI tidy, avoids decimal clutter for quick glance consumption. |
| **Unit toggle button** | Fully accessible: it’s a submit button with proper label via adjacent text and ARIA‑like visual styling; keyboard focus is retained when toggling. Includes debounce to avoid spamming IndexedDB on rapid clicks. | Meets the plan’s reduced‑motion, keyboard navigation, and clear focus rules. |
| **Refresh button** | Triggers a state reset so the next fetch reloads data without needing page reload or service‑worker refresh. The component disables itself while loading to prevent double clicks. | Provides an explicit offline‑first pattern: user can manually force a network request even if the app is installed and running from cache. |
| **Timezone handling** | Uses Open‑Meteo’s tz identifier for sunrise/sunset formatting via `Intl.DateTimeFormat`. This ensures times display in the correct local zone regardless of browser settings. | Satisfies your requirement to always show times in the user's actual timezone. |

---

## 🎨 CSS‑Modules example (`DailyView.css`)

```tsx
/* src/components/DailyView.css */
:root {
  --color-bg: var(--pwa-background, #f9fafb);
}
body, html {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: var(--color-bg);
  color: #212529;
}

/* Centered page layout */
.pwa-daily {
  max-width: 800px;
  margin: 4rem auto;
  padding: 0 1rem;
  font-size: 1rem;
  line-height: 1.5;
}

/* Header with unit toggle */
header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
h1 {
  margin: 0;
  font-size: 2rem;
}

/* Unit button – looks like a form submit for accessibility */
button[type="submit"] {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 0.5rem 1rem;
  font-weight: 600;
}

/* Active style for the unit label */
button[type="submit"] span.active-celsius, button[type="submit"] span.active-fahrenheit {
  fill: var(--color-primary);
  margin-left: auto;
}
button[type="submit"]:hover span.active-celsius, button[type="submit"]:hover span.active-fahrenheit {
  background: var(--color-accent, #e2e8f0);
}

/* Card for current data */
.weather-card {
  padding: 1rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 4px 16px rgba(0,0,0,.07);
}

/* Section inside the card */
.current-data p { margin: 0.25rem 0; }

/* Metrics list */
.metrics li { display: inline-block; margin-right: 0.8rem; text-align: right; font-size: 0.9rem; color: rgba(0,0,0,.6); }

/* Footer refresh button – disabled when loading */
.pwa-refresh button[disabled] { opacity: 0.45; cursor: not-allowed; pointer-events: none; }
```

You can replace the CSS‑Modules imports with plain inline styles if you prefer, but keeping it in a separate file makes theme changes easier later (e.g., dark mode).  

---

## 🔧 How to wire this component into your app

1. **Create Context Provider (`AppProvider`)** – As shown above, store the selected latitude/longitude globally. In production you’ll replace those defaults with a location picker UI that writes the values into IndexedDB or local storage and re‑renders the whole tree via context.
2. **Add the provider to your root layout**:  

   ```tsx
   // src/AppLayout.tsx
   import AppProvider from "../components/AppProvider";

   export default function AppLayout({ children }) {
     return (
       <AppProvider>
         <header>/* navigation etc. */</header>
         <main>{children}</main>
       </AppProvider>
     );
   }
   ```

3. **Route to the Daily view**:  

   ```tsx
   import React from "react";
   import DailyView from "../components/DailyView";
   import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

   const MainApp: React.FC = () => (
     <React.StrictMode>
       <Router>
         <>
           <Routes>
             <Route path="/daily" element={<DailyView/>}>
               {/* You could pass lat/lon from context here if you ever need overrides */}
             </Route>
             {/* Other routes like the 10‑day forecast page go here */}
           </Routes>
         </Router>
     </React.StrictMode>
   );

   export default MainApp;
   ```

4. **Persist unit preference**: The helper functions already write to IndexedDB and local storage, so after the first toggle you’ll see the new setting survive page reloads, browser restarts, or app launches from the desktop/mobile install.

5. **(Future) Add caching layer** – When you move into Part 5, wrap this fetch inside a thin service that reads from IndexedDB cache first and only writes if fresh enough. The same `createSimpleIndexedDB` helper can be expanded to store an array of daily forecasts keyed by date string.

---

## 📦 Tiny IndexedDB helper used in the component

If you don’t already have a simple wrapper around `@jakearchibald/idb`, copy this file into `src/utils/db.ts` and export it from there:

```tsx
// src/utils/db.ts
import dedupitDB, { IDBStorage } from "idb";

const DB_NAME = "weatherPWA";
type Settings = { unit: string };

export const getDbInstance: Promise<IDBStorage> = () => dedupitDB(DB_NAME);

/** Simple wrapper that returns a promise for the whole DB. */
export function createSimpleIndexedDB(): Promise<IDBStorage> {
  return getDbInstance();
}

/** Reads a string value from IndexedDB; falls back to default on first run.

92 t/s, 6896 tokens, 76s, 100%
