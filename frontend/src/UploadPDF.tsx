import React, { useState } from 'react';
import axios from 'axios';

const UploadPDF: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [email, setEmail] = useState('');
  const [data, setData] = useState<{ nouns: string[]; verbs: string[] } | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file || !email) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('email', email);

    try {
      const response = await axios.post(`${import.meta.env.VITE_BASE_URL}/api/v1/upload/`, formData);
      setData(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <form onSubmit={handleSubmit} className="flex flex-col">
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
        <input type="file" accept="application/pdf" onChange={handleFileChange} required />
        <button type="submit" className="bg-blue-500 text-white p-2 mt-2">Upload PDF</button>
      </form>

      {data && (
        <div className="mt-4">
          <h2>Extracted Data:</h2>
          <p><strong>Nouns:</strong> {data.nouns.join(', ')}</p>
          <p><strong>Verbs:</strong> {data.verbs.join(', ')}</p>
        </div>
      )}
    </div>
  );
};

export default UploadPDF;
