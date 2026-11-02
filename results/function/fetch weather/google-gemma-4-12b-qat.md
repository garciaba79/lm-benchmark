# Gemma 4 12B QAT
Model: google/gemma-4-12b-qat
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here is the complete solution using TypeScript. I have included the necessary interfaces to ensure type safety for the API response and the final return object.

```typescript
/**
 * Type definitions for the OpenWeatherMap API response structure
 */
interface OpenWeatherResponse {
  name: string;
  main: {
    temp: number;
    humidity: number;
  };
  weather: Array<{
    description: string;
  }>;
  cod: number;
}

/**
 * Type definition for our simplified return object
 */
interface WeatherData {
  temperature: number;
  humidity: number;
  description: string;
}

/**
 * Fetches current weather data for a given city.
 * @param city - The name of the city to fetch weather for.
 * @returns A promise resolving to a WeatherData object.
 * @throws Error if the city is not found or the network request fails.
 */
async function fetchWeatherData(city: string): Promise<WeatherData> {
  const API_KEY = "YOUR_PLACEHOLDER_API_KEY"; // Replace with real key
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=metric`;

  try {
    const response = await fetch(url);

    // Check if the HTTP response status is successful (200-299)
    if (!response.ok) {
      // Handle specific status codes (e.g., 404 for city not found)
      if (response.status === 404) {
        throw new Error(`City "${city}" not found.`);
      }
      throw new Error(`Network error: ${response.statusText}`);
    }

    // Parse the JSON body
    const data: OpenWeatherResponse = await response.json();

    // Return the formatted object
    return {
      temperature: data.main.temp,
      humidity: data.main.humidity,
      description: data.weather[0].description,
    };

  } catch (error) {
    // Log the error and re-throw or handle it as needed
    if (error instanceof Error) {
      console.error(`Error fetching weather: ${error.message}`);
    } else {
      console.error("An unknown error occurred.");
    }
    
    // Re-throwing allows the caller to handle the error (e.g., showing a UI alert)
    throw error;
  }
}

// --- Example Usage ---
(async () => {
  try {
    const weather = await fetchWeatherData("London");
    console.log(`Current Weather in London: ${weather.temperature}°C, ${weather.description} (Humidity: ${weather.humidity}%)`);
  } catch (err) {
    // Errors are handled here
  }
})();
```

### Key Features of this implementation:
1.  **Type Safety**: It defines `OpenWeatherResponse` to map the complex nested structure of the API, while `WeatherData` defines the clean, flattened object we actually want to use in our application.
2.  **URL Encoding**: Uses `encodeURIComponent(city)` to ensure that cities with spaces (like "New York") don't break the URL string.
3.  **Error Handling**: 
    *   It checks `response.ok` because `fetch` does not throw an error on 404 or 500 status codes; it only throws on network failures.
    *   It specifically checks for `404` to provide a more user-friendly error message.
4.  **Units**: I added `&units=metric` to the URL so the temperature is returned in Celsius (you can change this to `imperial` for Fahrenheit).
5.  **Native Fetch**: Uses the standard Web API `fetch` as requested, making it compatible with modern browsers and Node.js 18+.

95 t/s, 873 tokens, 9s, 6%
