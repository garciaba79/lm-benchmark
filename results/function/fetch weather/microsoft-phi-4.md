# Phi 4
Model: microsoft/phi-4
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

To create a TypeScript async function `fetchWeatherData` that retrieves weather data from the OpenWeatherMap API, you need to follow these steps:

1. Define types for the expected response.
2. Construct the URL with the city name and placeholder API key.
3. Use the native `fetch` API to make an HTTP request.
4. Parse the JSON response and extract relevant information.
5. Handle any potential errors gracefully.

Below is a complete implementation of the function:

```typescript
type WeatherApiResponse = {
  main: {
    temp: number; // Temperature in Kelvin by default
    humidity: number;
  };
  weather: Array<{
    description: string;
  }>;
};

type WeatherData = {
  temperature: number; // Celsius or Fahrenheit depending on API settings
  humidity: number;
  description: string;
};

async function fetchWeatherData(cityName: string): Promise<WeatherData> {
  const apiKey = 'YOUR_PLACEHOLDER_API_KEY'; // Replace with your actual OpenWeatherMap API key
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(cityName)}&appid=${apiKey}&units=metric`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Error fetching weather data: ${response.statusText}`);
    }

    const data: WeatherApiResponse = await response.json();

    const temperature = data.main.temp;
    const humidity = data.main.humidity;
    const description = data.weather[0].description;

    return { temperature, humidity, description };
  } catch (error) {
    console.error(`Failed to fetch weather data for ${cityName}:`, error);
    throw new Error('Unable to fetch weather data. Please try again later.');
  }
}

// Usage example:
fetchWeatherData('London')
  .then((weatherData) => {
    console.log(weatherData);
  })
  .catch((error) => {
    console.error(error.message);
  });
```

### Explanation:

- **Type Definitions:**
  - `WeatherApiResponse`: Defines the structure of the JSON response from OpenWeatherMap.
  - `WeatherData`: Defines the structure of the data we want to return, including temperature in Celsius (metric units), humidity, and a description.

- **API Key:** Replace `'YOUR_PLACEHOLDER_API_KEY'` with your actual API key obtained from OpenWeatherMap.

- **Error Handling:**
  - The function uses `try/catch` to handle errors that may occur during the fetch operation or JSON parsing.
  - If the response status is not OK, it throws an error with a descriptive message.

- **Units:** The query parameter `units=metric` ensures the temperature is returned in Celsius. You can change this to `imperial` for Fahrenheit if needed.

This function provides a robust way to fetch and handle weather data using TypeScript's type safety features.

82 t/s, 596 tokens, 7s, 4%
