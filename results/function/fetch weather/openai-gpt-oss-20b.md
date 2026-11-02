# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```ts
/**
 * Result returned by {@link fetchWeatherData}.
 */
export interface WeatherResult {
  /** Temperature in Celsius (according to the `units=metric` query‑param). */
  temperature: number;

  /** Humidity as a percentage. */
  humidity: number;

  /** Short textual description, e.g. “clear sky”. */
  description: string;
}

/**
 * Fetches current weather data for a given city from OpenWeatherMap.
 *
 * @param city - Name of the city (e.g. `"London"` or `"New York"`).
 * @returns A promise that resolves to an object containing temperature, humidity and description.
 *
 * The function uses the native `fetch` API and does **not** rely on any third‑party libraries.
 * It gracefully handles network errors and non‑200 HTTP responses by throwing a descriptive
 * error.  Callers can catch these errors with `try / catch`.
 *
 * @example
 * ```ts
 * try {
 *   const weather = await fetchWeatherData("Paris");
 *   console.log(weather.temperature); // e.g. 18.3
 * } catch (err) {
 *   console.error(err);
 * }
 * ```
 */
export async function fetchWeatherData(city: string): Promise<WeatherResult> {
  const apiKey = "YOUR_API_KEY"; // <-- replace with your real key

  // Build the request URL.  `units=metric` gives us Celsius.
  const url = new URL(
    "https://api.openweathermap.org/data/2.5/weather"
  );
  url.searchParams.set("q", city);
  url.searchParams.set("appid", apiKey);
  url.searchParams.set("units", "metric");

  try {
    const response = await fetch(url.toString());

    if (!response.ok) {
      // The API returns a JSON body with `message` on error
      let errMsg: string;
      try {
        const errorBody = await response.json();
        errMsg = errorBody.message || `${response.status} ${response.statusText}`;
      } catch (_) {
        errMsg = `${response.status} ${response.statusText}`;
      }
      throw new Error(`OpenWeatherMap API error: ${errMsg}`);
    }

    // The shape of the JSON returned by OpenWeatherMap
    const data = await response.json();

    // Pull out only what we care about and cast to our interface.
    const result: WeatherResult = {
      temperature: data.main.temp,
      humidity: data.main.humidity,
      description:
        Array.isArray(data.weather) && data.weather[0]
          ? data.weather[0].description
          : "No description",
    };

    return result;
  } catch (err) {
    // Re‑throw with a clearer message – the caller can still `catch`.
    if (err instanceof Error) {
      throw new Error(`Failed to fetch weather for "${city}": ${err.message}`);
    }
    throw err; // unknown error type – re‑throw as-is
  }
}
```

### How it works

1. **URL construction** – we build the request URL with the city name, API key and `units=metric` so temperatures come back in Celsius.
2. **Native fetch** – no external libs are used.
3. **Error handling**  
   * Network errors or other fetch failures throw inside the `try/catch`.  
   * Non‑200 HTTP responses are turned into a readable error using the JSON body returned by OpenWeatherMap (if any).  
4. **Result shaping** – we pick only the fields we need (`temp`, `humidity` and the first weather description) and return them as a strongly typed object.

Replace `"YOUR_API_KEY"` with your real key, or keep it as a placeholder if you’re just testing the function’s structure.

133 t/s, 879 tokens, 7s, 6%
