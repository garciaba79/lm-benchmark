# Qwen3.5 9B
Model: qwen/qwen3.5-9b
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

I have reviewed your Weather PWA Development Plan. I understand the technical stack (React, Vite, TypeScript, Open-Meteo, IndexedDB), the design goals (custom visuals, accessibility, offline support), and the phased approach you have outlined.

I will not provide any code or examples unless you explicitly ask for them. I am standing by for your next instructions.

114 t/s, 647 tokens, 6s, 20%

> #### 💬 User

What do you think about the app plan? Does it sound good, any issues, any improvements?

> #### 🤖 Assistant

This is a strong, well-structured plan that shows you understand how to build a portfolio project with both technical depth and design polish. It covers a full stack of modern web skills: state management, caching strategies, PWA implementation, accessibility, CI/CD, and testing.

## Overall Assessment

The plan sounds solid. It's ambitious but realistic for a showcase project that will look excellent in a resume or portfolio context. The focus on lightweight dependencies, custom visuals, and offline support distinguishes it from typical weather apps.

## Strengths of the Plan

- **Clear Scope Management** — You've broken the work into Parts 1–6 plus future stretch goals, which makes it manageable without feature creep.
- **Realistic Tech Stack Choices** — Open-Meteo is a smart pick (no keys, free tier), and IndexedDB via `idb` is lightweight and appropriate.
- **Accessibility and Performance Built In** — Not an afterthought; these are integrated from Part 1 onward.
- **PWA Focus** — Offline support, manifest, service worker strategy, and update flow are properly sequenced.
- **Visual Polish Emphasis** — Custom graphics, parallax, weather scenes will make a big difference for portfolio impact.
- **CI/CD and Testing** — Vitest + Biome + GitHub Actions shows production-readiness from early on.

## Potential Issues or Risks

### 1. Open-Meteo Geocoding Complexity (Part 1 Spike)
The geocoding spike is essential, but postal code support is inconsistent as you noted. This could lead to frustrating UX if a user types "London" and gets multiple results from different countries.

**Suggestion:** Consider building a simple fuzzy match or ranking system that prioritizes by population/known location name. Also, decide early whether to default to coordinates when text matches are ambiguous.

### 2. Time Zone Handling (Part 2)
Requesting `timezone=auto` is good practice, but some APIs behave inconsistently around DST transitions and remote locations like polar regions.

**Suggestion:** Add a test case in your Vitest suite for DST boundaries, and consider logging timezone resolution issues during development to catch them early.

### 3. Cache Freshness Strategy (Parts 1 & 5)
Your plan specifies "serve from cache if fresh (under 3 to 6 hours)". This is reasonable, but there's no hard rule in place for when to force a refresh versus serving stale data silently.

**Suggestion:** Clarify the cache lifetime policy explicitly:
- How long do we keep cached responses?
- When does the UI show "Stale data" vs auto-refresh?
- Do we need an API version check or just timestamp-based logic?

### 4. Pull-to-Refresh Fallback (Part 5)
You mention a custom polyfill fallback for iOS Safari, where native pull-to-refresh is unreliable. However, implementing a robust fallback across browsers can be non-trivial without adding more dependencies.

**Suggestion:** Consider making it optional or using a lightweight library like `react-native-pull-to-refresh` (for demo purposes) rather than building the polyfill from scratch. Alternatively, just emphasize manual refresh and keep pull-to-refresh as iOS Safari only if native support is detected.

### 5. Service Worker Update Flow
The plan mentions an "Update available, reload" banner, which is great for UX control. However, testing versioned builds and ensuring service worker replacement works reliably is non-trivial during development.

**Suggestion:** Use `vite-plugin-pwa` initially to simplify SW generation and registration, even if you later switch to a manual setup. It will make local testing much easier and reduce cognitive load during development.

