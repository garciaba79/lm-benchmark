# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: Function Fetch Weather
Created: 11/22/2026, 03:00:56 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here is the TypeScript implementation using native `fetch` and custom interfaces for type safety.

```typescript
// 1. Define interfaces for the API response structure
interface WeatherApiResponse {
  main: {
    temp: number;
    humidity: number;
  };
  weather: {
    description: string;
  }[];
}

// 2. Define the interface for our function's return value
interface WeatherData {
  temperature: number;
  humidity: number;
  description: string;
}

/**
 * Fetches current weather data for a given city.
 * @param city - The name of the city to fetch weather for.
 * @returns A promise resolving to an object containing temp, humidity, and description.
 */
async function fetchWeatherData(city: string): Promise<WeatherData> {
  const API_KEY = "YOUR_OPENWEATHERMAP_API_KEY_PLACEHOLDER";
  const BASE_URL = "https://api.openweathermap.org/data/2.5/weather";

  try {
    // We use units=metric to get temperature in Celsius
    const response = await fetch(`${BASE_URL}?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=metric`);

    // Check if the response is not OK (e.g., 404 city not found or 401 invalid key)
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    // Cast the response to our expected API interface
    const data = (await response.json()) as WeatherApiResponse;

    // Return the mapped object
    return {
      temperature: data.main.temp,
      humidity: data.main.humidity,
      description: data.weather[0].description,
    };
  } catch (error) {
    // Handle errors (Network errors, parsing errors, or thrown errors from above)
    if (error instanceof Error) {
      console.error(`Failed to fetch weather for "${city}":`, error.message);
      throw error; // Re-throw so the caller can handle it if needed
    } else {
      console.error("An unknown error occurred while fetching weather.");
      throw new Error("Unknown error");
    }
  }
}

// --- Example Usage ---

async function main() {
  try {
    console.log("Fetching weather for London...");
    const weather = await fetchWeatherData("London");
    console.log("Weather Data Received:", weather);
  } catch (err) {
    console.log("Main execution caught error:", (err as Error).message);
  }
}

main();
```

### Key Features of this implementation:

1.  **Strong Typing**: I defined `WeatherApiResponse` to match the exact structure of the OpenWeatherMap JSON response. This ensures that `data.main.temp` is recognized by TypeScript as a number, preventing runtime property access errors.
2.  **Native Fetch**: Uses the modern `fetch` API available in browsers and Node.js 18+.
3.  **Error Handling**:
    *   It checks `response.ok` to catch HTTP-level errors (like a 404 for a city that doesn't exist).
    *   It uses `encodeURIComponent(city)` to ensure city names with spaces (like "New York") don't break the URL.
    *   It uses a `try/catch` block to catch network failures or manual errors thrown during the process.
4.  **Data Transformation**: Instead of returning the entire bulky API object, the function maps it to a clean, simplified `WeatherData` object containing only what you requested.
5.  **Units**: I added `&units=metric` to the URL so that the temperature is returned in Celsius. You can change this to `imperial` for Fahrenheit.

56 t/s, 870 tokens, 16s, 6%
