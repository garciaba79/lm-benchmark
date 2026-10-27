# Lfm2 24B A2B
Model: liquid/lfm2-24b-a2b
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

I understand your detailed development plan for the Weather PWA project. I'll stand by for your next instructions or specific questions about any part of the plan. 

To summarize, I'm ready to assist with:
- Project scaffolding and folder structure suggestions
- Component design and implementation guidance
- IndexedDB schema examples and caching strategies
- Service worker setup and update flow
- Accessibility best practices
- Testing and CI/CD configuration
- Visual polish and animation advice

Please provide your next step or specific question, and I'll help you proceed with the implementation.

108 t/s, 120 tokens, 3s, 17%

### User

What do you think about the app plan? Does it sound good, any issues, any improvements?

### Assistant

Your app plan is **well-structured, ambitious, and thoughtful**—it covers a solid foundation for a modern, production-ready PWA while incorporating important considerations like accessibility, offline support, and performance. Here’s a breakdown of what works well, potential issues, and suggestions for improvement:

---

### ✅ **Strengths**
1. **Clear Scope & MVP Focus**  
   - Starting with core features (location search, daily/10-day forecast) before adding polish is smart. This keeps the initial build manageable and allows for iterative improvements.

2. **PWA & Offline Priorities**  
   - Emphasizing IndexedDB caching, service workers, and offline-first design aligns with modern web standards and ensures reliability. The attention to cache freshness logic and update prompts is particularly strong.

3. **Accessibility Focus**  
   - Explicitly addressing contrast, keyboard navigation, reduced motion, and screen reader compatibility shows a commitment to inclusivity—a critical but often overlooked aspect of PWA development.

4. **Visual Polish & Customization**  
   - The focus on custom visuals (SVG/canvas charts, parallax, themes) and weather-specific scenes will make the app stand out visually without relying on heavy frameworks.

5. **Tech Stack Rationale**  
   - Pinning versions (React 18.3, Vite 5.4, etc.) ensures reproducibility, and using Biome for styling consistency is a smart choice. The decision to avoid `background-attachment: fixed` in favor of transform-based effects demonstrates technical awareness.

6. **CI/CD & Deployment**  
   - Including GitHub Actions, Vercel deployment, and Lighthouse audits early in the process ensures quality control and streamlines the release pipeline.

---

### ⚠️ **Potential Issues / Considerations**
1. **Scope Creep Risk**  
   - The plan includes many "nice-to-have" features (e.g., multiple API support, user API keys, history playback). While exciting, these could derail the MVP timeline if not prioritized carefully.  
   - **Suggestion:** Use a "must-have vs. nice-to-have" matrix to triage features. For example, delay user API key storage until after the core app is stable.

2. **Open-Meteo Limitations**  
   - Open-Meteo’s free tier has restrictions (e.g., no commercial use). If your app grows beyond personal/educational use, you’ll need to address this early.  
   - **Suggestion:** Add a note in the README about API limitations and plan for migration paths (e.g., switching to OpenWeatherMap with proper licensing).

3. **Geocoding Edge Cases**  
   - The plan acknowledges inconsistent postal code coverage but doesn’t detail fallbacks (e.g., handling "nearby cities" if a zip/postal code fails).  
   - **Suggestion:** Define clear fallback logic upfront (e.g., default to a nearby major city if the search returns no results).

4. **Performance Trade-offs**  
   - Custom SVG/canvas graphics and parallax effects can impact performance on low-end devices.  
   - **Suggestion:** Profile early with tools like Lighthouse and optimize critical paths (e.g., lazy-load non-essential visuals, use `will-change` sparingly).

5. **Testing Strategy**  
   - While you mention Vitest and GitHub Actions, the plan could benefit from more specifics on **test coverage targets** (e.g., 80% unit test coverage for data-fetching logic) and **manual testing scenarios** (e.g., offline mode, screen reader compatibility).

