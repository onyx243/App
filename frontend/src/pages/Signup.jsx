import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../utils/auth.jsx';
import { useApi } from '../utils/api.js';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { setToken, setUser } = useAuth();
  const api = useApi();
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    const { data } = await api.post('/auth/signup', { email, password });
    setToken(data.token);
    setUser(data.user);
    navigate('/dashboard');
  };

  return (
    <form onSubmit={submit} className="max-w-sm mx-auto bg-white p-4 shadow">
      <h1 className="text-xl mb-2">Sign Up</h1>
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="border p-2 w-full mb-2" />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" className="border p-2 w-full mb-2" />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 w-full">Sign Up</button>
      <p className="mt-2 text-center text-sm">
        <Link to="/login" className="text-blue-500">Login</Link>
      </p>
    </form>
  );
}
