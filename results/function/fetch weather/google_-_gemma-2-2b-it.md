# Gemma 2 2B Instruct
Model: google_-_gemma-2-2b-it
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

```typescript
import { Response } from 'node:https';

interface WeatherDataResponse {
  main: {
    temp: number;
    humidity: number;
  };
  weather: [
    { description: string; icon?: string; }
  ];
}

async function fetchWeatherData(city: string): Promise<WeatherDataResponse> {
  try {
    const apiKey = 'YOUR_API_KEY'; // Replace with your actual OpenWeatherMap API key
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`);

    if (!response.ok) {
      throw new Error('Failed to fetch weather data'); 
    }

    const data: Response = await response.json(); // Assuming the API returns JSON
    return data as WeatherDataResponse;
  } catch (error) {
    console.error('Error fetching weather data:', error);
    throw error; 
  }
}

// Example usage:
fetchWeatherData('London')
  .then((data) => {
    const temperature = data.main.temp; // Extract temperature from the response
    const description = data.weather[0].description;
    console.log(`The weather in London is ${temperature}°C, ${description}`);
  })
  .catch((error) => console.error('Error:', error));

```


**Explanation:**

1. **Type Definitions:** 
   - The `WeatherDataResponse` interface specifies the expected structure of the JSON response from OpenWeatherMap API:
     * `main`: contains temperature and humidity
     * `weather`: an array of weather descriptions (one per day)
2. **Async Function (`fetchWeatherData`)**:
    * Takes a `city` string as input.
    * Uses `await fetch()` to make the network request, handling asynchronous operations.
    * Implements a try-catch block for error handling: 
       - If the response is not OK (not successful), it throws an error and handles it gracefully in the catch block.  
3. **API Call:**
   - Constructs the API URL with the `city` and your OpenWeatherMap API key (replace `YOUR_API_KEY`).
4. **Response Parsing:** 
    * The code assumes that the response is JSON format, so it uses `response.json()` to parse it into a JavaScript object.  The type annotation ensures you are working with the expected structure of your data. 
5. **Return Value and Error Handling**:
   - Returns the parsed weather data as a promise (the result from the API).


**Key Points:**

* **API Key:** Replace `YOUR_API_KEY` with your actual OpenWeatherMap API key to make it work. Get one for free on [https://openweathermap.org/api](https://openweathermap.org/api)
* **Error Handling**: The code uses a try-catch block to handle potential errors during the fetch request and parsing of the response.  


Let me know if you have any more questions or would like help with specific aspects!

233 t/s, 688 tokens, 3s, 9%
