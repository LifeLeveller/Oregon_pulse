const CITIES = [
  "Oregon",
  "Portland",
  "Salem",
  "Eugene",
  "West Linn",
  "Lake Oswego",
  "Bend",
  "Medford",
  "Ashland",
  "Corvallis",
  "Hillsboro",
  "Beaverton",
];

export default function CityFilter({ selectedCity, onCityChange }) {
  return (
    <div className="city-filter">
      <label htmlFor="city-select">Filter by city:</label>
      <select
        id="city-select"
        value={selectedCity}
        onChange={(e) => onCityChange(e.target.value)}
      >
        {CITIES.map((city) => (
          <option key={city} value={city}>
            {city === "Oregon" ? "All Oregon" : city}
          </option>
        ))}
      </select>
    </div>
  );
}