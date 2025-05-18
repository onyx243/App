import { useEffect, useState } from 'react';
import { useApi } from '../utils/api.js';
import { useAuth } from '../utils/auth.jsx';
import { io } from 'socket.io-client';
import toast from 'react-hot-toast';
import InfiniteScroll from 'react-infinite-scroll-component';

export default function Dashboard() {
  const [uploads, setUploads] = useState([]);
  const [visible, setVisible] = useState(10);
  const api = useApi();
  const { user, token } = useAuth();
  const [query, setQuery] = useState('');

  const fetchUploads = async () => {
    const { data } = await api.get('/dashboard');
    setUploads(data.uploads);
  };

  useEffect(() => {
    if (!token) return;
    fetchUploads();
    const socket = io(import.meta.env.VITE_WS_URL || window.location.origin, { query: { userId: user.id } });
    socket.on('new-upload', fetchUploads);
    return () => socket.disconnect();
  }, [token]);

  if (!token) return <p className="text-center">Login first</p>;

  const filtered = uploads.filter((u) => u.user.email.includes(query));

  const loadMore = () => setVisible((v) => v + 10);

  return (
    <div>
      <h1 className="text-xl mb-2">Dashboard</h1>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search email" className="border p-1 mb-2" />
      <InfiniteScroll
        dataLength={Math.min(visible, filtered.length)}
        next={loadMore}
        hasMore={visible < filtered.length}
        loader={<p>Loading...</p>}
      >
        <table className="min-w-full bg-white">
          <thead>
            <tr><th className="p-2">User</th><th className="p-2">Files</th><th className="p-2">Actions</th></tr>
          </thead>
          <tbody>
            {filtered.slice(0, visible).map((u) => (
              <tr key={u.id} className="border-t">
                <td className="p-2">{u.user.email}</td>
                <td className="p-2 space-x-1">
                  {u.files.map((f) => (
                    f.endsWith('.pdf')
                      ? <a href={f.startsWith('http') ? f : `/api/download/${encodeURIComponent(f.replace('/uploads/', ''))}`} key={f} className="text-blue-500" target="_blank" rel="noopener noreferrer">PDF</a>
                      : <img src={f.startsWith('http') ? f : `/api/download/${encodeURIComponent(f.replace('/uploads/', ''))}`} alt="thumb" className="inline w-12 h-12 object-cover" key={f} />
                  ))}
                </td>
                <td className="p-2">
                  <button
                    type="button"
                    onClick={() => api.patch(`/dashboard/${u.id}/printed`).then(() => { toast.success('Marked printed'); fetchUploads(); })}
                    className="text-green-600 mr-2"
                  >Printed</button>
                  <button
                    type="button"
                    onClick={() => api.delete(`/dashboard/${u.id}`).then(() => { toast.success('Deleted'); fetchUploads(); })}
                    className="text-red-600"
                  >Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </InfiniteScroll>
    </div>
  );
}
