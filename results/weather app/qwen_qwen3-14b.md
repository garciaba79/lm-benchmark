# Qwen Qwen3 14B
Model: qwen_qwen3-14b
Test: Weather App Planning
Created: 10/28/2026, 12:45:34 AM
Exported from: LM Studio (via test script)
Context 8K

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

Understood! I'll wait for your instructions on which specific part of the project you'd like assistance with. When you're ready to proceed with any aspect—whether it's scaffolding the project, designing components, setting up IndexedDB, or anything else—just let me know and I'll provide focused guidance without code examples until you ask explicitly. 

Are you ready to start with the first step (project initialization) or another part of the plan?

10 t/s, 293 tokens, 32s, 34%

> #### 💬 User

What do you think about the app plan? Does it sound good, any issues, any improvements?

> #### 🤖 Assistant

Your **Weather PWA development plan** is exceptionally well-structured, thoughtful, and aligned with modern web development best practices. Here's my breakdown of its strengths, potential issues, and suggestions for improvement:

---

### ✅ **Strengths**
1. **Clear Scope & MVP Focus**  
   The project balances ambition with realism by prioritizing a clean, functional MVP (daily weather + 10-day forecast) before diving into polish and PWA features. This ensures the app remains lightweight while still being portfolio-worthy.

2. **Tech Stack Choices**  
   - Using **React + TypeScript + Vite** is modern, efficient, and avoids unnecessary bloat (e.g., no Next.js).  
   - **Open-Meteo API** is a smart choice for simplicity (no API key required) and non-commercial use.  
   - **IndexedDB via `idb`** for caching aligns with PWA goals and avoids heavy libraries like Redux.

3. **PWA & Offline Strategy**  
   The plan emphasizes **manual service worker setup**, **cache freshness logic**, and **offline indicators**, which are critical for a robust PWA. Including pull-to-refresh as an enhancement (not a dependency) shows platform-aware design.

4. **Accessibility & Design Philosophy**  
   - Explicit focus on **color contrast, keyboard navigation, reduced motion**, and semantic HTML is commendable.  
   - Custom visuals (SVGs, parallax) ensure uniqueness without relying on third-party libraries.

5. **Testing & CI/CD Integration**  
   Including **Vitest for unit tests**, **Biome for linting/formatting**, and GitHub Actions for CI ensures maintainability and quality from the start.

6. **Documentation & Readme Planning**  
   The plan includes a **README roadmap** (screenshots, architecture notes) and emphasizes documenting decisions (e.g., pinned Biome versions), which is rare in many projects.

---

### ⚠️ **Potential Issues / Considerations**
1. **Open-Meteo API Limitations**  
   - Open-Meteo’s free tier is non-commercial only. If the app is intended for public use, ensure compliance with their terms (e.g., attribution).  
   - Check if their 16-day forecast data meets your needs (some APIs offer more granular historical or real-time data).

2. **Geocoding Fallbacks**  
   The plan mentions postal code fallbacks but notes inconsistent coverage. Consider:  
   - Prioritizing city names over zip codes for broader compatibility.  
   - Using a fallback location (e.g., `Crestview, FL`) if all geocoding attempts fail.

3. **Time Zone Handling**  
   While requesting `timezone=auto` from Open-Meteo is smart, ensure your app handles time zone conversions correctly when displaying sunrise/sunset times and hourly forecasts.

4. **IndexedDB Caching Strategy**  
   - Define a clear cache expiration policy (e.g., 6 hours for weather data).  
   - Consider using **cache versioning** in IndexedDB to avoid conflicts during updates.

5. **Service Worker Registration**  
   The plan delays service worker registration until Part 5, which is logical but requires careful testing to ensure offline behavior works seamlessly with cached assets and API responses.

6. **Unit Toggle (°F/°C)**  
   Storing user preferences in IndexedDB is good, but consider adding a default based on the user’s system locale or location (e.g., Celsius for most countries, Fahrenheit for the US).

---

### 🔧 **Suggestions for Improvement**
1. **Add Internationalization (i18n) as a Stretch Goal**  
   If targeting global users, support for multiple languages could be a nice-to-have (e.g., via `react-i18next` or a simple JSON-based system).

