import { Routes, Route, Link, Navigate } from 'react-router-dom';
import Login from './Login.jsx';
import Signup from './Signup.jsx';
import Upload from './Upload.jsx';
import Dashboard from './Dashboard.jsx';
import { useAuth } from '../utils/auth.jsx';
import RequireRole from '../utils/RequireRole.jsx';
import { useEffect, useState } from 'react';

export default function App() {
  const { token, logout } = useAuth();
  const [dark, setDark] = useState(localStorage.getItem('dark') === 'true');
  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
    localStorage.setItem('dark', dark);
  }, [dark]);
  return (
    <div className="container mx-auto p-4">
      <nav className="flex justify-between mb-4">
        <Link to="/">Home</Link>
        <div className="space-x-2">
          <button type="button" onClick={() => setDark(!dark)} className="text-sm underline">
            {dark ? 'Light' : 'Dark'}
          </button>
          {token && (
            <button type="button" onClick={logout} className="text-blue-500">Logout</button>
          )}
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/upload/:slug" element={<Upload />} />
        <Route
          path="/dashboard"
          element={(
            <RequireRole roles={['shopOwner']}>
              <Dashboard />
            </RequireRole>
          )}
        />
      </Routes>
    </div>
  );
}
