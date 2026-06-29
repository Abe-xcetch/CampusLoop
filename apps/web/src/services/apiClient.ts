import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Configure interceptors to automatically inject Firebase ID Token
 * before dispatching requests to Django REST Framework
 */
apiClient.interceptors.request.use(
  async (config) => {
    // In a real application, fetch the token from Firebase Authentication sdk
    // e.g., const token = await firebase.auth().currentUser?.getIdToken();
    const token = typeof window !== "undefined" ? localStorage.getItem("firebase_id_token") : null;
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
