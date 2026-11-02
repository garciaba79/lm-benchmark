# LFM2.5 8B A1B
Model: lfm2.5-8b-a1b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```ts
// Type definitions for the weather response
export type WeatherResult = {
  temperature: number;
  humidity: string;
  description: string[];
};

/**
 * Fetches current weather data for a given city from OpenWeatherMap.
 *
 * @param city Name of the city to look up.
 * @returns A promise that resolves with an object containing temperature, humidity, and description,
 *          or throws an error on failure.
 */
export async function fetchWeatherData(city: string): Promise<WeatherResult> {
  // Placeholder API key – replace with your actual OpenWeatherMap key
  const API_KEY = process.env.OPENWEATHER_KEY ?? 'YOUR_PLACEHOLDER_API_KEY';

  // Build the request URL using query parameters (city name + metric units)
  const url =
    `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&units=metric&appid=${API_KEY}`;

  try {
    const response = await fetch(url);

    // Throw an error if the HTTP request failed
    if (!response.ok) {
      throw new Error(`OpenWeatherMap API error: ${response.status} - ${response.statusText}`);
    }

    // Parse JSON body and extract fields we need
    const data: WeatherResultRaw = await response.json();

    return {
      temperature: data.main.temp,
      humidity: `${data.main.humidity}%`,
      description: data.weather.map((w) => w.description),
    };
  } catch (error) {
    // Re‑throw a more descriptive error while preserving the original message
    throw new Error(
      `Failed to fetch weather for "${city}": ${(error instanceof Error ? error.message : 'Network or parsing error')`
    );
  }
}

/* Example shape of the raw OpenWeatherMap JSON response */
interface WeatherResultRaw {
  main: { temp: number; humidity: number };
  description: Array<{ description: string }>;
}
```

390 t/s, 1254 tokens, 3s, 8%
