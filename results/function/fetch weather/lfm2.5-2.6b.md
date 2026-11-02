# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
// Type definitions for OpenWeatherMap response and result
interface OpenWeatherMapResponse {
  main: {
    temp: number;
    humidity: number;
  };
  weather: Array<{
    description: string;
    main: string;
  }>;
}

interface WeatherData {
  temperature: number;
  humidity: number;
  description: string;
}

// Placeholder API key - replace with your actual OpenWeatherMap API key
const OPENWEATHER_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY_HERE';

/**
 * Fetches current weather data for a specified city from the OpenWeatherMap API.
 *
 * @param cityName - The name of the city to fetch weather for
 * @returns A Promise that resolves to an object containing temperature, humidity, and description
 * @throws Error if the request fails or returns invalid data
 */
async function fetchWeatherData(cityName: string): Promise<WeatherData> {
  try {
    // Construct the API endpoint with query parameters
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(cityName)}&appid=${OPENWEATHER_API_KEY}&units=metric`;

    // Execute the fetch request using native browser API
    const response = await fetch(url);

    // Check for HTTP error statuses (e.g., 404, 500)
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status} - ${response.statusText}`);
    }

    // Parse the JSON response
    const data: OpenWeatherMapResponse = await response.json();

    // Extract current weather information from the response
    // The first item in the 'weather' array contains current conditions
    if (data.weather && data.weather.length > 0) {
      const weatherInfo = data.weather[0];
      
      return {
        temperature: data.main.temp,
        humidity: data.main.humidity,
        description: weatherInfo.description
      };
    }

    throw new Error('Weather data not found for the specified city');
  } catch (error) {
    // Graceful error handling - log the issue and re-throw as a rejected Promise
    console.error(`Failed to fetch weather data for "${cityName}":`, error);
    
    throw new Error(`Unable to retrieve weather information: ${(error as Error).message}`);
  }
}

// Example usage:
/*
try {
  const weather = await fetchWeatherData('London');
  console.log(weather); 
  // Output: { temperature: 12.5, humidity: 72, description: 'clear sky' }
} catch (err) {
  console.error(err);
}
*/
```

287 t/s, 2636 tokens, 9s, 17%
