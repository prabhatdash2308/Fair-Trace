import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { User, UserRole } from '@/types';

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
}

interface AuthState {
  // Tokens
  token: string | null;
  refreshToken: string | null;
  expiresAt: number | null;

  // User
  user: AuthUser | null;

  // Status
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  login: (token: string, user: AuthUser) => void;
  logout: () => void;
  setUser: (user: Partial<User>) => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      expiresAt: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,

      login: (token, user) =>
        set({ token, user, isAuthenticated: true }),

      logout: () =>
        set({
          token: null,
          refreshToken: null,
          expiresAt: null,
          user: null,
          isAuthenticated: false,
        }),

      setUser: (userUpdate) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...userUpdate } : null,
        })),

      setLoading: (isLoading) => set({ isLoading }),
    }),
    {
      name: 'rg_auth',
      storage: createJSONStorage(() => localStorage),
      // Persist only what is needed to restore the session
      partialize: (state) => ({
        token: state.token,
        refreshToken: state.refreshToken,
        expiresAt: state.expiresAt,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
