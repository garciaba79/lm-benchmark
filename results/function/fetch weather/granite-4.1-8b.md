# Granite 4.1 8B
Model: granite-4.1-8b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Below is a TypeScript implementation of the `fetchWeatherData` function as described. This function uses the native `fetch` API to call the OpenWeatherMap API, processes the JSON response, and returns an object containing temperature, humidity, and weather description. Error handling is included using try/catch blocks.

```typescript
interface WeatherResponse {
  main: {
    temp: number; // Temperature in Kelvin
    humidity: number;
  };
  weather: Array<{
    description: string;
  }>;
}

/**
 * Fetches current weather data for a given city from the OpenWeatherMap API.
 * 
 * @param cityName The name of the city for which to fetch weather data.
 * @returns A promise resolving to an object containing temperature, humidity, and description.
 */
async function fetchWeatherData(cityName: string): Promise<{
  temperature: number;
  humidity: number;
  description: string;
}> {
  const apiKey = 'YOUR_API_KEY_HERE'; // Replace with your actual API key
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(cityName)}&appid=${apiKey}&units=metric`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data: WeatherResponse = await response.json();
    return {
      temperature: data.main.temp,
      humidity: data.main.humidity,
      description: data.weather[0].description
    };
  } catch (error) {
    console.error('Failed to fetch weather data:', error);
    throw new Error(`Fetch failed: ${String(error)}`);
  }
}

// Example usage:
fetchWeatherData('London')
  .then((weatherData) => {
    console.log(`Temperature: ${weatherData.temperature}°C, Humidity: ${weatherData.humidity}%, Description: ${weatherData.description}`);
  })
  .catch((error) => {
    console.error(error.message);
  });
```

### Key Points:
- **TypeScript Interface**: `WeatherResponse` is defined to match the expected structure of the OpenWeatherMap API response.
- **Async Function**: The function is marked as `async`, allowing the use of `await` within it.
- **Fetch API**: Utilizes the native `fetch` function for HTTP requests, compatible with modern browsers and Node.js (with a suitable polyfill if needed).
- **Error Handling**: Includes try/catch blocks to manage network errors or non-200 HTTP responses gracefully.
- **API Key Placeholder**: Replace `'YOUR_API_KEY_HERE'` with your actual OpenWeatherMap API key.

This function will return the current temperature in Celsius, humidity percentage, and a textual weather description for the specified city.

127 t/s, 571 tokens, 5s, 4%
