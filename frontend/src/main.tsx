import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// Initialize theme on app start
const theme = localStorage.getItem('app-storage');
if (theme) {
  const parsed = JSON.parse(theme);
  if (parsed?.state?.theme?.mode === 'dark') {
    document.documentElement.classList.add('dark');
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)