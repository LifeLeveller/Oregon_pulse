import { useState } from "react";
import WeatherCard from "./components/WeatherCard";
import NewsFeed from "./components/NewsFeed";
import EventsList from "./components/EventsList";
import CityFilter from "./components/CityFilter";
import AlertBanner from "./components/AlertBanner";
import WildfireWidget from "./components/WildfireWidget";
import "./App.css";

export default function App() {
  const [selectedCity, setSelectedCity] = useState("Portland");

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
            <p>Oregon local dashboard</p>
            <span className="header-copyright">© 2026 Sriranjini Sridhar</span>
          </div>
        </div>
      </header>
      <AlertBanner />
      <CityFilter selectedCity={selectedCity} onCityChange={setSelectedCity} />
      <main className="dashboard">
        <WeatherCard city={selectedCity} />
        <NewsFeed city={selectedCity} />
        <EventsList city={selectedCity} />
      </main>
      <div className="secondary-dashboard">
        <WildfireWidget />
      </div>
      <footer className="footer">
        <p>© {new Date().getFullYear()} Sriranjini Sridhar. All rights reserved.</p>
        <p>Built with Python, FastAPI, React and deployed on Railway and Vercel.</p>
      </footer>
    </div>
  );
}