2. **Consider Web Components for Reusability**  
   For components like weather icons or charts, consider using **Web Components** (e.g., `<weather-icon>`), which can improve modularity and reuse across projects.

3. **Optimize SVG/Canvas Performance**  
   If using custom SVGs or canvas for visuals, ensure they are optimized for performance (e.g., lazy loading, reducing complexity).

4. **Include a "Clear Cache" UI Feature**  
   While the plan mentions it as a nice-to-have, adding a button to clear cached data could be invaluable for debugging and demos.

5. **Test on iOS Safari Early**  
   iOS has stricter PWA requirements (e.g., no `background-attachment: fixed`, limited pull-to-refresh support). Test installability and offline behavior early in Part 6.

6. **Lighthouse Score Targets**  
   The plan mentions aiming for a Lighthouse score of 90+ but doesn’t specify how to achieve it. Consider adding actionable steps (e.g., lazy loading images, reducing JS/CSS bundle sizes).

---

### 🚀 **Final Thoughts**
This is one of the most comprehensive and thoughtful project plans I’ve seen for a portfolio PWA. It balances technical depth with practicality, ensuring the app remains lightweight, accessible, and visually appealing while covering all critical PWA features (offline support, installability, caching). 

**One minor tweak**: Consider adding **a note about Open-Meteo’s non-commercial use policy** in the README to avoid legal issues if the app is shared publicly. Otherwise, proceed with confidence—this plan will result in a polished, modern, and impactful project! 🌤️

Let me know when you’re ready to dive into implementation or need help refining any part of the plan further.

9 t/s, 1971 tokens, 210s, 56%

> #### 💬 User

What tech documentation would help you understand the app plan better?

> #### 🤖 Assistant

To fully understand and implement your **Weather PWA** plan effectively, here are the key types of **technical documentation** that would help clarify requirements, reduce ambiguity, and ensure consistency across development phases:

---

