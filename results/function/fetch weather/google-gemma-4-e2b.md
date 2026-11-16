# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: Function Fetch Weather
Created: 11/15/2026, 09:41:04 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here is the complete TypeScript implementation for the `fetchWeatherData` async function using the native `fetch` API.

### Prerequisites

Make sure you have a TypeScript environment set up (e.g., Node.js with TypeScript installed).

### TypeScript Implementation

```typescript
/**
 * Defines the structure of the weather data we expect from the API.
 */
interface WeatherData {
    temperature: number;
    humidity: number;
    description: string;
}

/**
 * Fetches current weather data for a given city from the OpenWeatherMap API.
 *
 * @param city The name of the city to fetch weather data for.
 * @returns A Promise that resolves to an object containing temperature, humidity, and description.
 * @throws An error if the network request fails or the API returns an error.
 */
async function fetchWeatherData(city: string): Promise<WeatherData> {
    // --- Configuration ---
    // IMPORTANT: Replace this with your actual OpenWeatherMap API key
    const API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"; 
    const BASE_URL = "https://api.openweathermap.org/data/2.5/weather";

    if (!API_KEY || API_KEY === "YOUR_OPENWEATHERMAP_API_KEY") {
        throw new Error("API Key is missing or not configured. Please set a valid OpenWeatherMap API key.");
    }

    // Construct the full API URL
    const url = `${BASE_URL}?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=metric`; // 'units=metric' for Celsius

    try {
        // 1. Perform the network request
        const response = await fetch(url);

        // 2. Check if the HTTP response status code indicates success (200-299)
        if (!response.ok) {
            // Throw an error with the status text if the response is not okay (e.g., 404, 401)
            const errorBody = await response.json().catch(() => ({ message: `HTTP Error: ${response.status}` }));
            throw new Error(`Failed to fetch weather data. Status: ${response.status}. Message: ${errorBody.message || 'Unknown error'}`);
        }

        // 3. Parse the JSON response
        const data = await response.json();

        // 4. Extract the required fields and map them to our expected interface
        if (data && data.main && data.weather && data.weather.length > 0) {
            const temperature = data.main.temp;
            const humidity = data.main.humidity;
            // The description is usually an array, we take the first element
            const description = data.weather[0].description;

            return {
                temperature: temperature,
                humidity: humidity,
                description: description,
            };
        } else {
            throw new Error(`Unexpected data structure received from API for city: ${city}`);
        }

    } catch (error) {
        // Graceful error handling for network errors or thrown custom errors
        console.error(`Error fetching weather for ${city}:`, error);
        // Re-throw a standardized error to be handled by the caller
        throw new Error(`Could not retrieve weather data for ${city}. Details: ${error instanceof Error ? error.message : String(error)}`);
    }
}

// --- Example Usage ---
async function main() {
    const city1 = "London";
    const city2 = "Tokyo";
    const invalidCity = "NonExistentCityXYZ";

    console.log("--- Fetching Weather for London ---");
    try {
        const londonData = await fetchWeatherData(city1);
        console.log(`✅ Success for ${city1}:`);
        console.log(`Temperature: ${londonData.temperature}°C`);
        console.log(`Humidity: ${londonData.humidity}%`);
        console.log(`Description: ${londonData.description}`);
    } catch (error) {
        console.error(`❌ Error fetching London data: ${error instanceof Error ? error.message : String(error)}`);
    }

    console.log("\n--- Fetching Weather for Tokyo ---");
    try {
        const tokyoData = await fetchWeatherData(city2);
        console.log(`✅ Success for ${city2}:`);
        console.log(`Temperature: ${tokyoData.temperature}°C`);
        console.log(`Humidity: ${tokyoData.humidity}%`);
        console.log(`Description: ${tokyoData.description}`);
    } catch (error) {
        console.error(`❌ Error fetching Tokyo data: ${error instanceof Error ? error.message : String(error)}`);
    }

    console.log("\n--- Testing Error Handling (Invalid City) ---");
    try {
        await fetchWeatherData(invalidCity);
    } catch (error) {
        console.error(`❌ Successfully caught expected error for ${invalidCity}: ${error instanceof Error ? error.message : String(error)}`);
    }
}

main();
```

### Explanation of Key Components:

1.  **`interface WeatherData`**: Defines a clear contract for the data returned by the function, improving type safety.
2.  **`async function fetchWeatherData(city: string): Promise<WeatherData>`**: Declares the function as asynchronous and explicitly states that it returns a `Promise` which will resolve to an object matching the `WeatherData` structure.
3.  **API Key Handling**: It includes a check for the API key, ensuring the function fails early if crucial configuration is missing. (Remember to replace the placeholder!)
4.  **`await fetch(url)`**: Uses the native `fetch` API to request data from the constructed URL.
5.  **Error Checking (`response.ok`)**: This is critical. `fetch` only throws an error for network failures, not for HTTP error codes (like 404 Not Found or 401 Unauthorized). We must manually check `response.ok` and throw a detailed error if the response status is not successful.
6.  **JSON Parsing**: `await response.json()` parses the stream into a JavaScript object.
7.  **Data Extraction**: It safely navigates the nested structure of the OpenWeatherMap response (`data.main.temp`, `data.main.humidity`, etc.) and maps it to the simple `WeatherData` interface before returning the final result.
8.  **`try...catch` Block**: The entire process is wrapped in a `try...catch` block to handle network failures, invalid API responses, or errors thrown during manual data processing, ensuring the function always resolves its promise (either with data or an error).

197 t/s, 1479 tokens, 8s
