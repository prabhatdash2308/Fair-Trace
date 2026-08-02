import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { AppProvider } from './app/providers/AppProvider';
import { GlobalErrorBoundary } from './components/error';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <GlobalErrorBoundary>
      <AppProvider>
        <App />
      </AppProvider>
    </GlobalErrorBoundary>
  </React.StrictMode>
);