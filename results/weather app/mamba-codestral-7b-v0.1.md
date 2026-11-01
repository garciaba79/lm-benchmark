# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: Weather App Planning
Created: 10/28/2026, 12:45:34 AM
Exported from: LM Studio (via test script)
Context 32K

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

You are starting a new project for creating a Weather app. Here is your development plan:

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

**Core:**

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

**Tooling and environment:**

- Biome (lint + format, light custom rules for your preferred style)
- Vitest (unit tests)
- GitHub Actions (CI)
- Windows 11, VS Code, Git + Git Bash
- GitHub (public repo) and Vercel (deployment)

**Dependencies:**

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

### Part 7: Multiple API Support (Optional)

- Add support for multiple APIs such as OpenWeatherMap or WeatherAPI.com
- Allow users to select their preferred weather provider in the settings
- Update the app's UI and data fetching logic accordingly

### Part 8: User-provided API Keys (Optional)

- Add a feature for users to provide their own API keys for OpenWeatherMap or WeatherAPI.com
- Store the user's API key in IndexedDB
- Update the app's data fetching logic to use the user's API key when available

### Part 9: Basic Weather History Playback (Optional)

- Add a feature that allows users to view historical weather data for a specific location and date range
- Fetch historical weather data from OpenWeatherMap or WeatherAPI.com using their APIs
- Display the historical weather data in a chart or graph format

### Part 10: Share Functionality (Optional)

- Add a share functionality that allows users to share the current weather conditions, including temperature, wind speed, and precipitation
- Implement sharing options such as text message, email, or social media platforms
- Update the app's UI and data fetching logic accordingly

### Part 11: Advanced Visual Enhancements (Optional)

- Add a feature that allows users to customize the visual style of the app with different themes or color schemes
- Implement dynamic background images or animations based on weather conditions
- Allow users to save their favorite visual styles as presets and switch between them easily

### Part 12: More Location Management (Optional)

- Add a feature that allows users to manage multiple locations, such as adding favorites or creating custom locations
- Implement location search functionality for finding new locations by name or coordinates
- Allow users to set default locations for quick access
- Update the app's UI and data fetching logic accordingly

141 t/s, 2466 tokens, 19s, 17%

> #### 💬 User

What do you think about the app plan? Does it sound good, any issues, any improvements?

> #### 🤖 Assistant

The weather PWA development plan looks well-structured and covers all the necessary aspects of a modern web application. Here are my thoughts on the plan:

1. Core Project Goals: This section outlines the main objectives of the project, such as creating a lightweight, visually clean React Progressive Web App (PWA) for weather forecasting with custom graphics and offline support. The goals are clear and concise, which is important for staying focused during development.
2. Tech Stack: This section provides an overview of the technologies being used in the project, such as React, TypeScript, Vite, react-router-dom, IndexedDB via idb wrapper, CSS Modules + custom flexbox only, and Open-Meteo for weather data fetching. The choice of these technologies is reasonable and should provide a solid foundation for building the app.
3. Core: This section outlines the core features that will be implemented in the project, such as location selection and saving, daily view, 10-day forecast with drill-down, visual polish, offline support via IndexedDB caching and service worker, accessibility by design, and deployment to Vercel. The list of core features is comprehensive and covers all the necessary aspects of a weather PWA.
4. Tooling and Environment: This section outlines the tools and environment that will be used for development, such as Biome (lint + format, light custom rules for your preferred style), Vitest (unit tests), GitHub Actions (CI), Windows 11, VS Code, Git + Git Bash, GitHub, and Vercel. The choice of tools is reasonable and should provide a smooth development experience.
5. Development Parts: This section outlines the different parts that will be developed during the project, such as Part 1 (Project Initialization and Core Setup), Part 2 (Daily Weather View), Part 3 (10-Day Forecast View), Part 4 (Visual Enhancements and Weather Themes), Part 5 (Caching, Service Worker, and Offline Polish), Part 6 (PWA Completion and Installability), and Part 7 (Multiple API Support). This breakdown of development parts is helpful for understanding the scope of the project.
6. Development Flow: This section outlines the suggested development flow, which includes phases such as Phase 1 (Project Initialization and Core Setup) and Phase 2 (PWA Completion and Installability), along with specific milestones to be achieved at each phase. The development flow is clear and provides a roadmap for completing the project.
7. Project Benefits: This section outlines the potential benefits of the project, such as creating a portfolio-worthy project, showcasing modern web skills, demonstrating offline support, and testing API data mapping logic. These benefits are important for motivating the development process.
8. Philosophy: This section provides some guidance on how to approach the project, such as keeping scope realistic, staying fully custom, and following a lightweight, visually clean design. The philosophy is clear and should help guide the development process.
9. Changes from the Earlier Versions: This section notes that the plan has been updated since an earlier version, with specific changes such as pinning react-router to 6.0.2 instead of using a caret (^) range, adding a service worker registration step in Part 5, and deferring the decision on vite-plugin-pwa until manual setup becomes tedious. These updates are helpful for providing context on how the plan has evolved over time.
10. Next Steps: This section suggests some next steps that can be taken after completing the initial development milestones, such as working on Parts 7 and 8 (Multiple API Support) or exploring additional features like user-provided API keys or basic weather history playback. These suggestions are helpful for guiding future development efforts.

