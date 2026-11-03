# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: Function Fetch Weather
Created: 11/03/2026, 01:42:15 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
interface WeatherData {
  temperature: number;
  humidity: number;
  description: string;
}

interface OpenWeatherMapResponse {
  main: {
    temp: number;
    humidity: number;
  };
  weather: Array<{
    description: string;
  }>;
}

const API_KEY = "YOUR_API_KEY_HERE";

async function fetchWeatherData(city: string): Promise<WeatherData> {
  try {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&units=metric&appid=${API_KEY}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: OpenWeatherMapResponse = await response.json();

    return {
      temperature: data.main.temp,
      humidity: data.main.humidity,
      description: data.weather[0].description,
    };
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to fetch weather data for ${city}: ${error.message}`);
    }
    throw new Error(`Failed to fetch weather data for ${city}: Unknown error`);
  }
}
```

23 t/s, 289 tokens, 13s
