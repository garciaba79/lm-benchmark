# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here's a clean, well-typed implementation:

```typescript
/**
 * Shape of the data we return to callers.
 */
export interface WeatherData {
  city: string;
  temperature: number;   // in Kelvin (convert as needed)
  humidity: number;       // percentage 0–100
  description: string;    // e.g. "clear sky", "few clouds"
}

/**
 * Shape of the OpenWeatherMap current-weather JSON response.
 */
interface OpenWeatherMapResponse {
  name?: string;
  main: {
    temp: number;   // Kelvin
    humidity: number; // percentage
  };
  weather: Array<{
    description: string;
    main: string;
  }>;
}

/**
 * Thrown when the API returns a non-2xx status or an invalid response.
 */
export class WeatherApiError extends Error {
  constructor(
    public readonly city: string,
    public readonly statusCode?: number,
    message: string
  ) {
    super(message);
    this.name = "WeatherApiError";
  }
}

const API_URL = "https://api.openweathermap.org/data/2.5/weather";
const API_KEY = "YOUR_API_KEY_HERE"; // ← replace with your real key

/**
 * Fetches current weather for a city from the OpenWeatherMap API.
 *
 * @param city  Name of the city to look up (e.g. "London")
 * @returns     Promise resolving to { temperature, humidity, description }
 */
export async function fetchWeatherData(city: string): Promise<WeatherData> {
  try {
    const response = await fetch(
      `${API_URL}?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=metric`
    );

    if (!response.ok) {
      // OpenWeatherMap uses specific codes; surface them for debugging.
      const code = response.status;
      let detail: string | undefined;
      try {
        const body = await response.json();
        detail = body.message ?? "";
      } catch {
        /* ignore parse errors */
      }

      throw new WeatherApiError(city, code, `Weather request failed (${code})${detail ? `: ${detail}` : ""}`);
    }

    const data: OpenWeatherMapResponse = await response.json();

    return {
      city: data.name ?? city,
      temperature: data.main.temp, // Kelvin → convert to Celsius/Fahrenheit if needed
      humidity: data.main.humidity,
      description: data.weather[0]?.description ?? "unknown",
    };
  } catch (error) {
    if (error instanceof WeatherApiError) throw error;

    if (error instanceof TypeError) {
      // TypeError is what native fetch throws on network failures.
      throw new WeatherApiError(city, undefined, "Network error while fetching weather data");
    }

    const message = error instanceof Error ? error.message : String(error);
    throw new WeatherApiError(city, undefined, `Unexpected error: ${message}`);
  }
}
```

### Usage example

```typescript
try {
  const weather = await fetchWeatherData("London");
  console.log(weather);
  // { city: "London", temperature: 12.4, humidity: 76, description: "few clouds" }
} catch (error) {
  if (error instanceof WeatherApiError) {
    console.error(`Could not fetch weather for ${error.city}:`, error.message);
  } else {
    console.error("Unexpected error:", error);
  }
}
```

### Notes on setup & usage

- **Fetch availability:** Native `fetch` is built into modern browsers and Node.js ≥ 18. If you're using an older TypeScript/Node setup, install the types:
  ```bash
  npm install --save-dev @types/node   # for Node
  # or ensure "DOM" lib is enabled in tsconfig.json for browser targets
  ```

- **Units:** I used `units=metric` (Celsius). Remove it to get Kelvin, or swap to `units=imperial` for Fahrenheit. Adjust the `temperature` field accordingly if you need a specific unit.

- **API key security:** Never commit your real API key. Use environment variables in production:
  ```typescript
  const API_KEY = process.env.OPENWEATHER_API_KEY ?? "";
  ```

- **Rate limits & caching:** OpenWeatherMap has rate limits (60 calls/min free tier). For repeated lookups, consider adding a small cache layer around this function.

139 t/s, 1363 tokens, 10s, 9%
