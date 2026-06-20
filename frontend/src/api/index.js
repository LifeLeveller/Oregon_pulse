import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
});

export const fetchHeadlines = async (city = null) => {
  const params = city && city !== "Oregon" ? { city } : {};
  const { data } = await api.get("/headlines", { params });
  return data;
};

export const fetchWeather = async (city = "Oregon") => {
  const params = { city };
  const { data } = await api.get("/weather", { params });
  return data;
};

export const fetchEvents = async (city = null) => {
  const params = city && city !== "Oregon" ? { city } : {};
  const { data } = await api.get("/events", { params });
  return data;
};

export const fetchAlerts = async () => {
  const { data } = await api.get("/alerts");
  return data;
};

export const fetchWildfires = async () => {
  const { data } = await api.get("/wildfires");
  return data;
};