### 📄 1. **API Documentation**
   - **Open-Meteo API**:  
     A detailed reference for their endpoints (e.g., geocoding, current weather, forecast). Include examples of requests/responses, rate limits, and required parameters.  
     *(Link: https://open-meteo.com/en/docs)*
   - **Geolocation API**:  
     Document how the browser's `navigator.geolocation` is used (permissions, fallbacks for denied access).
   - **IndexedDB Schema**:  
     A clear diagram or JSON schema of your IndexedDB structure (e.g., tables for locations, cached weather data, user preferences).

---

### 🧱 2. **Code Structure & Folder Layout**
   - A **directory tree** with explanations for each folder/file:  
     ```
     /src
       /components      # Reusable UI elements (e.g., WeatherCard)
       /views           # Page-level components (DailyView, ForecastView)
       /context         # Global state management (LocationContext, ThemeContext)
       /utils           # Helper functions (cache helpers, unit conversion)
       /styles          # CSS Modules or global styles
       /types           # TypeScript interfaces and types
       /services        # API calls and IndexedDB interactions
     ```
   - A **component diagram** showing how views, context, and services interact.

---

### 🧩 3. **State Management & Data Flow**
   - A **flowchart or diagram** of the app's data flow:  
     - How user input (location search) triggers API calls → updates global state → renders UI.
     - How cached data is retrieved from IndexedDB and merged with fresh API responses.
   - Documentation on **React Context usage**:  
     - Which contexts are used (e.g., `LocationContext`, `ThemeContext`), their props, and how they're consumed.

---

### 📦 4. **Caching & Service Worker Strategy**
   - A **cache strategy document** with:  
     - Cache expiration rules (e.g., "weather data expires after 6 hours").  
     - How stale data is handled (fallback to cached data, refresh on user action).  
     - IndexedDB schema for caching (e.g., `key: [locationId + timestamp]`, value: API response).
   - A **service worker registration plan**:  
     - When it's registered (Part 5), how assets and API responses are cached.  
     - How updates are handled (e.g., "Update available" banner, versioning).

---

### 🧪 5. **Testing & CI/CD Documentation**
   - A **test coverage guide** for Vitest:  
     - Which components/services have unit tests (e.g., `cacheManager.test.ts`, `unitConversion.test.ts`).  
     - How to run tests locally (`npm test`) and in GitHub Actions.
   - A **CI/CD pipeline overview**:  
     - GitHub Actions workflows for linting (Biome), testing, and deployment to Vercel.  
     - Environment variables used during deployment (e.g., `VERCEL_PROJECT_ID`).

---

### 🖼️ 6. **Visual Design & Accessibility Guidelines**
   - A **style guide** for:  
     - Color themes (light/dark modes, weather-specific palettes).  
     - Typography, spacing, and flexbox layouts.  
     - Parallax effects (transform-based, not `background-attachment`).  
   - An **accessibility checklist**:  
     - WCAG compliance targets (e.g., contrast ratios ≥ 4.5:1).  
     - Keyboard navigation paths for all interactive elements.  
     - ARIA labels for SVGs/canvas charts.

---

### 📱 7. **PWA & Offline Documentation**
   - A **manifest.json template** with notes on:  
     - Icons (maskable, 192x192 and 512x512 sizes).  
     - Theme colors, display mode (`standalone`), and name.
   - An **offline behavior guide**:  
     - How the app detects offline status.  
     - How cached data is displayed (e.g., "Using cached data" banner).  
     - Pull-to-refresh implementation (native or polyfill).

---

### 📝 8. **README & README.md Template**
   - A **README.md template** with:  
     - Project overview and goals.  
     - Installation steps (`npm install`, `npm run dev`).  
     - Deployment instructions (Vercel).  
     - Contributing guidelines (e.g., "Run tests before submitting PRs").  
     - License (MIT, etc.).  
   - A **"Getting Started" section** for new contributors:  
     - How to set up the project locally.  
     - Key files to modify (e.g., `manifest.json`, `service-worker.js`).

---

### 📁 9. **Versioning & Dependency Policy**
   - A **dependency version table**:  
     - Pin exact versions for tools like React, Vite, Biome, and Vitest.  
     - Example:  
       ```json
       {
         "react": "^18.3",
         "vite": "^5.4",
         "biome": "1.0.0"
       }
       ```
   - A **versioning policy** for app updates (e.g., semantic versioning, when to increment major/minor/patch).

---

### 🧠 10. **Error Handling & Edge Cases**
   - A **list of edge cases**:  
     - Geolocation denied → fallback to hardcoded location.  
     - No internet → show cached data + "Offline mode" banner.  
     - Invalid date in forecast route → redirect to today's view.
   - An **error boundary documentation** for React:  
     - How error boundaries are implemented (e.g., `ErrorBoundary` component).  
     - Fallback UI for failed API calls or cache misses.

---

### 🔍 Bonus: Lighthouse & Performance Goals
   - A **Lighthouse score target document**:  
     - PWA: 90+ (installability, caching, service worker).  
     - Accessibility: 95+ (color contrast, keyboard navigation).  
     - Performance: 85+ (bundle size, load time).

---

### Summary
These documents will ensure **clarity**, **consistency**, and **maintainability** for your project. They also make it easier to onboard new contributors or revisit the app later. If you'd like, I can help draft any of these templates! 🚀

10 t/s, 1993 tokens, 203s, 71%

> #### 💬 User

Provide me an example react component for the daily view.

> #### 🤖 Assistant

Here's a **skeleton React component** for your **Daily Weather View**, written in TypeScript, aligned with your project plan. This example includes structure, state hooks, loading/error handling, and placeholder UI elements that match your goals (e.g., unit toggle, parallax effects, accessibility).

---

### 📁 File: `src/views/DailyView.tsx`

```tsx
import React, { useEffect, useState } from 'react';
import styles from './DailyView.module.css'; // CSS Module for styling
import { useLocationContext } from '../../context/LocationContext'; // Global location state
import { useUnitPreference } from '../../context/UnitContext'; // Unit toggle (°F/°C)
import { WeatherData } from '../../types/weather'; // TypeScript interface for weather data

const DailyView: React.FC = () => {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const { selectedLocation } = useLocationContext();
  const { unitPreference, toggleUnit } = useUnitPreference();

  // Fetch weather data from Open-Meteo API
  useEffect(() => {
    if (!selectedLocation) return;

    const fetchWeatherData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Replace with actual API call to Open-Meteo
        const response = await fetch(
          `https://api.open-meteo.com/v1/forecast?latitude=${selectedLocation.lat}&longitude=${selectedLocation.lon}&current_weather=true&timezone=auto`
        );

        if (!response.ok) {
          throw new Error('Failed to fetch weather data');
        }

        const data: WeatherData = await response.json();
        setWeather(data);
      } catch (err) {
        setError((err as Error).message || 'An error occurred while fetching weather data.');
      } finally {
        setLoading(false);
      }
    };

    fetchWeatherData();
  }, [selectedLocation]);

  // Render loading state
  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <p>Loading current weather...</p>
        {/* Add skeleton UI here */}
      </div>
    );
  }

  // Render error state
  if (error) {
    return (
      <div className={styles.errorContainer}>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Try Again</button>
      </div>
    );
  }

  // Render weather data
  if (!weather) return null;

  const { temperature, feels_like, wind_speed, humidity, sunrise, sunset } = weather.current_weather;

  return (
    <div className={styles.dailyView}>
      {/* Parallax background based on weather condition */}
      <div className={`${styles.background} ${styles[getBackgroundClass(weather.current_weather.weather_code)]}`}>
        <div className={styles.overlay}></div>
      </div>

      <div className={styles.content}>
        <h1>{selectedLocation.name}</h1>
        <p>Current Weather</p>

        {/* Temperature Display */}
        <div className={styles.temperature}>
          <span>{temperature}°{unitPreference === 'metric' ? 'C' : 'F'}</span>
          <button onClick={toggleUnit}>Toggle Unit</button>
        </div>

        {/* Key Metrics */}
        <div className={styles.metrics}>
          <div>
            <p>Feels Like:</p>
            <p>{feels_like}°{unitPreference === 'metric' ? 'C' : 'F'}</p>
          </div>
          <div>
            <p>Wind Speed:</p>
            <p>{wind_speed} {unitPreference === 'metric' ? 'm/s' : 'mph'}</p>
          </div>
          <div>
            <p>Humidity:</p>
            <p>{humidity}%</p>
          </div>
        </div>

        {/* Sunrise/Sunset */}
        <div className={styles.sunriseSunset}>
          <p>Sunrise: {sunrise}</p>
          <p>Sunset: {sunset}</p>
        </div>

        {/* Hourly Chart (placeholder for canvas/SVG) */}
        <div className={styles.hourlyChart}>
          <h2>Hourly Forecast</h2>
          {/* Replace with actual chart component */}
          <canvas width="400" height="150"></canvas>
        </div>

        {/* Refresh Button */}
        <button onClick={() => window.location.reload()}>Refresh Data</button>
      </div>
    </div>
  );
};

