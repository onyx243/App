import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useApi } from '../utils/api.js';

export default function Upload() {
  const { slug } = useParams();
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState('');
  const api = useApi();

  const submit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    files.forEach((f) => formData.append('files', f));
    await api.post(`/upload/${slug}`, formData);
    setMessage('Uploaded!');
    setTimeout(() => setMessage(''), 3000);
  };

  return (
    <form onSubmit={submit} className="max-w-md mx-auto bg-white p-4 shadow">
      <h1 className="text-xl mb-2">Upload Files</h1>
      <input type="file" multiple onChange={(e) => setFiles(Array.from(e.target.files))} className="mb-2" />
      {message && <p className="text-green-600 mb-2">{message}</p>}
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 w-full">Upload</button>
    </form>
  );
}