### 6. PWA Install on iOS
iOS Safari requires HTTPS and proper manifest validation; it also has stricter limits than Android Chrome. Ensure you test with both `display: standalone` and `minimal-ui` modes in your manifest, and verify that icons meet Apple's requirements (e.g., high-resolution PNGs).

**Suggestion:** Use a tool like PWA Builder or the Lighthouse PWA report to audit iOS compatibility early.

### 7. Open-Meteo Attribution & Non-Commercial Terms
You've noted this in your goals, but make sure you:
- Add the attribution footer on every view (you already plan this)
- Include it in your README and Vercel metadata
- Consider a terms-of-use link if the app goes public

### 8. Visual Polish Risks (Part 4)
Custom weather scenes and parallax can introduce performance issues on lower-end devices, especially iOS Safari. Also, background images that don't load from cache could cause visual glitches when switching between cached and fresh data.

**Suggestion:** Use SVG/CSS-based backgrounds instead of large raster images; they'll scale better and load faster. Test on a variety of devices before final polish.

### 9. Error Handling and Resilience
You plan to use error boundaries, but also consider:
- What happens if Open-Meteo API changes or times out?
- How do you handle network failures gracefully (e.g., cached data fallback)?
- Are there retries for failed fetches?

**Suggestion:** Add exponential backoff logic for failed fetches and a clear "Network error – using cached data" message.

### 10. Future Modular Parts (7–12)
These are good stretch goals, but be aware that Part 8 (user-provided API keys) could introduce security risks if not handled carefully.

**Suggestion:** If you go this route, store the key in `IndexedDB` encrypted or at least not accessible via browser console. Consider a secure vault approach for sensitive data.

## Suggested Minor Adjustments

| Area | Suggested Improvement |
| --- | --- |
| **Cache Strategy** | Define clear cache TTLs and invalidation rules upfront. |
| **Service Worker** | Use `vite-plugin-pwa` during development to reduce setup friction. |
| **Visual Polish** | Keep backgrounds lightweight (SVG/CSS), test on older devices. |
| **Geocoding UX** | Add a fallback ranking system for ambiguous location searches. |
| **Pull-to-Refresh** | Consider making it optional or using a lightweight library. |
| **Error Handling** | Include retries and explicit stale data messaging. |
| **Future Parts** | Review Part 8 carefully for security implications before implementing. |

## Final Verdict

This plan is well-thought-out, technically sound, and ambitious enough to make a strong portfolio piece. It balances scope with quality, and your attention to accessibility, performance, and offline support is impressive. The risks are mostly around geocoding edge cases, iOS PWA quirks, and cache logic — all manageable with careful testing and documentation.

If you'd like to move forward with implementation or want to discuss any specific part in more depth (e.g., cache schema design, error boundary pattern, or service worker structure), just let me know.

114 t/s, 1629 tokens, 14s, 26%

> #### 💬 User

What tech documentation would help you understand the app plan better?

> #### 🤖 Assistant

To ensure my future advice remains perfectly aligned with your specific implementation choices and constraints, having documentation or definitions in these areas would be most helpful:

### 1. Open-Meteo API Documentation & Limits
Since this is your primary data source, having the latest API docs handy (or pinned links) helps clarify:
*   **Rate limits:** Are you working within standard free tier limits or expecting higher volume?
*   **Response structure:** Exact JSON fields for daily vs. hourly endpoints.
*   **Geocoding behavior:** How Open-Meteo handles ambiguous city names versus coordinates to refine the "fuzzy match" strategy.

### 2. Design System / Visual Preferences
Since "clean UI" and "custom visuals" are core goals, documentation helps define scope:
*   **Color Palette/Theme Tokens:** Hex codes for light/dark modes if you have them defined.
*   **Typography Stack:** Specific fonts (e.g., Inter, system-ui) to ensure consistent cross-platform rendering.
*   **Iconography:** Any reference assets (e.g., Feather Icons, custom SVGs) or requirements to draw icons from scratch.

