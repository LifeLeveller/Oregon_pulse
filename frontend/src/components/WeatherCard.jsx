import { useQuery } from "@tanstack/react-query";
import { fetchWeather } from "../api";

export default function WeatherCard({ city }) {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["weather", city],
    queryFn: () => fetchWeather(city),
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) return <div className="card">Loading weather...</div>;
  if (isError) return <div className="card">Failed to load weather.</div>;
  if (!data) return <div className="card">No weather data.</div>;

  return (
    <div className="card">
      <h2>{data.city} Weather</h2>
      <div className="weather-temp">{Math.round(data.temp_f)}°F</div>
      <div className="weather-desc">{data.description}</div>
      <div className="weather-details">
        <span>Feels like {Math.round(data.feels_like_f)}°F</span>
        <span>Humidity {data.humidity}%</span>
        <span>Wind {data.wind_speed} mph</span>
      </div>
    </div>
  );
}