# Ministral 3 3B Reasoning 2512
Model: ministral-3-3b-reasoning-2512
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here is the TypeScript async function `fetchWeatherData` that meets all the specified requirements:

```typescript
interface ApiResponse {
    main: {
        temp: number;
        humidity: number;
    };
    weather: Array<{
        description: string;
    }>;
}

interface WeatherData {
    temperature: number; // in Celsius
    humidity: number;
    description: string;
}

async function fetchWeatherData(city: string): Promise<WeatherData> {
    try {
        const apiKey = "your_api_key_here"; // placeholder API key
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data: ApiResponse = await response.json();

        return {
            temperature: data.main.temp - 273.15, // Convert from Kelvin to Celsius
            humidity: data.main.humidity,
            description: data.weather[0].description
        };
    } catch (error) {
        console.error("Error fetching weather data:", error);
        throw error; // Re-throw the error for the caller to handle if needed
    }
}
```

This function:
- Defines interfaces for the API response and the expected weather data.
- Takes a city name as input and fetches data from OpenWeatherMap using a placeholder API key.
- Converts temperature from Kelvin to Celsius by subtracting 273.15.
- Returns a promise that resolves to an object with `temperature`, `humidity`, and `description`.
- Handles errors by catching them in a try/catch block, logging the error, and re-throwing it for the caller to handle if necessary.
- Uses only native fetch without external libraries.

215 t/s, 1958 tokens, 9s, 7%
