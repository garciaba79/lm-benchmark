# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: Function Fetch Weather
Created: 11/03/2026, 12:33:36 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here is the complete TypeScript async function `fetchWeatherData` that uses native `fetch` to interact with the OpenWeatherMap API, includes proper error handling, and defines clear types.

### Prerequisites

This code assumes you have a standard Node.js or browser environment where the `globalThis.fetch` is available (which is true for modern browsers and often polyfilled/available in recent Node versions).

### TypeScript Implementation

```typescript
/**
 * Defines the structure of the relevant data we expect from the OpenWeatherMap API response.
 */
interface WeatherDetails {
    temperature: number; // Temperature in Celsius or Kelvin, depending on API units used
    humidity: number;
    description: string;
}

/**
 * Defines the structure of the raw JSON response from the API for type safety.
 * Note: This is simplified to only capture what we need.
 */
interface OpenWeatherApiResponse {
    main: {
        temp: number;      // Temperature in Kelvin by default
        humidity: number;  // Humidity percentage
    };
    weather: Array<{
        description: string; // Weather description (e.g., "clear sky")
    }>;
}

/**
 * Fetches current weather data for a given city from the OpenWeatherMap API.
 * 
 * @param cityName The name of the city to fetch data for.
 * @returns A Promise that resolves to an object containing temperature, humidity, and description.
 * @throws An error if the network request fails or the API returns an error status.
 */
async function fetchWeatherData(cityName: string): Promise<WeatherDetails> {
    // IMPORTANT: Replace with your actual OpenWeatherMap API Key
    const API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"; 
    const BASE_URL = "https://api.openweathermap.org/data/2.5/weather";

    if (!API_KEY || API_KEY === "YOUR_OPENWEATHERMAP_API_KEY") {
        throw new Error("API Key is missing. Please set your OpenWeatherMap API key.");
    }

    // Construct the full URL, specifying units=metric for Celsius
    const url = `${BASE_URL}?q=${encodeURIComponent(cityName)}&appid=${API_KEY}&units=metric`;

    console.log(`Fetching weather data for ${cityName}...`);

    try {
        // 1. Perform the fetch request
        const response = await fetch(url);

        // 2. Handle HTTP error statuses (e.g., 404 Not Found, 401 Unauthorized)
        if (!response.ok) {
            let errorMessage = `HTTP Error! Status: ${response.status} (${response.statusText})`;
            
            // Attempt to read error details from the body if available
            const errorBody = await response.json().catch(() => ({ message: "No detailed error body provided." }));
            if (errorBody.message) {
                errorMessage += ` - Details: ${errorBody.message}`;
            }

            throw new Error(errorMessage);
        }

        // 3. Parse the JSON response
        const data: OpenWeatherApiResponse = await response.json();

        // 4. Map the raw API data to our desired, clean return structure
        if (!data || !data.main || !data.weather || data.weather.length === 0) {
             throw new Error("Received incomplete or unexpected weather data structure.");
        }
        
        const temperature = data.main.temp;
        const humidity = data.main.humidity;
        // We take the description from the first element in the weather array
        const description = data.weather[0].description;

        return {
            temperature: Math.round(temperature), // Round for cleaner display
            humidity: humidity,
            description: description,
        };

    } catch (error) {
        // 5. Catch network errors or any other thrown exceptions
        console.error("Failed to fetch weather data:", error);
        // Re-throw a more user-friendly error message
        if (error instanceof Error) {
             throw new Error(`Could not retrieve weather for ${cityName}. Reason: ${(error as Error).message}`);
        } else {
            throw new Error("An unknown error occurred during the fetch operation.");
        }
    }
}

// --- Example Usage ---

async function main() {
    try {
        // Successful case
        const weather = await fetchWeatherData("London");
        console.log("\n✅ Success! Weather in London:");
        console.log(`   Temperature: ${weather.temperature}°C`);
        console.log(`   Humidity: ${weather.humidity}%`);
        console.log(`   Conditions: ${weather.description}`);

    } catch (error) {
        if (error instanceof Error) {
            console.error("\n❌ Main execution error caught:", error.message);
        }
    }

    console.log("\n" + "=".repeat(30) + "\n");
    
    try {
        // Failure case: City does not exist (will likely hit a 404 status code handled by the function)
        await fetchWeatherData("NonExistentCity123XYZ");

    } catch (error) {
         if (error instanceof Error) {
            console.error("\n✅ Successfully caught expected error:", error.message);
        }
    }
}

// Run the examples
main();
```

144 t/s, 1196 tokens, 8s
