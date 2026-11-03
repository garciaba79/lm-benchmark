# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Function Fetch Weather
Created: 11/03/2026, 02:52:27 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
interface WeatherResponse {
  main: {
    temp: number;
    humidity: number;
  };
  weather: [
    {
      description: string;
    }
  ];
}

interface WeatherData {
  temperature: number;
  humidity: number;
  description: string;
}

async function fetchWeatherData(city: string): Promise<WeatherData> {
  try {
    // Using a placeholder API key - in production, you'd want to use environment variables
    const apiKey = 'YOUR_API_KEY_HERE';
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`;
    
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
    if (error instanceof Error) {
      throw new Error(`Failed to fetch weather data: ${error.message}`);
    } else {
      throw new Error('Failed to fetch weather data: Unknown error occurred');
    }
  }
}

// Example usage:
/*
fetchWeatherData('London')
  .then(data => {
    console.log(`Temperature: ${data.temperature}°C`);
    console.log(`Humidity: ${data.humidity}%`);
    console.log(`Description: ${data.description}`);
  })
  .catch(error => {
    console.error(error.message);
  });
*/
```

This TypeScript function includes:

1. **Type Definitions**:
   - `WeatherResponse`: Interface for the OpenWeatherMap API response structure
   - `WeatherData`: Interface for the clean, structured data we return

2. **Key Features**:
   - Uses native `fetch` API
   - Proper async/await handling
   - Comprehensive error handling with try/catch
   - URL encoding for city names with special characters
   - Units set to metric (Celsius)
   - Placeholder API key (replace with your actual key)

3. **Error Handling**:
   - Network errors
   - HTTP status errors
   - JSON parsing errors
   - General unknown errors

4. **Return Format**:
   - Clean object with temperature, humidity, and description
   - All values properly typed

To use this function, you'll need to replace `'YOUR_API_KEY_HERE'` with your actual OpenWeatherMap API key. The function handles various error scenarios gracefully and returns a promise that resolves to the structured weather data.

62 t/s, 552 tokens, 9s