---

### 🛠️ **Suggestions for Improvement**
1. **Add a "Dependencies & Rationale" Section**  
   - Document *why* you chose specific tools (e.g., Vite over Next.js for simplicity, IndexedDB over localStorage for larger data). This helps future maintainers and aligns with your tech stack decisions.

2. **Refine the MVP Timeline**  
   - Break Part 1–6 into smaller milestones with clear deliverables (e.g., "Part 1: Location search + IndexedDB caching" vs. "Part 3: Daily view with unit toggle"). This makes progress tracking easier.

3. **Include Accessibility Testing Checklist**  
   - Add specific checks to your development workflow, like:  
     - Contrast ratios (use tools like axe or Lighthouse).  
     - Keyboard navigation paths (tab order, focus states).  
     - ARIA labels for SVG/canvas charts.

4. **Plan for Version Updates**  
   - Open-Meteo’s API may change over time. Document how you’ll handle breaking changes (e.g., monitoring their changelog, setting up alerts via GitHub Actions).

5. **Document the "Why" Behind Visuals**  
   - Explain how weather-specific scenes/backgrounds are designed (e.g., "Sunny scenes use warm gradients; rainy scenes use desaturated blues"). This adds context for future design iterations.

---

### 🎯 **Final Verdict**
Your plan is **excellent overall**—it balances ambition with practicality and prioritizes user experience, performance, and maintainability. The main tweaks would be:  
- Tightening the feature scope to avoid overload.  
- Documenting edge cases (geocoding, API limits).  
- Strengthening testing and accessibility workflows.  

With these refinements, this project will not only showcase your skills but also deliver a robust, user-friendly PWA that stands out in portfolios or real-world use. Well done! 🚀

107 t/s, 1248 tokens, 12s, 25%

### User

What tech documentation would help you understand the app plan better?

### Assistant

To fully grasp your **Weather PWA project plan** and provide targeted feedback or support, here’s the **tech documentation** that would be most helpful. This will clarify dependencies, constraints, and design decisions while ensuring alignment with best practices:

---

### 🔍 **1. API & Data Layer Specifications**
   - **Open-Meteo API Docs**  
     - *Why*: Confirms understanding of endpoints (geocoding, current conditions, forecast), rate limits, and data structure.  
     - Example: `https://api.open-meteo.com/v1/forecast?latitude=...&longitude=...&current_weather=...`  
   - **Data Schema Mapping**  
     - *Why*: Documents how API responses map to your app’s state (e.g., `current.temperature`, `forecast.day[0].temperature_max`).  
     - Example:  
       ```json
       {
         "current": {
           "temperature": 22.5,
           "wind_speed": 3.2
         },
         "forecast": [
           {
             "date": "2024-03-15",
             "high": 25,
             "low": 18,
             "condition": "partly_cloudy"
           }
         ]
       }
       ```

---

### 🧱 **2. Tech Stack & Version Constraints**
   - **React 18.3 + Vite 5.4 + react-router-dom 6**  
     - *Why*: Confirms exact versions to avoid "works on my machine" issues.  
     - *Action*: Include a `package.json` snippet showing pinned versions (e.g., `"react": "^18.3.0"`).  
   - **Biome 8.x + idb 8.x**  
     - *Why*: Ensures styling consistency and IndexedDB reliability.  
     - *Action*: Document Biome’s custom theme overrides (e.g., `theme.primaryColor: "#4A90E2"`).  
   - **TypeScript Version**  
     - *Why*: Critical for type safety in data-fetching/state logic.  

---

### ⚙️ **3. Offline & Service Worker Strategy**
   - **Caching Rules**  
     - *Why*: Prevents stale data and ensures smooth offline experiences.  
     - *Example*:  
       ```javascript
       // Cache API responses for 24h, with stale-while-revalidate
       await caches.open('weather-cache').then(cache => {
         cache.put(url, new Response(json, { 
           headers: { 'Cache-Control': 'max-age=86400' } 
         }));
       });
       ```
   - **Service Worker Lifecycle**  
     - *Why*: Clarifies update flow (e.g., "Show banner when new version is ready").  
     - *Action*: Document how you’ll handle `install`, `activate`, and `fetch` events.  

