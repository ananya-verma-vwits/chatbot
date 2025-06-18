import React, { useState } from 'react';
import { Loader, Modal } from './common';

function FileUpload({ onUpload }) {
  const [uploading, setUploading] = useState(false);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      alert('File uploaded successfully!');
      onUpload(); // Refresh file list
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  return (
    <>
      <div className="bg-white dark:bg-dark-200 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-2xl p-6 text-center transition-all hover:border-blue-500 dark:hover:border-blue-400 mb-4">
        <h3 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">Upload Documents</h3>
        <input
          type="file"
          accept=".pdf,.txt,.doc,.docx"
          onChange={handleFileUpload}
          className="hidden"
          id="file-upload"
          disabled={uploading}
        />
        <label htmlFor="file-upload">
          <span className={`px-6 py-2.5 bg-blue-500 text-white font-medium rounded-lg cursor-pointer inline-block transition-all hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 ${
            uploading ? 'opacity-50 cursor-not-allowed' : ''
          }`}>
            Choose File
          </span>
        </label>
      </div>

      <Modal isOpen={uploading}>
        <h3 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Uploading Document</h3>
        <Loader />
        <p className="text-gray-600 dark:text-gray-300">Please wait while we process your file...</p>
      </Modal>
    </>
  );
}

export default FileUpload;