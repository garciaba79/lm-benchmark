# Microsoft Phi 4 Mini Instruct
Model: microsoft_phi-4-mini-instruct
Test: Function Fetch Weather
Created: 11/02/2026, 12:49:08 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript async function called fetchWeatherData that takes a city name string as input and fetches current weather data from the OpenWeatherMap API (use a placeholder API key). It should return a promise resolving to an object with temperature, humidity, and description. Handle errors gracefully with try/catch, and include type definitions for the response. Use native fetch, no external libraries.

> #### 🤖 Assistant

// TypeScript interface representing expected structure of weather data
interface WeatherData {
  main: { temp: number; humidity: number };
  weather: [{ id: string; description: string }];
}

// Function to retrieve current weather information given a city name using OpenWeatherMap API.
async function fetchWeatherData(cityName: string): Promise<WeatherData> {
  const apiKey = 'YOUR_API_KEY'; // Replace with your actual API key
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=${apiApiKey}`;

  try {
    const response = await fetch(url);
    
    if (!response.ok) { 
      throw new Error(`Failed to get weather data: ${response.status} - ${await (response.text())}`);
    }

    // Parse JSON and extract relevant fields
    const jsonData = await response.json();
    return {
      temperature: jsonData.main.temp,
      humidity: jsonData.main.humidity,
      description: jsonData.weather[0].description
    };
  } catch (error) { 
    console.error('Error fetching weather data:', error.message);
    
    // Resolve promise with an empty object in case of failure to handle gracefully.
    return Promise.resolve({});
  }
}

209 t/s, 260 tokens, 1s, 2%
