import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Notification, SyncStatus, Theme } from '../types';

interface AppState {
  theme: Theme;
  notifications: Notification[];
  syncStatus: SyncStatus;
  isOnline: boolean;
  sidebarOpen: boolean;
  currentGroup: number | null;
}

interface AppActions {
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  markNotificationRead: (id: string) => void;
  clearNotifications: () => void;
  setSyncStatus: (status: Partial<SyncStatus>) => void;
  setOnline: (online: boolean) => void;
  setSidebarOpen: (open: boolean) => void;
  setCurrentGroup: (groupId: number | null) => void;
}

export const useAppStore = create<AppState & AppActions>()(
  persist(
    (set, get) => ({
      theme: { mode: 'light' },
      notifications: [],
      syncStatus: {
        isOnline: true,
        lastSync: Date.now(),
        pendingChanges: 0,
      },
      isOnline: true,
      sidebarOpen: true,
      currentGroup: null,

      setTheme: (theme) => {
        set({ theme });
        document.documentElement.classList.toggle('dark', theme.mode === 'dark');
      },

      toggleTheme: () => {
        const { theme } = get();
        const newTheme: Theme = { mode: theme.mode === 'light' ? 'dark' : 'light' };
        set({ theme: newTheme });
        document.documentElement.classList.toggle('dark', newTheme.mode === 'dark');
      },

      addNotification: (notification) => {
        const id = Math.random().toString(36).substr(2, 9);
        const newNotification: Notification = {
          ...notification,
          id,
          timestamp: Date.now(),
        };
        set((state) => ({
          notifications: [...state.notifications, newNotification],
        }));
      },

      removeNotification: (id) => {
        set((state) => ({
          notifications: state.notifications.filter((n) => n.id !== id),
        }));
      },

      markNotificationRead: (id) => {
        set((state) => ({
          notifications: state.notifications.map((n) =>
            n.id === id ? { ...n, read: true } : n
          ),
        }));
      },

      clearNotifications: () => {
        set({ notifications: [] });
      },

      setSyncStatus: (status) => {
        set((state) => ({
          syncStatus: { ...state.syncStatus, ...status },
        }));
      },

      setOnline: (online) => {
        set({ isOnline: online });
        if (online) {
          get().setSyncStatus({ isOnline: true, lastSync: Date.now() });
        }
      },

      setSidebarOpen: (open) => {
        set({ sidebarOpen: open });
      },

      setCurrentGroup: (groupId) => {
        set({ currentGroup: groupId });
      },
    }),
    {
      name: 'app-storage',
      partialize: (state) => ({ 
        theme: state.theme,
        sidebarOpen: state.sidebarOpen,
        currentGroup: state.currentGroup,
      }),
    }
  )
);