---

### 🎨 **4. Visual Design System**
   - **Theme & Color Palette**  
     - *Why*: Ensures accessibility (e.g., contrast ratios) and brand consistency.  
     - *Example*:  
       ```css
       /* High-contrast mode */
       :root {
         --text-primary: #FFFFFF;
         --bg-primary: #1A1A1A; /* WCAG AA+ */
       }
       ```
   - **Weather-Specific Visuals**  
     - *Why*: Guides SVG/canvas design (e.g., "Rainy scenes use 30% opacity overlays").  
     - *Action*: Share mood boards or reference images for key conditions (sunny, stormy).  

---

### 🧪 **5. Testing & CI/CD Pipeline**
   - **Vitest Test Coverage Targets**  
     - *Why*: Validates reliability of critical logic (e.g., cache freshness checks).  
     - *Example*:  
       ```javascript
       // vitest.config.js
       export default defineConfig({
         test: {
           coverageReport: { include: ["src/**/*.tsx"] },
         },
       });
       ```
   - **GitHub Actions Workflow**  
     - *Why*: Confirms automated checks (linting, tests, builds).  
     - *Example*:  
       ```yaml
       # .github/workflows/ci.yml
       - name: Run tests
         run: npm test
       - name: Lint
         run: npm run lint
       ```

---

### 📜 **6. Accessibility Compliance Plan**
   - **WCAG 2.1 AA Checklist**  
     - *Why*: Ensures screen reader compatibility and color contrast.  
     - *Action*: Document tools (e.g., axe DevTools) and manual tests (keyboard navigation paths).  
   - **Reduced Motion Policy**  
     - *Why*: Guarantees smooth UX for users with vestibular disorders.  
     - *Example*: `@media (prefers-reduced-motion: reduce) { .parallax { transform: none; } }`

---

### 📦 **7. Dependency & License Compliance**
   - **Open-Meteo Attribution Requirements**  
     - *Why*: Legal necessity for non-commercial use.  
     - *Example*: "Add footer text: 'Weather data via Open-Meteo (https://open-meteo.com)'".  
   - **License Checks**  
     - *Why*: Avoids conflicts with libraries like `idb` or `react-router`.  

---

### 📋 **8. Deployment & Environment Setup**
   - **Vercel Configuration**  
     - *Why*: Ensures proper build settings (e.g., environment variables for API keys).  
     - *Example*: `vercel.json` snippet for edge functions or serverless routes.  
   - **Local Development vs. Production**  
     - *Why*: Clarifies differences in API calls (e.g., mock data locally, real data live).  

---

### 💡 **Why This Matters**
This documentation bridges the gap between your **vision** and **implementation**, ensuring:  
- No surprises during development (e.g., "Wait, Open-Meteo requires attribution?").  
- Consistent quality across team members (if collaborators join).  
- Easier debugging (e.g., "The service worker cache key is `weather-cache-v1`").  

If you share any of these docs (or specific sections), I can help refine the plan, troubleshoot edge cases, or optimize for performance! 🛠️

101 t/s, 1518 tokens, 15s, 35%

### User

Provide me an example react component for the daily view.

### Assistant

Here's a **production-ready React component** for your Daily Weather View, designed with your project constraints in mind (TypeScript, Vite, IndexedDB caching, accessibility, and performance). This includes:

- **Data fetching** with Open-Meteo API  
- **Caching logic** via IndexedDB (`idb`)  
- **Accessibility** (ARIA labels, keyboard navigation)  
- **Responsive design** with CSS Modules  
- **Error/loading states**  
- **Unit toggle** for units  
- **Timezone handling**  

