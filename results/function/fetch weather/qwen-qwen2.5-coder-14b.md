# Qwen2.5 Coder 14B
Model: qwen/qwen2.5-coder-14b
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

To create a TypeScript async function that fetches weather data from the OpenWeatherMap API, you'll need to define the structure of the response and handle potential errors using try/catch blocks. Below is an example implementation:

```typescript
interface WeatherData {
  temperature: number;
  humidity: number;
  description: string;
}

async function fetchWeatherData(cityName: string): Promise<WeatherData> {
  const apiKey = 'YOUR_PLACEHOLDER_API_KEY'; // Replace with your actual API key
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=${apiKey}&units=metric`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    // Extract the necessary information from the response
    const temperature = data.main.temp;
    const humidity = data.main.humidity;
    const description = data.weather[0].description;

    return {
      temperature,
      humidity,
      description,
    };
  } catch (error) {
    console.error('Error fetching weather data:', error);
    throw error; // Rethrow the error to be handled by the caller
  }
}

// Example usage:
fetchWeatherData('London')
  .then(data => {
    console.log(`Temperature: ${data.temperature}°C, Humidity: ${data.humidity}%, Description: ${data.description}`);
  })
  .catch(error => {
    console.error('Failed to fetch weather data:', error);
  });
```

### Explanation:

1. **Interface Definition**: We define a `WeatherData` interface to specify the structure of the object that our function will return. This includes properties for temperature, humidity, and description.

2. **Function Implementation**:
   - The function `fetchWeatherData` is declared as `async`, allowing us to use `await` for asynchronous operations.
   - We construct the API URL using the city name and a placeholder API key. Make sure to replace `'YOUR_PLACEHOLDER_API_KEY'` with your actual OpenWeatherMap API key.
   - We use `fetch` to make a GET request to the OpenWeatherMap API.
   - If the response is not successful (i.e., `response.ok` is false), we throw an error with the status code.
   - We parse the JSON response and extract the temperature, humidity, and weather description from the data.
   - The extracted data is returned as a `WeatherData` object.

3. **Error Handling**:
   - Errors are caught in the `catch` block, where we log the error message to the console.
   - The error is rethrown to be handled by the caller of the function.

This implementation ensures that you can fetch weather data for a given city and handle any potential errors gracefully.

79 t/s, 594 tokens, 8s, 4%
