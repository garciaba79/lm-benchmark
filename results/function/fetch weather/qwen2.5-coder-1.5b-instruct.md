# Qwen2.5 Coder 1.5B Instruct
Model: qwen2.5-coder-1.5b-instruct
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
// Import necessary types from TypeScript's built-in library
import { RequestInfo, Response } from 'node-fetch';

/**
 * Asynchronously fetches current weather data from OpenWeatherMap API.
 * 
 * @param city - The name of the city for which to fetch weather data.
 * @returns A promise resolving to an object with temperature, humidity, and description.
 */
async function fetchWeatherData(city: string): Promise<{ temperature: number; humidity: number; description: string }> {
    try {
        // Construct the API URL
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=YOUR_API_KEY&units=metric`;

        // Fetch data from the API
        const response: Response = await fetch(url);

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response
        const weatherData: any = await response.json();

        // Extract temperature, humidity, and description from the data
        const temperature = weatherData.main.temp;
        const humidity = weatherData.main.humidity;
        const description = weatherData.weather[0].description;

        return { temperature, humidity, description };
    } catch (error) {
        console.error('Error fetching weather data:', error);
        throw error; // Re-throw the error to propagate it
    }
}

// Example usage:
fetchWeatherData('London')
    .then(data => {
        console.log(`Temperature: ${data.temperature}°C, Humidity: ${data.humidity}%`);
        console.log(`Description: ${data.description}`);
    })
    .catch(error => {
        console.error('Failed to fetch weather data:', error);
    });
```

In this solution, we've created a TypeScript function `fetchWeatherData` that takes a city name as input and returns a promise. The function uses the native `fetch` API to make an HTTP request to the OpenWeatherMap API. It handles errors gracefully by catching any exceptions that occur during the fetch operation or parsing of the response. The example usage demonstrates how to call this function and handle its result.

339 t/s, 454 tokens, 1s, 7%
