import { useEffect, useState } from 'react';
import { useApi } from '../utils/api.js';
import { useAuth } from '../utils/auth.jsx';
import { io } from 'socket.io-client';

export default function Dashboard() {
  const [uploads, setUploads] = useState([]);
  const api = useApi();
  const { user, token } = useAuth();

  const fetchUploads = async () => {
    const { data } = await api.get('/dashboard');
    setUploads(data.uploads);
  };

  useEffect(() => {
    if (!token) return;
    fetchUploads();
    const socket = io(import.meta.env.VITE_API_URL.replace('/api', ''), { query: { userId: user.id } });
    socket.on('new-upload', fetchUploads);
    return () => socket.disconnect();
  }, [token]);

  if (!token) return <p className="text-center">Login first</p>;

  return (
    <div>
      <h1 className="text-xl mb-2">Dashboard</h1>
      <table className="min-w-full bg-white">
        <thead>
          <tr><th className="p-2">User</th><th className="p-2">Files</th><th className="p-2">Actions</th></tr>
        </thead>
        <tbody>
          {uploads.map((u) => (
            <tr key={u._id} className="border-t">
              <td className="p-2">{u.user.email}</td>
              <td className="p-2">
                {u.files.map((f) => <a href={`/${f}`} key={f} className="block text-blue-500" target="_blank" rel="noopener noreferrer">{f}</a>)}
              </td>
              <td className="p-2">
                <button type="button" onClick={() => api.patch(`/dashboard/${u._id}/printed`).then(fetchUploads)} className="text-green-600 mr-2">Printed</button>
                <button type="button" onClick={() => api.delete(`/dashboard/${u._id}`).then(fetchUploads)} className="text-red-600">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
