import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export const fetchHeadlines = async () => {
  const { data } = await api.get("/headlines");
  return data;
};

export const fetchWeather = async () => {
  const { data } = await api.get("/weather");
  return data;
};

export const fetchEvents = async () => {
  const { data } = await api.get("/events");
  return data;
};