import WeatherCard from "./components/WeatherCard";
import NewsFeed from "./components/NewsFeed";
import EventsList from "./components/EventsList";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <header className="header">
        <div className="header-banner">
          <img
            src="https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1200&q=80"
            alt="Oregon landscape"
            className="header-image"
          />
          <div className="header-overlay">
            <h1>Oregon Pulse</h1>
            <p>West Linn and Oregon local dashboard</p>
            <span className="header-copyright">© 2026 Sriranjini Sridhar</span>
          </div>
        </div>
      </header>
      <main className="dashboard">
        <WeatherCard />
        <NewsFeed />
        <EventsList />
      </main>
    </div>
  );
}