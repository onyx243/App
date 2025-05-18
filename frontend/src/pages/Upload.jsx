import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useParams } from 'react-router-dom';
import { useApi } from '../utils/api.js';
import toast from 'react-hot-toast';

export default function Upload() {
  const { slug } = useParams();
  const [files, setFiles] = useState([]);
  const [progress, setProgress] = useState(0);
  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'image/*': [],
      'application/pdf': [],
    },
    onDrop: (accepted) => setFiles(accepted),
  });
  const api = useApi();

  const submit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    files.forEach((f) => formData.append('files', f));
    await api.post(`/upload/${slug}`, formData, {
      onUploadProgress: (e) => setProgress(Math.round((e.loaded * 100) / e.total)),
    });
    toast.success('Uploaded!');
    setProgress(0);
  };

  return (
    <form onSubmit={submit} className="max-w-md mx-auto bg-white p-4 shadow">
      <h1 className="text-xl mb-2">Upload Files</h1>
      <div {...getRootProps()} className="border-2 border-dashed p-4 mb-2 text-center cursor-pointer">
        <input {...getInputProps()} />
        {files.length > 0 ? files.map((f) => <p key={f.name}>{f.name}</p>) : 'Drag files here'}
      </div>
      {progress > 0 && <div className="w-full bg-gray-200 h-2 mb-2"><div className="bg-blue-500 h-full" style={{ width: `${progress}%` }} /></div>}
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 w-full">Upload</button>
    </form>
  );
}
