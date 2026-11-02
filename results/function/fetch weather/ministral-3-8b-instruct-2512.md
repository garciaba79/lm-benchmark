# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here's a TypeScript async function `fetchWeatherData` that fetches current weather data from OpenWeatherMap API using native `fetch`. It includes proper error handling and type definitions:

```typescript
interface WeatherResponse {
  temperature: number; // in Celsius
  humidity: number;
  description: string;
}

async function fetchWeatherData(cityName: string): Promise<WeatherResponse> {
  const apiKey = 'YOUR_PLACEHOLDER_API_KEY'; // Replace with your actual API key or use environment variables
  const baseUrl = 'https://api.openweathermap.org/data/2.5/weather';

  try {
    const response = await fetch(`${baseUrl}?q=${encodeURIComponent(cityName)}&units=metric&appid=${apiKey}`);

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    const data: any = await response.json();

    // Validate required fields exist
    if (!data.main || !data.weather || !data.weather[0]) {
      throw new Error('Invalid weather data format from API');
    }

    return {
      temperature: Math.round(data.main.temp), // Round to nearest integer
      humidity: data.main.humidity,
      description: data.weather[0].description
    };
  } catch (error) {
    console.error(`Error fetching weather for ${cityName}:`, error);
    throw new Error('Failed to fetch weather data. Please check the city name and try again.');
  }
}

// Example usage:
// fetchWeatherData('Paris')
//   .then(weather => console.log(weather))
//   .catch(err => console.error(err));
```

### Important Notes:

1. **API Key**: Replace `'YOUR_PLACEHOLDER_API_KEY'` with your actual OpenWeatherMap API key or use environment variables for security.

2. **Error Handling**:
   - Checks for HTTP errors (non-200 responses)
   - Validates the response structure
   - Provides user-friendly error messages

3. **Type Safety**:
   - Defines `WeatherResponse` interface with expected properties
   - Uses type assertions where needed while maintaining safety

4. **Units**:
   - Uses metric units (Celsius) by default in the API call

5. **Security**:
   - Encodes the city name to prevent potential injection issues

For production use, you might want to:
1. Store the API key in environment variables
2. Add more comprehensive error handling
3. Consider adding retry logic for failed requests
4. Implement caching if needed

127 t/s, 541 tokens, 4s, 7%
