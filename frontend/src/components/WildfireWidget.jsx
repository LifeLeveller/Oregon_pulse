import { useQuery } from "@tanstack/react-query";
import { fetchWildfires } from "../api";

export default function WildfireWidget() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["wildfires"],
    queryFn: fetchWildfires,
  });

  if (isLoading) return <div className="card">Loading wildfire data...</div>;
  if (isError) return <div className="card">Failed to load wildfire data.</div>;

  return (
    <div className="card">
      <h2>Active Wildfires</h2>
      {data.wildfires.length === 0 ? (
        <p className="no-results">No active fire detections in Oregon right now.</p>
      ) : (
        <ul className="wildfire-list">
          {data.wildfires.slice(0, 10).map((fire, i) => (
            <li key={i} className="wildfire-item">
              <span className={`confidence-badge confidence-${fire.confidence}`}>
                {fire.confidence === "h" ? "High" : "Nominal"} confidence
              </span>
              <span className="wildfire-coords">
                {fire.latitude.toFixed(3)}, {fire.longitude.toFixed(3)}
              </span>
              <span className="wildfire-date">{fire.acq_date}</span>
            </li>
          ))}
        </ul>
      )}
      <p className="wildfire-source">Data: NASA FIRMS satellite detection</p>
    </div>
  );
}