# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here’s a self‑contained, TypeScript‑only solution. It defines the expected shape of the raw OpenWeatherMap payload, builds the request URL with a placeholder API key, and returns an object containing **temperature**, **humidity**, and **description**. Errors are caught inside `try/catch` so the promise always resolves (returning fallback values if something goes wrong).

```ts
// ---------- Type definitions ----------

/** Shape of the data returned by OpenWeatherMap for a city */
interface RawWeatherResponse {
  main?: {
    temp?: number;   // temperature in metric units (°C)
    humidity?: number;
  };
  weather?: Array<{
    description?: string;
  }>;
}

/** Public return type of fetchWeatherData */
type WeatherInfo = {
  temperature: number;
  humidity: number;
  description: string;
};

// ---------- Implementation ----------

/**
 * Fetches the current weather for a given city from OpenWeatherMap.
 *
 * @param city - Name of the city to query
 * @returns A promise that resolves to an object containing temperature (°C),
 *          humidity (%), and a short weather description.
 */
async function fetchWeatherData(city: string): Promise<WeatherInfo> {
  // TODO: Replace with your real API key
  const apiKey = "YOUR_API_KEY";

  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(
    city
  )}&units=metric&appid=${apiKey}`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      console.error(`Weather API request failed with status: ${response.status}`);
      return {
        temperature: NaN,
        humidity: NaN,
        description: "Unable to retrieve weather data",
      };
    }

    // Parse the JSON body into our expected shape
    const json = (await response.json()) as RawWeatherResponse;

    // Extract fields; fall back to defaults if a property is missing
    const temperature =
      json.main?.temp ?? 0;               // °C because we asked for metric units
    const humidity = json.main?.humidity ?? 0;
    const description = json.weather?.[0]?.description ?? "No data";

    return { temperature, humidity, description };
  } catch (error) {
    console.error("Error fetching weather:", error);
    // Graceful fallback – the promise still resolves
    return {
      temperature: NaN,
      humidity: NaN,
      description: "Network or parsing error",
    };
  }
}

export { fetchWeatherData };
```

**Key points**

1. **Async/await + native `fetch`** – no external libraries are used.
2. **`try/catch`** wraps the entire network request; any thrown exception (e.g., DNS failure, JSON parse error) is caught and logged, and a safe fallback object is returned instead of propagating an uncaught rejection.
3. **Type safety** – `RawWeatherResponse` describes the incoming API payload, while the function’s return type (`WeatherInfo`) guarantees that callers receive exactly `{ temperature: number; humidity: number; description: string }`.
4. **Placeholder key** – replace `"YOUR_API_KEY"` with a real OpenWeatherMap API key before using it in production.

109 t/s, 2809 tokens, 27s, 18%
