"use client";
import React, { useEffect, useState } from "react";
import { getFirebaseAuth } from "./firebase";
import { onAuthStateChanged, signOut as firebaseSignOut } from "firebase/auth";
import { apiClient } from "../services/apiClient";

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  useEffect(() => {
    try {
      const auth = getFirebaseAuth();
      const unsub = onAuthStateChanged(auth, async (user) => {
        if (user) {
          const token = await user.getIdToken();
          localStorage.setItem("firebase_id_token", token);
          localStorage.setItem("campusloop_authed", "1");
          setIsAuthenticated(true);
        } else {
          localStorage.removeItem("firebase_id_token");
          localStorage.removeItem("campusloop_authed");
          setIsAuthenticated(false);
        }
      });
      return () => unsub();
    } catch (err) {
      // Firebase not configured - fallback to localStorage
      const ok = typeof window !== "undefined" && !!localStorage.getItem("campusloop_authed");
      setIsAuthenticated(ok);
    }
  }, []);

  return {
    isAuthenticated,
    async signOut() {
      try {
        // call backend logout endpoint
        await apiClient.post('/auth/logout/');
      } catch (e) {
        // ignore errors
      }
      try {
        const auth = getFirebaseAuth();
        await firebaseSignOut(auth);
      } catch (e) {
        // ignore
      }
      localStorage.removeItem('firebase_id_token');
      localStorage.removeItem('campusloop_authed');
      setIsAuthenticated(false);
    }
  };
}