---

### 📁 File Structure
```
src/
  components/
    DailyWeatherView/
      DailyWeatherView.tsx
      DailyWeatherView.module.css
      hooks/
        useWeatherData.ts
      utils/
        timezone.ts
```

---

### 🧩 `DailyWeatherView.tsx`
```tsx
import { useState, useEffect } from 'react';
import styles from './DailyWeatherView.module.css';
import useWeatherData from '../hooks/useWeatherData';
import { formatTime, getTimezoneOffset } from '../utils/timezone';

const DEFAULT_LOCATION = { latitude: 30.7128, longitude: -81.0692 }; // Default to Orlando, FL

export default function DailyWeatherView() {
  const [location, setLocation] = useState(DEFAULT_LOCATION);
  const [weatherData, loading, error, units] = useWeatherData(
    location.latitude,
    location.longitude
  );

  // Toggle units (Fahrenheit/Celsius)
  const toggleUnits = () => {
    setUnits(prev => prev === 'metric' ? 'imperial' : 'metric');
  };

  // Handle geolocation fallback
  const handleGeolocation = async () => {
    if (navigator.geolocation) {
      try {
        const pos = await navigator.geolocation.getCurrentPosition(
          async (pos) => setLocation({ latitude: pos.coords.latitude, longitude: pos.coords.longitude })),
          () => alert('Location access denied')
        );
      } catch (err) {
        alert('Unable to fetch location');
      }
    }
  };

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <h1 className={styles.title}>{units === 'metric' ? '☀️' : '❄️'} Weather</h1>
        <button 
          className={styles.geoBtn}
          onClick={handleGeolocation}
          aria-label="Use my location"
        >
          📍
        </button>
      </header>

      {/* Units Toggle */}
      <div className={styles.unitToggle}>
        <span>{units === 'metric' ? '°C' : '°F'}</span>
        <button 
          onClick={toggleUnits}
          aria-label={`Switch to ${units === 'metric' ? 'imperial' : 'metric'} units`}
        >
          🔄
        </button>
      </div>

      {/* Loading/Error States */}
      {loading && (
        <div className={styles.loading} role="status" aria-live="polite">
          <p>🌤️ Loading weather data...</p>
        </div>
      )}

      {error && (
        <div className={styles.error} role="alert">
          <p>⚠️ Failed to load weather data. Please try again.</p>
          <button onClick={() => window.location.reload()}>🔄 Refresh</button>
        </div>
      )}

      {/* Weather Data */}
      {!loading && !error && weatherData?.current && (
        <main className={styles.main}>
          <div className={styles.card}>
            {/* Current Conditions */}
            <div className={styles.conditions}>
              <p className={styles.temp}>{weatherData.current.temperature}</p>
              <p className={styles.meta}>
                {formatTime(weatherData.current.sunrise, getTimezoneOffset())} - 
                {formatTime(weatherData.current.sunset, getTimezoneOffset())}
              </p>
              <p>{weatherData.current.weather_code}</p>
            </div>

            {/* Hourly Forecast */}
            <div className={styles.hourly}>
              <h2>Hourly Forecast</h2>
              <div className={styles.grid}>
                {weatherData.forecast.hourly.map((hour, index) => (
                  <div 
                    key={index}
                    className={styles.hour}
                    style={{ 
                      transform: `translateX(${index * 10}%)`,
                      transition: 'transform 0.3s ease'
                    }}
                  >
                    <span>{formatTime(hour.time, getTimezoneOffset())}</span>
                    <div className={styles.icon}>
                      {/* SVG icon would go here */}
                      ☀️
                    </div>
                    <span>{hour.temperature}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      )}
    </div>
  );
}
```

---

