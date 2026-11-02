# LFM2.5 1.2B Instruct
Model: lfm2.5-1.2b-instruct
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

Here's a TypeScript async function called `fetchWeatherData` that accepts a city name string, fetches current weather data from the OpenWeatherMap API (using a placeholder API key), and returns an object with temperature, humidity, and description:

```typescript
// Define the shape of the response from OpenWeatherMap API
interface WeatherResponse {
  main: Main;
}

interface Main {
  temp: number; // Temperature in Kelvin by default
  pressure: number; // Pressure in hPa
  humidity: number;
  description: string;
}

interface CityInfo {
  cityName: string;
  temperature: number; // Temperature in Celsius
  humidity: number;
  description: string;
}

// Placeholder API key (not secure for production)
const PLACEHOLDER_API_KEY = 'your_placeholder_api_key';

async function fetchWeatherData(cityName: string): Promise<CityInfo> {
  const apiKey = PLACEHOLDER_API_KEY;
  const baseUrl = `https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=${apiKey}`;

  try {
    const response = await fetch(baseUrl);
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    const data: WeatherResponse = await response.json();

    // Extract relevant fields
    const tempCelsius = (data.main.temp - 273.15).toFixed(2); // Convert to Celsius
    const humidity = data.main.humidity;
    const description = data.weather[0].description;

    return {
      cityName,
      temperature: tempCelsius,
      humidity,
      description,
    };
  } catch (error) {
    console.error('Error fetching weather data:', error);
    throw new Error('Could not retrieve weather data');
  }
}
```

### Usage Example:
```typescript
fetchWeatherData('London')
  .then(cityInfo => {
    console.log(cityInfo);
  })
  .catch(error => {
    console.error(error);
  });
```

### Notes:
- Replace `'your_placeholder_api_key'` with a valid API key from [OpenWeatherMap](https://openweathermap.org/api).
- The function returns the city's name, temperature in Celsius, humidity, and a weather description.
- Errors are handled gracefully using `try/catch`.

Let me know if you'd like to include more details like wind speed or country code!

581 t/s, 561 tokens, 1s, 4%
