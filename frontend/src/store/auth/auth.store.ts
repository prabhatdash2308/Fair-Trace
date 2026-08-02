import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { User, UserRole } from '@/types';
import { DEMO_MODE, DEMO_USER, DEMO_TOKEN } from '@/config/demo';

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

// ── Demo Mode: pre-hydrate the store so guards never bounce ──────────────────
const demoInitial = DEMO_MODE
  ? {
      token: DEMO_TOKEN,
      refreshToken: null,
      expiresAt: null,
      user: DEMO_USER as AuthUser,
      isAuthenticated: true,
      isLoading: false,
    }
  : {
      token: null,
      refreshToken: null,
      expiresAt: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
    };

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      ...demoInitial,

      login: (token, user) =>
        set({ token, user, isAuthenticated: true }),

      logout: () =>
        // In demo mode, logout re-seeds the demo user instead of clearing
        DEMO_MODE
          ? set({ token: DEMO_TOKEN, user: DEMO_USER as AuthUser, isAuthenticated: true })
          : set({
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
      partialize: (state) => ({
        token: state.token,
        refreshToken: state.refreshToken,
        expiresAt: state.expiresAt,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
      // In demo mode, skip reading stale localStorage so demo user is always active
      merge: (persisted, current) => {
        if (DEMO_MODE) return current;
        return { ...current, ...(persisted as Partial<AuthState>) };
      },
    }
  )
);