### 3. PWA Manifest Specifications
To avoid trial-and-error during Part 6:
*   **Icon Assets:** The specific sizes and formats required for iOS vs. Android manifest icons.
*   **Theme Colors:** Preferred colors for the app chrome (status bar, taskbar) on install.
*   **Scope/Start URL:** Specific routing rules (e.g., starting at `/` or `/dashboard`).

### 4. Accessibility Compliance Targets
To ensure Part 1's accessibility tasks are actionable:
*   **WCAG Level:** Are you targeting AA (general contrast) or AAA (strict contrast)?
*   **Focus Indicators:** Specific styles for focus rings (e.g., outline vs. shadow).
*   **ARIA Patterns:** Preference for native HTML semantics versus ARIA live regions for status updates.

### 5. Offline/Cache Strategy Documentation
Since you want to avoid stale data issues:
*   **TTL Rules:** Exact timestamp windows for cache freshness (e.g., "Refresh if > 3 hours old").
*   **Fallback Behavior:** Do users see a specific error message when offline, or just cached data?

### 6. Error Handling & UI Patterns
To standardize the "Loading", "Empty", and "Error" states:
*   **Toast Notifications:** Which library (if any) or custom implementation for alerts/errors?
*   **Modal vs. Inline:** How deep errors (e.g., API timeout) are presented to the user.

### 7. Project Conventions & Folder Structure
Even with standard Vite, preferences help:
*   **Naming Conventions:** PascalCase vs. camelCase for files/folders.
*   **Component Organization:** Do you prefer feature-based folders or layer-based folders (components/containers/presentational)?

### Summary
The plan you provided is already quite robust, so this documentation is optional but valuable for fine-tuning. If you do not have these specific documents yet, that is completely fine; we can derive those details during the implementation phase. I am ready when you are to proceed with **Part 1: Project Initialization**.

112 t/s, 2050 tokens, 19s, 38%

> #### 💬 User

Provide me an example react component for the daily view.

> #### 🤖 Assistant

Here is an example Daily View React component written to match your development plan: it follows your TypeScript approach, uses CSS Modules, integrates with your Open-Meteo data structure, includes accessibility patterns, and adheres to your lightweight dependency philosophy.

## `DailyView.tsx`

