# Qwen3.6 35B A3B
Model: qwen/qwen3.6-35b-a3b
Test: Function Fetch Weather
Created: 11/22/2026, 03:13:03 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
interface WeatherData {
  temperature: number;
  humidity: number;
  description: string;
}

async function fetchWeatherData(city: string): Promise<WeatherData> {
  const apiKey = "YOUR_PLACEHOLDER_API_KEY";
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    const weatherData: WeatherData = {
      temperature: data.main.temp,
      humidity: data.main.humidity,
      description: data.weather[0].description,
    };

    return weatherData;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to fetch weather data: ${error.message}`);
    }
    throw new Error("Failed to fetch weather data: Unknown error");
  }
}
```

44 t/s, 243 tokens, 6s, 2%
