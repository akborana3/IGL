/** Axios instance with retry, timeout, and interceptors. */

import axios, { AxiosError, AxiosInstance } from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:7860";

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor with retry
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const config = error.config as any;
    if (!config) return Promise.reject(error);

    config.__retryCount = config.__retryCount || 0;

    // Retry on network errors and 5xx, up to 3 times
    const shouldRetry =
      config.__retryCount < 3 &&
      (!error.response || (error.response.status >= 500 && error.response.status < 600));

    if (shouldRetry) {
      config.__retryCount++;
      const delay = Math.min(1000 * config.__retryCount, 3000);
      await new Promise((resolve) => setTimeout(resolve, delay));
      return api(config);
    }

    return Promise.reject(error);
  }
);

export default api;
