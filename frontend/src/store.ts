// ReviewGuard AI — Zustand Auth Store

import { create } from 'zustand'
import type { UserRole } from './api'

interface AuthUser {
  id: string
  email: string
  full_name: string
  role: UserRole
}

interface AuthState {
  token: string | null
  user: AuthUser | null
  isAuthenticated: boolean
  login: (token: string, user: AuthUser) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('rg_token'),
  user: (() => {
    try { return JSON.parse(localStorage.getItem('rg_user') || 'null') }
    catch { return null }
  })(),
  isAuthenticated: !!localStorage.getItem('rg_token'),

  login: (token, user) => {
    localStorage.setItem('rg_token', token)
    localStorage.setItem('rg_user', JSON.stringify(user))
    set({ token, user, isAuthenticated: true })
  },

  logout: () => {
    localStorage.removeItem('rg_token')
    localStorage.removeItem('rg_user')
    set({ token: null, user: null, isAuthenticated: false })
  },
}))
