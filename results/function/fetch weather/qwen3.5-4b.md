# Qwen3.5 4B
Model: qwen3.5-4b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
// Weather data response interface
interface WeatherResponse {
  temp: number;
  humidity: number;
  description: string;
}

// API configuration (placeholder key)
const OPENWEATHER_API_KEY = 'YOUR_OPENWEATHER_MAP_API_KEY'; // Replace with actual key
const BASE_URL = 'https://api.openweathermap.org/data/2.5/weather';

/**
 * Fetches current weather data for a given city using the OpenWeatherMap API.
 * @param city - The name of the city to fetch weather data for.
 * @returns A promise that resolves to an object containing temperature, humidity, and description.
 */
export async function fetchWeatherData(city: string): Promise<WeatherResponse> {
  try {
    const response = await fetch(`${BASE_URL}?q=${encodeURIComponent(city)}&appid=${OPENWEATHER_API_KEY}&units=metric`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    return {
      temp: Math.round(data.main.temp),
      humidity: data.main.humidity,
      description: data.weather[0].description
    };
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to fetch weather data for ${city}: ${error.message}`);
    } else {
      throw new Error('An unexpected error occurred while fetching weather data');
    }
  }
}

// Example usage:
// const weather = await fetchWeatherData('London');
// console.log(weather); // { temp: 15, humidity: 60, description: 'overcast clouds' }
```

177 t/s, 632 tokens, 4s, 4%