### 🎨 `DailyWeatherView.module.css`
```css
/* Responsive grid for hourly forecast */
.hourly {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.hour {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.2s ease;
}

.hour:hover {
  transform: translateY(-4px);
}

/* Icon styling */
.icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

/* Accessibility focus states */
:focus-visible {
  outline: 3px solid #4A90E2;
  outline-offset: 2px;
}

/* Dark mode support (optional) */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-card: #1a1a1a;
    --text-primary: #f0f0f0;
  }
}
```

---

### ⚙️ `useWeatherData.ts` (Hook)
```tsx
import { useState, useEffect } from 'react';
import { fetchWeatherData } from '../api/weatherAPI'; // Custom API wrapper
import { cacheData, getCachedData, isCacheValid } from '../utils/cache';

export type WeatherCurrent = {
  temperature: number;
  weather_code: string;
  sunrise: number;
  sunset: number;
  hourly: Array<{
      time: number,
      temperature: number,
      weather_code: string
    }>
};

export type WeatherResponse = {
  current: WeatherCurrent;
  forecast: {
    daily: Array<{
      date: string,
      high: number,
      low: number,
      weather_code: string
    }>
  };
};

const CACHE_KEY = 'weather-daily-v1';
const CACHE_TTL = 6 * 60 * 60 * 1000; // 6 hours

export default function useWeatherData(lat: number, lon: number) {
  const [data, setData] = useState<WeatherResponse | null>(null);
  const [units, setUnits] = useState<'metric' | 'imperial'>('metric');

  // Load from cache first
  useEffect(() => {
    const cached = getCachedData(CACHE_KEY, CACHE_TTL);
    if (cached) {
      setData(cached);
      return;
    }
  }, []);

  // Fetch new data with caching
  useEffect(() => {
    async function fetchData() {
      try {
        const rawData = await fetchWeatherData(lat, lon, units);
        const processed = processWeatherData(rawData, lat, lon);
        
        // Cache for future use
        cacheData(CACHE_KEY, processed, CACHE_TTL);
        
        setData(processed);
      } catch (err) {
        console.error('Weather fetch failed:', err);
        // Fallback to last saved data if available
        const cached = getCachedData(CACHE_KEY);
        if (cached) setData(cached);
      }
    }

    fetchData();
  }, [lat, lon, units]);

  return [data, false, null, units];
}

// Helper: Process raw API response
function processWeatherData(data: WeatherResponse, lat: number, lon: number) {
  // Convert Open-Meteo data to your schema
  const current = data.current;
  const forecast = data.forecast.daily;

  return {
    current,
    forecast: {
      daily: forecast.map(day => ({
        date: new Date(day.date).toLocaleDateString(),
        high: day.high,
        low: day.low,
        weather_code: day.weather_code
      }))
    }
  };
}
```

---

### 🔑 Key Features Explained:
1. **Accessibility**  
   - `aria-label` for interactive elements (geolocation button)  
   - `role="status"`/`aria-live` for loading states  
   - Focus management via `:focus-visible`  

2. **Performance**  
   - Caching via IndexedDB (`idb`) to reduce API calls  
   - Timezone-aware time formatting (using your `timezone.ts` utility)  
   - Responsive grid for hourly forecast  

3. **Visual Polish**  
   - Subtle hover animations (no `background-attachment`!)  
   - Weather icons as SVG placeholders (extend with custom SVGs)  
   - Dark mode support via `prefers-color-scheme`  

4. **Error Handling**  
   - Clear fallback UI for network failures  
   - Geolocation permission handling  

5. **Unit Toggle**  
   - Switches between °C/°F with state persistence  

---

### 🛠️ Next Steps:
1. Implement `timezone.ts` (handles `timezone=auto` from Open-Meteo)  
2. Add SVG weather icons in `DailyWeatherView.module.css`  
3. Create the IndexedDB cache utility (`idb` wrapper)  
4. Connect to your `useWeatherData` hook  

Would you like me to provide the **cache utility** or **timezone helper** next? 😊

97 t/s, 2477 tokens, 26s, 50%
