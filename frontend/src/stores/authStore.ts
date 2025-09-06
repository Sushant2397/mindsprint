import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, AuthTokens } from '../types';
import { apiService } from '../services/api';

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  login: (username: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => void;
  getProfile: () => Promise<void>;
  clearError: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (username: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const { user, tokens } = await apiService.login({ username, password });
          set({ user, tokens, isAuthenticated: true, isLoading: false });
        } catch (error: any) {
          set({ 
            error: error.response?.data?.error || 'Login failed', 
            isLoading: false 
          });
          throw error;
        }
      },

      register: async (userData: any) => {
        set({ isLoading: true, error: null });
        try {
          const { user, tokens } = await apiService.register(userData);
          set({ user, tokens, isAuthenticated: true, isLoading: false });
        } catch (error: any) {
          set({ 
            error: error.response?.data?.error || 'Registration failed', 
            isLoading: false 
          });
          throw error;
        }
      },

      logout: () => {
        apiService.logout();
        set({ 
          user: null, 
          tokens: null, 
          isAuthenticated: false, 
          error: null 
        });
      },

      getProfile: async () => {
        set({ isLoading: true, error: null });
        try {
          const user = await apiService.getProfile();
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error: any) {
          set({ 
            error: error.response?.data?.error || 'Failed to get profile', 
            isLoading: false 
          });
          throw error;
        }
      },

      clearError: () => set({ error: null }),
      setLoading: (loading: boolean) => set({ isLoading: loading }),

      // Check if user is actually authenticated by verifying tokens
      checkAuth: () => {
        const { tokens, user } = get();
        if (tokens && user) {
          // Verify token is not expired (basic check)
          try {
            const tokenData = JSON.parse(atob(tokens.access.split('.')[1]));
            const isExpired = tokenData.exp * 1000 < Date.now();
            if (isExpired) {
              set({ user: null, tokens: null, isAuthenticated: false });
              return false;
            }
            return true;
          } catch {
            set({ user: null, tokens: null, isAuthenticated: false });
            return false;
          }
        }
        return false;
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        user: state.user, 
        tokens: state.tokens, 
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
);