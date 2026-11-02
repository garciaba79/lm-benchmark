# LFM2.5 230M
Model: lfm2.5-230m
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
interface WeatherResponse {
  temperature: number;
  humidity: number;
  description: string;
}

async function fetchWeatherData(cityName: string): Promise<WeatherResponse> {
  try {
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=YOUR_API_KEY`);
    if (!response.ok) throw new Error('Failed to load data');

    const data: WeatherResponse = await response.json();
    return { temperature, humidity, description };
  } catch (error) {
    console.error('Error fetching weather data:', error);
    throw error;
  }
}

// Example usage:
fetchWeatherData("New York").then(data => console.log(`Temperature: ${data.temperature}, Humidity: ${data.humidity}, Description: ${data.description}`));
```

This code defines a `weatherResponse` interface to specify the structure of the response from OpenWeatherMap. The function `fetchWeatherData` takes a city name as input and returns a promise that resolves with an object containing temperature, humidity, and description. It uses native `fetch` and handles errors gracefully with a try/catch block.

1022 t/s, 275 tokens, 0s, 2%
