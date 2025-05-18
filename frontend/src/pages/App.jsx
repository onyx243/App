import { Routes, Route, Link, Navigate } from 'react-router-dom';
import Login from './Login.jsx';
import Signup from './Signup.jsx';
import Upload from './Upload.jsx';
import Dashboard from './Dashboard.jsx';
import { useAuth } from '../utils/auth.jsx';

export default function App() {
  const { token, logout } = useAuth();
  return (
    <div className="container mx-auto p-4">
      <nav className="flex justify-between mb-4">
        <Link to="/">Home</Link>
        {token && (
          <button type="button" onClick={logout} className="text-blue-500">Logout</button>
        )}
      </nav>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/upload/:slug" element={<Upload />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  );
}
