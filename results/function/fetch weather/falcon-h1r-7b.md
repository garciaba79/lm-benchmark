# Falcon H1R 7B
Model: falcon-h1r-7b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Below is a self‑contained TypeScript example that meets all of the requirements: it defines a response type, uses `fetch` with no external dependencies, converts Kelvin → Celsius, extracts humidity and weather description, handles errors gracefully with `try…catch`, and returns a clean object from an async function.

```ts
// ──────────────────────────────────────────────────────────────
// Types for the OpenWeatherMap response we care about
// ──────────────────────────────────────────────────────────────
export interface WeatherResponse {
  /** Temperature in degrees Celsius */
  temperature: number;
  /** Relative humidity percentage */
  humidity: number;
  /** Human‑readable weather description, e.g. "clear sky", "rain" */
  description: string;
}

// Optional custom error type for clearer handling downstream
export class FetchError extends Error {
  public readonly status?: number;
  constructor(message: string, initStatus?: number) {
    super(message);
    // Keeping the prototype chain intact so instanceof works as expected
    Object.setPrototypeOf(this, new.target.prototype);
    this.status = initStatus;
  }
}

/**
 * Fetches current weather data for a given city name from OpenWeatherMap.
 *
 * @param city City name – e.g. "London", "Tokyo". The string is URL‑encoded internally.
 * @returns Promise that resolves to an object containing temperature, humidity and description.
 *         Rejects with a FetchError if the request fails or returns a non‑2xx status code.
 */
async function fetchWeatherData(city: string): Promise<WeatherResponse> {
  // ── API key placeholder ────────────────────────────────────────
  // Replace this value with your real OpenWeatherMap API key.
  // In many CI environments you’ll pull it from environment variables instead.
  const API_KEY: string = process.env?.OPENWEATHERMAP_API_KEY as string;
  if (!API_KEY) {
    // Fallback placeholder for quick manual testing. Remove or replace with your key in production.
    API_KEY = 'YOUR_PLACEHOLDER_API_KEY';
  }

  const url: string = new URL('https://api.openweathermap.org/data/2.5/weather');
  url.searchParams.set('q', encodeURIComponent(city));
  url.searchParams.set('appid', API_KEY);
  // Use metric units to get temperature in Kelvin and humidity as a percentage.
  url.searchParams.set('units', 'metric');

  try {
    const response: Response = await fetch(url, undefined);

    // ── Simple HTTP status check ───────────────────────────────────────
    if (!response.ok) {
      // Grab any error payload for debugging purposes
      const errorBody = await response.text();
      throw new FetchError(`HTTP error! status: ${response.status}`, response.status);
    }

    // ── Parse JSON ───────────────────────────────────────────────────────
    const data = await response.json();

    // Expected shape from OpenWeatherMap (excerpt):
    // {
    //   "main": {"temp": 280.15, "humidity": 63},
    //   "weather":[{"description":"clear sky","icon":"04n"}]
    // }

    // Temperature is returned in Kelvin when using metric units. Convert to Celsius.
    const tempKelvin: number = data.main?.temp ?? NaN;
    if (Number.isNaN(tempKelvin)) {
      throw new Error('Missing temperature value in API response.');
    }
    const temperatureCelsius: number = tempKelvin - 273.15;

    // Humidity is already a percentage.
    const humidity: number = data.main?.humidity ?? NaN;
    if (Number.isNaN(humidity)) {
      throw new Error('Missing humidity value in API response.');
    }

    // Weather description comes from the first weather object in the array.
    const description: string = (data.weather?.[0]?.description) ?? 'Unknown';

    // Validate that we have a non‑NaN temperature before returning.
    if (Number.isNaN(temperatureCelsius)) {
      throw new Error('Invalid temperature after conversion.');
    }

    return {
      temperature: temperatureCelsius,
      humidity,
      description,
    };
  } catch (rawError) {
    // ── Graceful error handling ───────────────────────────────────────
    // Log the raw error for debugging; then re‑throw a normalized FetchError.
    console.error('⚠️ Error while fetching weather data for', city, ':', rawError);

    // Preserve any status code if we have it from an HTTP error above.
    const wrappedError: FetchError = new FetchError(
      'Failed to retrieve weather data.',
      (rawError as Error).status?.number
    );
    // Attach the original payload for deeper investigation if desired.
    (wrappedError as any).payload = rawError;

    throw wrappedError;
  }
}

/* ────────────────────────────────────────
   Example usage:

import { fetchWeatherData } from './weather-fetcher';

async function demo() {
  try {
    const weather = await fetchWeatherData('London');
    console.log(`🌤️ ${weather.description}: ${weather.temperature.toFixed(1)}°C, ${weather.humidity}% humidity`);
  } catch (err) {
    // err will be a FetchError if something went wrong
    console.error('Weather request failed:', (err as any).message);
  }
}

demo();
 ──────────────────────────────────────── */
```

**Key points in the implementation:**

1. **Type safety:** An explicit `interface WeatherResponse` defines exactly what data we need.
2. **Native fetch only:** No third‑party modules are used; everything is built on JavaScript’s global `fetch`.
3. **Placeholder API key:** The function first checks an environment variable (`OPENWEATHERMAP_API_KEY`); if missing it falls back to a placeholder string you must replace with your real key before deployment.
4. **Error handling:**  
   * HTTP errors are detected by checking `response.ok`. If the request fails, a descriptive `FetchError` is thrown.  
   * Network‑level or parsing errors are caught in the outer `catch`, logged, and rethrown as a normalized error so callers can uniformly handle failures.
5. **Unit conversion:** Temperature comes back in Kelvin; we subtract 273.15 to return Celsius (the most common user‑friendly unit). Humidity is already provided as a percentage.

You can drop the snippet into any TypeScript project, replace the placeholder API key with your own, and call `fetchWeatherData('YourCity')`. The returned promise resolves to an object containing temperature, humidity, and description.

105 t/s, 3099 tokens, 30s, 20%
