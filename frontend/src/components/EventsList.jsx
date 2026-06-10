import { useQuery } from "@tanstack/react-query";
import { fetchEvents } from "../api";

export default function EventsList({ city }) {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["events", city],
    queryFn: () => fetchEvents(city),
  });

  if (isLoading) return <div className="card">Loading events...</div>;
  if (isError) return <div className="card">Failed to load events.</div>;

  return (
    <div className="card">
      <h2>Local Events</h2>
      {!data || data.events.length === 0 ? (
        <p className="no-results">No events found for {city}.</p>
      ) : (
        <ul className="events-list">
          {data.events.map((item) => (
            <li key={item.id} className="event-item">
              <a href={item.link} target="_blank" rel="noopener noreferrer">
                {item.title}
              </a>
              <span className="event-source">{item.source}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}