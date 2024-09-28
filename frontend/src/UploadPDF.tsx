import React, { useState } from 'react';
import axios from 'axios';
import DisplayData from './DisplayData'; // Import DisplayData component

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
  
      const responseData = response.data;
  
      // Parse nouns and verbs as arrays from the string
      const nouns = JSON.parse(responseData.nouns.replace(/'/g, '"')); // Replace single quotes with double quotes before parsing
      const verbs = JSON.parse(responseData.verbs.replace(/'/g, '"'));
  
      setData({ nouns, verbs });
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };
  

  return (
    <div className="flex flex-col items-center">
      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
          className="p-2 border border-gray-300"
        />
        <p className="text-sm text-gray-600">Email Address can only be used once with one PDF.</p>
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          required
          className="p-2 border border-gray-300"
        />
        <button type="submit" className="bg-blue-500 text-white p-2 mt-2">
          Upload PDF
        </button>
      </form>

      {/* Use DisplayData component to show extracted nouns and verbs */}
      <DisplayData data={data} />
    </div>
  );
};

export default UploadPDF;
