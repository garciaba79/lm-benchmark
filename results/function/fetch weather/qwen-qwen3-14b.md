# Qwen3 14B
Model: qwen/qwen3-14b
Test: Function Fetch Weather
Created: 11/03/2026, 01:06:00 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here's a complete TypeScript function called `fetchWeatherData` that fulfills your requirements:

### ✅ Features:
- Uses **native `fetch()`**.
- Uses **async/await** with **try/catch** for error handling.
- Returns an object with **temperature**, **humidity**, and **description**.
- Includes **type definitions** (using TypeScript interfaces).
- Uses a **placeholder API key** from OpenWeatherMap.

---

### 🌐 OpenWeatherMap API Documentation Reference:
- Base URL: `https://api.openweathermap.org/data/2.5/weather`
- Query parameters: `q={cityName}&appid={apiKey}&units=metric`

---

### ✅ TypeScript Code:

```typescript
// Define a type for the weather data response
interface WeatherData {
  temperature: number;
  humidity: number;
  description: string;
}

// Async function to fetch weather data
async function fetchWeatherData(cityName: string): Promise<WeatherData> {
  const apiKey = 'your-placeholder-api-key-here'; // Replace with actual API key

  try {
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(cityName)}&appid=${apiKey}&units=metric`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Extract and return required weather information
    return {
      temperature: data.main.temp,
      humidity: data.main.humidity,
      description: data.weather[0].description
    };

  } catch (error) {
    console.error('Failed to fetch weather data:', error);
    throw new Error(`Could not retrieve weather data for ${cityName}: ${error.message}`);
  }
}

// Example usage:
fetchWeatherData('London')
  .then(data => console.log('Weather Data:', data))
  .catch(error => console.error('Error:', error));
```

---

### 🧪 Notes:

- Replace `'your-placeholder-api-key-here'` with a real [OpenWeatherMap API key](https://home.openweathermap.org/api_keys).
- You may need to install TypeScript if you haven't already, or use it in your project setup.
- The `encodeURIComponent(cityName)` ensures the city name is properly URL-encoded.

Let me know if you want this wrapped into a class or module structure!

80 t/s, 499 tokens, 6s