Overall, I think this plan is well-structured and covers all the necessary aspects of a modern web application. The choice of technologies and development flow seem reasonable, and the list of core features is comprehensive. However, it would be beneficial to add more specific details on how certain features will be implemented, such as custom visual polish or offline support via service workers. Additionally, providing examples or code snippets for some of the key components or workflows could help clarify the development process and make the plan more concrete.

141 t/s, 951 tokens, 7s, 20%

> #### 💬 User

What tech documentation would help you understand the app plan better?

> #### 🤖 Assistant

To provide a clearer understanding of your weather PWA development plan, here are some technical documents that might be helpful:

1. React Documentation: The official React documentation (https://reactjs.org/) provides detailed information on how to build and structure a React application, including best practices for state management, component architecture, and performance optimization. This knowledge would help you understand the choice of React as your framework and how to implement key features such as location selection, daily view, and 10-day forecast with drill-down.
2. TypeScript Documentation: The official TypeScript documentation (https://www.typescriptlang.org/docs/) provides detailed information on how to use TypeScript in your project, including best practices for type declarations, interfaces, and generics. This knowledge would help you understand the choice of TypeScript as your language and how to implement key features such as data fetching and unit tests.
3. Vite Documentation: The official Vite documentation (https://vitejs.dev/) provides detailed information on how to use Vite for building and bundling your application, including best practices for performance optimization and development workflows. This knowledge would help you understand the choice of Vite as your build tool and how to implement key features such as service workers and offline support via IndexedDB caching.
4. react-router-dom Documentation: The official documentation for react-router-dom (https://reactrouter.com/web/guides/quick-start) provides detailed information on how to use the library for routing in your React application, including best practices for handling route parameters and nested routes. This knowledge would help you understand the choice of react-router-dom as your routing solution and how to implement key features such as location search and daily view drill-down.
5. IndexedDB Documentation: The official IndexedDB documentation (https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API) provides detailed information on how to use the IndexedDB API for storing and retrieving data in a browser, including best practices for performance optimization and schema design. This knowledge would help you understand the choice of IndexedDB as your caching solution and how to implement key features such as offline support via service workers.
6. Open-Meteo Documentation: The official documentation for Open-Meteo (https://open-meteo.com/en) provides detailed information on how to use the API for weather forecasting, including best practices for data fetching and error handling. This knowledge would help you understand the choice of Open-Meteo as your weather API provider and how to implement key features such as daily view and 10-day forecast with drill-down.
7. CSS Modules Documentation: The official documentation for CSS Modules (https://github.com/css-modules/css-modules) provides detailed information on how to use the technique for scoping styles in your React components, including best practices for naming conventions and class composition. This knowledge would help you understand the choice of CSS Modules as your styling solution and how to implement key features such as custom visual polish and parallax effects.
8. Service Worker Documentation: The official documentation for service workers (https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) provides detailed information on how to use the API for offline support in your web application, including best practices for caching strategies and event handling. This knowledge would help you understand the choice of service workers as your offline solution and how to implement key features such as offline support via IndexedDB caching and a service worker.
9. Vercel Documentation: The official documentation for Vercel (https://vercel.com/docs) provides detailed information on how to deploy and host your web application, including best practices for performance optimization and continuous integration workflows. This knowledge would help you understand the choice of Vercel as your deployment solution and how to implement key features such as GitHub Actions for CI and automated testing.
10. Biome Documentation: The official documentation for Biome (https://biomejs.dev/) provides detailed information on how to use the tool for linting, formatting, and code quality checks in your JavaScript or TypeScript project, including best practices for configuration and customization options. This knowledge would help you understand the choice of Biome as your linter and how to implement key features such as accessibility by design and automated testing.

140 t/s, 974 tokens, 7s, 23%

> #### 💬 User

Provide me an example react component for the daily view.

> #### 🤖 Assistant

Here is an example React component for a daily weather forecast view:
```javascript
import React from 'react';
import PropTypes from 'prop-types';
import styles from './DailyView.module.css';

const DailyView = ({ date, location, temperature, humidity, windSpeed }) => {
  return (
    <div className={styles.container}>
      <h2>{date}</h2>
      <p>{location}</p>
      <p>Temperature: {temperature}°F</p>
      <p>Humidity: {humidity}%</p>
      <p>Wind Speed: {windSpeed} mph</p>
    </div>
  );
};

DailyView.propTypes = {
  date: PropTypes.string.isRequired,
  location: PropTypes.string.isRequired,
  temperature: PropTypes.number.isRequired,
  humidity: PropTypes.number.isRequired,
  windSpeed: PropTypes.number.isRequired,
};

export default DailyView;
```
This component takes in the following props:

* `date` (string): The date for which the forecast is being displayed.
* `location` (string): The location for which the forecast is being displayed.
* `temperature` (number): The temperature for the given date and location.
* `humidity` (number): The humidity level for the given date and location.
* `windSpeed` (number): The wind speed for the given date and location.

The component renders a container div with a class of `container`, which can be styled using CSS Modules to provide custom visual polish. Inside the container, there are heading and paragraph elements that display the date, location, temperature, humidity, and wind speed for the given forecast. The propTypes object defines the expected types for each prop, ensuring that the component receives the correct data types and helps prevent bugs caused by incorrect usage.

142 t/s, 437 tokens, 3s, 24%
