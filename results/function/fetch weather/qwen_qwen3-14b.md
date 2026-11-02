# Qwen Qwen3 14B
Model: qwen_qwen3-14b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
// Define the interface for the weather data structure
interface WeatherData {
  temperature: number;
  humidity: number;
  description: string;
}

// Placeholder API key (replace with actual key in production)
const API_KEY = 'your_api_key_here';

/**
 * Asynchronously fetches current weather data from OpenWeatherMap API.
 * @param city - The name of the city for which to retrieve weather data.
 * @returns A Promise resolving to an object containing temperature, humidity, and description.
 */
async function fetchWeatherData(city: string): Promise<WeatherData> {
  try {
    // Construct the API URL with the provided city and placeholder API key
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${API_KEY}`
    );

    // Check if the HTTP response is successful (status code in 2xx range)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Parse JSON data from the response
    const data = await response.json();

    // Extract temperature, humidity, and weather description from the API response
    return {
      temperature: data.main.temp,
      humidity: data.main.humidity,
      description: data.weather[0].description
    };
  } catch (error) {
    // Handle any errors that occur during the fetch or parsing process
    console.error('Error fetching weather data:', error);
    throw new Error('Failed to retrieve weather data. Please try again later.');
  }
}

// Example usage:
// fetchWeatherData("London")
//   .then(data => console.log(data))
//   .catch(error => console.error(error));
```

---

### ✅ Features:

- **Type Safety**: Uses TypeScript interfaces (`WeatherData`) for clear and safe data handling.
- **Error Handling**: Catches and logs errors, then rethrows a user-friendly error message to handle gracefully.
- **URL Encoding**: Uses `encodeURIComponent` to ensure the city name is safely encoded in the URL.
- **Graceful Failure**: If the API returns an HTTP error (e.g., 404), it throws a descriptive error instead of silently failing.

---

### 📌 Notes:

- Replace `'your_api_key_here'` with your actual OpenWeatherMap API key for production use.
- The temperature is returned in Kelvin as per the default behavior of the OpenWeatherMap API. If needed, you can convert it to Celsius or Fahrenheit within this function.

10 t/s, 1639 tokens, 167s, 21%
