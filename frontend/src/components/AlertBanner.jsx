import { useQuery } from "@tanstack/react-query";
import { fetchAlerts } from "../api";

export default function AlertBanner() {
  const { data } = useQuery({
    queryKey: ["alerts"],
    queryFn: fetchAlerts,
    refetchInterval: 10 * 60 * 1000,
  });

  if (!data || data.alerts.length === 0) return null;

  const topAlerts = data.alerts.slice(0, 3);

  return (
    <div className="alert-banner">
      <div className="alert-banner-icon">⚠️</div>
      <div className="alert-banner-content">
        {topAlerts.map((alert, i) => (
          <div key={i} className="alert-banner-item">
            <strong>{alert.event}</strong> — {alert.area_desc.split(";")[0]}
          </div>
        ))}
      </div>
    </div>
  );
}