```tsx
import { useState, useEffect } from 'react';
import { useLocationContext } from '../context/LocationContext';
import { useWeatherCache } from '../utils/weatherCache';
import styles from './DailyView.module.css';

export interface DailyViewData {
  temperature: number;
  feelsLike: number;
  condition: 'clear' | 'cloudy' | 'rain' | 'snow' | 'storm';
  windSpeed: number;
  humidity: number;
  sunrise: string;
  sunset: string;
  high: number;
  low: number;
}

export interface DailyViewProps {
  data?: Partial<DailyViewData>;
  isLoading?: boolean;
  error?: Error | null;
  refreshTrigger?: () => void;
}

const CACHE_DURATION_MS = 3 * 60 * 60 * 1000; // 3 hours

export const DailyView: React.FC<DailyViewProps> = ({
  data,
  isLoading,
  error,
  refreshTrigger,
}) => {
  const { location, timeZone } = useLocationContext();
  const [displayUnit, setDisplayUnit] = useState<'imperial' | 'metric'>('imperial');
  const cachedData = useWeatherCache(location.name || 'Crestview, FL', CACHE_DURATION_MS);

  // Fallback to cached data or provided data if no external fetch is running
  const currentData = isLoading && !error ? undefined : { ...data, ...cachedData };
  const hasData = !!currentData?.temperature;

  // Convert unit display values
  const getTemperatureDisplay = (value: number) =>
    displayUnit === 'metric' ? `${Math.round(value)}°C` : `${Math.round(value * 1.8 + 32)}°F`;

  const getWindDisplay = (value: number) =>
    displayUnit === 'metric' ? `${value} km/h` : `${Math.round(value * 0.621)} mph`;

  // Accessibility announcement for updates
  useEffect(() => {
    if (!hasData) return;
    const currentTemp = getTemperatureDisplay(currentData.temperature);
    const message = `Current temperature ${currentTemp}. Weather in ${location.name || 'your location'}.`;

    const announcer = document.querySelector<HTMLElement>('[data-testid="weather-announcer"]');
    if (announcer) {
      announcer.textContent = message;
    }
  }, [currentData?.temperature, location.name]);

  return (
    <main data-testid="daily-view" className={styles.container}>
      {/* Accessibility Announcer for Screen Readers */}
      <div data-testid="weather-announcer" aria-live="polite" />

      {/* Header with Location and Refresh */}
      <header className={styles.header}>
        <h1>
          {hasData && currentData ? (
            <>
              Current Weather in <span>{location.name || 'Unknown'}</span>
            </>
          ) : (
            <span>Loading...</span>
          )}
        </h1>

        {/* Unit Toggle - Accessible */}
        <div className={styles.unitToggle}>
          <button
            type="button"
            onClick={() => setDisplayUnit('imperial')}
            aria-pressed={displayUnit === 'imperial'}
            className={`unit-button ${displayUnit === 'imperial' ? 'active' : ''}`}
          >
            °F / mph
          </button>

          <button
            type="button"
            onClick={() => setDisplayUnit('metric')}
            aria-pressed={displayUnit === 'metric'}
            className={`unit-button ${displayUnit === 'metric' ? 'active' : ''}`}
          >
            °C / km/h
          </button>

          <button
            type="button"
            onClick={() => {}}
            disabled={!hasData}
            aria-label={`Refresh weather data. Last updated: ${currentData?.updated || 'N/A'}`}
            className={`unit-button refresh ${!hasData ? 'disabled' : ''}`}
          >
            🔄
          </button>

          {/* Manual Refresh via IDB */}
          {refreshTrigger && (
            <button
              type="button"
              onClick={refreshTrigger}
              className="manual-refresh-button"
            >
              Manual Refresh
            </button>
          )}
        </div>
      </header>

      {/* Weather Condition Scene */}
      <section className={styles.scene}>
        {hasData && currentData ? (
          <>
            <span
              className={`condition-icon ${currentData.condition}`}
              data-testid="weather-icon"
              aria-hidden="true"
            >
              {/* Custom SVG - Replace with your hand-built icons */}
              <svg viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="45" fill={currentData.condition === 'clear' ? '#FFD700' : currentData.condition === 'rain' ? '#4A90E2' : currentData.condition === 'snow' ? '#E8F4F8' : '#B0C4DE'} />
                {/* Icon implementation would go here */}
              </svg>
            </span>
            <p className="condition-label">
              {currentData.condition.charAt(0).toUpperCase() + currentData.condition.slice(1)}
            </p>
          </>
        ) : (
          <div className="loading-skeleton condition-icon" />
        )}

        {/* Sunrise / Sunset - Accessible */}
        {hasData && currentData && timeZone && (
          <>
            <div className={styles.sunTimes}>
              <span data-testid="sunrise-time" aria-label={`Sunrise at ${currentData.sunrise}`}>
                ☀️ {currentData.sunrise} ({timeZone})
              </span>
              <span data-testid="sunset-time" aria-label={`Sunset at ${currentData.sunset}`}>
                🌅 {currentData.sunset} ({timeZone})
              </span>
            </div>
          </>
        )}
      </section>

      {/* Main Metrics Grid */}
      <section className={styles.metricsGrid} aria-labelledby="main-metrics-heading">
        <h2 id="main-metrics-heading" className="visually-hidden">Current Weather Details</h2>

        {/* Temperature Card - Accessible */}
        <div className={styles.metricCard}>
          <span className="metric-label" data-testid="temperature-label">Temperature</span>
          <div
            role="status"
            aria-live="polite"
            data-testid="temperature-value"
          >
            {hasData ? (
              getTemperatureDisplay(currentData.temperature)
            ) : (
              <span>Loading...</span>
            )}
          </div>
        </div>

        {/* Feels Like */}
        <div className={styles.metricCard}>
          <span className="metric-label">Feels Like</span>
          {hasData ? (
            getTemperatureDisplay(currentData.feelsLike)
          ) : (
            <span>Loading...</span>
          )}
        </div>

        {/* Wind */}
        <div className={styles.metricCard}>
          <span className="metric-label">Wind</span>
          {hasData ? (
            getWindDisplay(currentData.windSpeed)
          ) : (
            <span>Loading...</span>
          )}
        </div>

        {/* Humidity */}
        <div className={styles.metricCard}>
          <span className="metric-label">Humidity</span>
          {hasData ? (
            currentData.humidity + '%'
          ) : (
            <span>Loading...</span>
          )}
        </div>

        {/* High / Low */}
        <div className={styles.metricCard}>
          <span className="metric-label">High / Low</span>
          {hasData ? (
            `${getTemperatureDisplay(currentData.high)} / ${getTemperatureDisplay(currentData.low)}`
          ) : (
            <span>Loading...</span>
          )}
        </div>
      </section>

      {/* Loading State */}
      {isLoading && !error && (
        <div className={styles.loadingOverlay}>
          <span className="loading-spinner" />
          <p>Fetching latest weather data...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div role="alert" className={styles.errorState}>
          <h2>Error</h2>
          <p>{error.message || 'Failed to fetch weather data'}</p>
          <button onClick={() => refreshTrigger?.()}>Retry</button>
        </div>
      )}

      {/* Last Updated */}
      <footer className={styles.footer}>
        {hasData && currentData ? (
          <span data-testid="last-updated">Last updated: {currentData.updated}</span>
        ) : null}
      </footer>
    </main>
  );
};

export default DailyView;
```

