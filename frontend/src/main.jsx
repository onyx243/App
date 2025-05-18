import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './pages/App.jsx';
import './index.css';
import { AuthProvider } from './utils/auth.jsx';
import { Toaster } from 'react-hot-toast';

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <AuthProvider>
      <App />
      <Toaster position="top-right" />
    </AuthProvider>
  </BrowserRouter>,
);
