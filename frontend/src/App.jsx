import WeatherCard from "./components/WeatherCard";
import NewsFeed from "./components/NewsFeed";
import EventsList from "./components/EventsList";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <header className="header">
        <h1>Oregon Pulse</h1>
        <p>West Linn and Oregon local dashboard</p>
      </header>
      <main className="dashboard">
        <WeatherCard />
        <NewsFeed />
        <EventsList />
      </main>
    </div>
  );
}