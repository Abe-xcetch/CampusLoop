import { create } from "zustand";
import { User } from "@campusloop/shared";

interface AuthState {
  user: User | null;
  idToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: User | null, idToken: string | null) => void;
  setLoading: (isLoading: boolean) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  idToken: null,
  isAuthenticated: false,
  isLoading: true,
  setUser: (user, idToken) =>
    set({
      user,
      idToken,
      isAuthenticated: !!user,
      isLoading: false,
    }),
  setLoading: (isLoading) => set({ isLoading }),
  logout: () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("firebase_id_token");
    }
    set({ user: null, idToken: null, isAuthenticated: false, isLoading: false });
  },
}));
