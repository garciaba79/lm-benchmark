# Qwen3.5 9B
Model: qwen/qwen3.5-9b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here's a complete TypeScript async function called `fetchWeatherData` that fetches current weather data from the OpenWeatherMap API using native `fetch`. It includes proper type definitions, graceful error handling, and uses a placeholder API key:

```typescript
interface WeatherResponse {
  temperature: number; // in Celsius
  humidity: number;    // percentage (0-100)
  description: string; // weather description
}

interface ApiResponse extends Omit<WeatherResponse, 'temperature'> & Record<string, any> {
  main: { temp: number; humidity: number };
  weather: Array<{ description: string }>;
}

const API_KEY = "your_placeholder_api_key";

async function fetchWeatherData(cityName: string): Promise<WeatherResponse> {
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(cityName)}&appid=${API_KEY}&units=metric`;

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`OpenWeatherMap API error: ${errorData.message || response.statusText}`);
    }

    const data: ApiResponse = await response.json();

    return {
      temperature: data.main.temp,
      humidity: data.main.humidity,
      description: data.weather[0].description,
    };
  } catch (error) {
    if (error instanceof Error) {
      console.error("FetchWeatherData failed:", error.message);
      throw new Error(`Failed to fetch weather for "${cityName}": ${error.message}`);
    } else {
      console.error("Unknown error in fetchWeatherData");
      throw new Error("An unexpected error occurred while fetching weather data");
    }
  }
}

// Example usage:
// (fetchWeatherData("London").then(console.log).catch(console.error));
```

This function properly defines TypeScript types for both the API response and returned data, uses `encodeURIComponent` to safely handle city names with special characters, and ensures robust error handling.

122 t/s, 663 tokens, 6s, 5%
