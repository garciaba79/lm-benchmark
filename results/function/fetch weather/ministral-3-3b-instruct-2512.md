# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here's a TypeScript async function that fetches weather data from OpenWeatherMap using `fetch` (native browser API) with proper error handling:

```typescript
interface WeatherData {
    temperature: number;
    humidity: number;
    description: string;
}

async function fetchWeatherData(cityName: string): Promise<WeatherData> {
    // Replace with your actual OpenWeatherMap API key
    const API_KEY = 'YOUR_API_KEY_HERE';
    const API_URL = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(
        cityName
    )}&appid=${API_KEY}&units=metric`;

    try {
        // Fetch weather data from OpenWeatherMap API
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Extract relevant weather information
        return {
            temperature: data.main.temp,
            humidity: data.main.humidity,
            description: data.weather[0].description
        };
    } catch (error) {
        console.error('Error fetching weather data:', error);
        throw new Error(`Failed to fetch weather data for ${cityName}. Please try again later.`);
    }
}

// Example usage:
// fetchWeatherData('London')
//     .then(data => console.log(data))
//     .catch(err => console.error(err));
```

### Key Features:
1. **Type Definitions**: Uses an `interface WeatherData` to define the expected response structure
2. **Error Handling**:
   - Checks for HTTP errors (non-200 responses)
   - Catches network/parsing errors
3. **API Configuration**:
   - Uses OpenWeatherMap's current weather endpoint
   - Includes proper URL encoding for city names
4. **Units**: Sets `units=metric` to get temperatures in Celsius
5. **Clean Response**: Returns only the requested fields (temperature, humidity, description)

### Notes:
- Replace `'YOUR_API_KEY_HERE'` with an actual OpenWeatherMap API key
- The function uses the metric units system by default - change to `imperial` if you need Fahrenheit/Celsius
- For production use, consider adding rate limiting and caching
- The example shows how to call it as a promise (you can also chain `.then()` or use async/await)

231 t/s, 508 tokens, 2s, 7%