---

## `DailyView.module.css` Example

Here's a simplified CSS Module example that aligns with your flexbox-only, lightweight styling approach:

```css
.container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.unitToggle {
  display: flex;
  gap: 0.5rem;
}

.unit-button {
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  background: #fff;
  cursor: pointer;
  border: 2px solid transparent;
  font-size: 0.875rem;
}

.unit-button.active {
  border-color: currentColor;
}

.unit-button.refresh:hover:not(:disabled) {
  background: #f0f0f0;
}

.unit-button.disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.scene {
  text-align: center;
  padding: 2rem;
  border-radius: 8px;
  background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
}

.metricsGrid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-top: auto;
}

.metricCard {
  padding: 1rem;
  border-radius: 6px;
  background: rgba(255,255,255,0.8);
  text-align: center;
  font-size: 0.875rem;
}

.loadingOverlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.9);
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  border: 0;
}
```

---

## Next Steps & Considerations for Part 2 Implementation

Based on your development plan, here's what to integrate when implementing this component:

| Area | Integration Point |
| --- | --- |
| **Open-Meteo Data Mapping** | Create a utility function that maps Open-Meteo daily endpoint JSON → `DailyViewData` |
| **IndexedDB Cache** | Wire up the cache key with location name + date; use `useWeatherCache` to persist and retrieve data |
| **Error Boundary** | Wrap this component in a React Error Boundary (Part 1 foundation) |
| **Time Zone Handling** | Use `timezone=auto` from Open-Meteo and store in context; render times in that zone |
| **Accessibility** | Include `[data-testid]` attributes for automation testing (Vitest + Lighthouse) |
| **Service Worker Strategy** | Register this data under `/daily/:date?` route prefix to support caching |

---

If you'd like me to:
- Generate the `weatherCache.ts` utility hook,
- Create the `LocationContext`,
- Build the Open-Meteo API mapping layer,
- Or write Vitest tests for this component's behavior,

just let me know. I'm ready when you are.

111 t/s, 3150 tokens, 29s, 49%
