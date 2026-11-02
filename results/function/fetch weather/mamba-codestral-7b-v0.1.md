# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
interface WeatherResponse {
    main: { temp: number; humidity: number },
    weather: [{ description: string }]
}

async function fetchWeatherData(cityName: string): Promise<{ temperature: number, humidity: number, description: string }> {
    const API_KEY = 'your-placeholder-api-key'; // replace with your actual OpenWeatherMap API key
    const url = `http://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=${API_KEY}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data: WeatherResponse = await response.json();
        return {
            temperature: Math.round(data.main.temp - 273.15), // convert from Kelvin to Celsius
            humidity: data.main.humidity,
            description: data.weather[0].description
        };
    } catch (error) {
        console.log('An error occurred while fetching the weather data', error);
        throw error; // rethrow to be handled by the caller if needed
    }
}
```

150 t/s, 301 tokens, 2s, 1%
