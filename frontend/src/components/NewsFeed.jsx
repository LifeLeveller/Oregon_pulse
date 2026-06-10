import { useQuery } from "@tanstack/react-query";
import { fetchHeadlines } from "../api";

export default function NewsFeed({ city }) {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["headlines", city],
    queryFn: () => fetchHeadlines(city),
  });

  if (isLoading) return <div className="card">Loading headlines...</div>;
  if (isError) return <div className="card">Failed to load headlines.</div>;

  return (
    <div className="card">
      <h2>Oregon News</h2>
      {data.headlines.length === 0 ? (
        <p className="no-results">No headlines found for {city}.</p>
      ) : (
        <ul className="news-list">
          {data.headlines.map((item) => (
            <li key={item.id} className="news-item">
              <a href={item.link} target="_blank" rel="noopener noreferrer">
                {item.title}
              </a>
              <span className="news-source">{item.source}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}