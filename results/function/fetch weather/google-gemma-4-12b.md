# Gemma 4 12B
Model: google/gemma-4-12b
Test: Function Fetch Weather
Created: 11/03/2026, 12:56:30 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here is the TypeScript implementation.

I have included a custom `interface` to ensure type safety for the API response and the final returned object.

```typescript
/**
 * Represents the structure of the data returned by our function
 */
interface WeatherData {
  temperature: number; // Temperature in Celsius (or Kelvin, depending on units)
  humidity: number;
  description: string;
}

/**
 * Fetches current weather data for a given city using the OpenWeatherMap API.
 * 
 * @param city - The name of the city to query
 * @returns A promise that resolves to an object containing temperature, humidity, and description
 */
async function fetchWeatherData(city: string): Promise<WeatherData> {
  const apiKey = "YOUR_PLACEHOLDER_API_KEY"; // Replace with actual key
  // Using 'metric' units to get Celsius; change to 'imperial' for Fahrenheit
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      // Handle specific HTTP errors (e.g., 404 Not Found or 401 Unauthorized)
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    const data: any = await response.json();

    // Map the raw API response to our simplified WeatherData structure
    const result: WeatherData = {
      temperature: data.main?.temp,
      humidity: data.main?.humidity,
      description: data.weather?.[0]?.description || "No description available"
    };

    // Validate that the required fields exist before returning
    if (result.temperature === undefined || result.humidity === undefined) {
        throw new Error("Received incomplete data from weather service.");
    }

    return result;
  } catch (error) {
    // Graceful error handling: log the error and re-throw or return a default
    console.error(`Failed to fetch weather for ${city}:`, error);
    throw new Error(`Could not retrieve weather data: ${error instanceof Error ? error.message : String(error)}`);
  }
}

// --- Example Usage ---
async function example() {
  try {
    const data = await fetchWeatherData("London");
    console.log(`Current Weather in London: ${data.temperature}°C, Humidity: ${data.humidity}%, Conditions: ${data.description}`);
  } catch (err) {
    console.error("Main process caught error:", err);
  }
}

example();
```

### Key Features of this implementation:

1.  **Type Safety**: It uses an `interface` to define exactly what the function returns, ensuring that other parts of your application know exactly what fields are available.
2.  **URL Encoding**: I used `encodeURIComponent(city)` to ensure that cities with spaces (like "New York") don't break the URL structure.
3.  **Robust Error Handling**: The code checks `response.ok` before attempting to parse JSON. This is crucial because `fetch` only throws an error on network failures; 404s or 401s are technically successful HTTP exchanges and must be checked manually.
4.  **Data Mapping**: Instead of returning the raw, massive JSON object from OpenWeatherMap, it extracts only the specific fields you requested (`temperature`, `humidity`, `description`).
5.  **Standard Compliance**: Uses native `fetch` and standard TypeScript features without requiring external libraries like Axios.

82 t/s, 798 tokens, 10s
