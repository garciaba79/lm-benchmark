# Qwen2.5 Coder 7B Instruct
Model: qwen2.5-coder-7b-instruct
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here's how you can write the `fetchWeatherData` function in TypeScript:

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

async function fetchWeatherData(cityName: string): Promise<WeatherResponse> {
  const apiKey = 'your_placeholder_api_key';
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=${apiKey}`;

  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: WeatherResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching weather data:', error);
    throw error; // Rethrow the error to handle it further up in the call stack
  }
}

// Example usage:
fetchWeatherData('London')
  .then(data => {
    console.log(`Temperature: ${data.main.temp}K, Humidity: ${data.main.humidity}%, Description: ${data.weather[0].description}`);
  })
  .catch(error => {
    console.error('Failed to fetch weather data:', error);
  });
```

### Explanation:

1. **Type Definitions**:
   - `WeatherResponse` interface defines the structure of the expected response from the OpenWeatherMap API.
   
2. **Function Definition**:
   - `fetchWeatherData` is an async function that takes a city name as input and returns a promise resolving to a `WeatherResponse`.

3. **API Key Placeholder**:
   - Replace `'your_placeholder_api_key'` with your actual OpenWeatherMap API key.

4. **Fetching Data**:
   - The `fetch` function is used to make the HTTP request.
   - If the response status is not OK (i.e., not in the range 200-299), an error is thrown.
   
5. **Error Handling**:
   - Errors are caught and logged using a try/catch block. The error is then rethrown to be handled further up the call stack.

6. **Example Usage**:
   - Demonstrates how to use `fetchWeatherData` and handle its promise.

Make sure you have an active API key from OpenWeatherMap and replace `'your_placeholder_api_key'` with your actual key before running this code.

149 t/s, 511 tokens, 3s, 4%