// Helper to get background class based on weather code (e.g., sunny, rainy)
function getBackgroundClass(weatherCode: number): string {
  switch (weatherCode) {
    case 0:
      return 'sunny';
    case 1:
    case 2:
    case 3:
      return 'cloudy';
    case 45:
    case 48:
      return 'foggy';
    case 51:
    case 53:
    case 55:
      return 'lightRain';
    case 61:
    case 63:
    case 65:
      return 'moderateRain';
    case 71:
    case 73:
    case 75:
      return 'heavySnow';
    default:
      return 'default';
  }
}

export default DailyView;
```

---

### 🔧 Notes for Integration

- **Context Usage**: This component uses `useLocationContext` and `useUnitPreference`, which you’ll need to define in your context files.
- **Styling**: The CSS Module (`DailyView.module.css`) should include styles for `.background`, `.overlay`, `.temperature`, etc., with parallax effects using `transform: translateZ()` or similar (avoid `background-attachment: fixed`).
- **API Integration**: Replace the placeholder API call with your actual logic, including caching via IndexedDB.
- **Accessibility**: Add ARIA labels and semantic HTML elements (e.g., `<main>`, `<button aria-label="Toggle temperature unit">`) as needed.

---

### 📌 Next Steps
1. Create a `WeatherData` TypeScript interface in `src/types/weather.ts`.
2. Implement the actual API call to Open-Meteo, including error handling and caching.
3. Add custom SVG or canvas components for charts (e.g., hourly forecast).
4. Style with CSS Modules and parallax effects.

Would you like me to help draft the corresponding **CSS Module**, **TypeScript interface**, or **context files**?

10 t/s, 1836 tokens, 188s, 87%
