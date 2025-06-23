import React, { useState } from 'react';
import { Loader, Modal } from './common';

function FileUpload({ onUpload }) {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setUploadProgress(0);
    
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const data = await response.json();
      console.log('Upload response:', data);
      
      alert('File uploaded and processed with FAISS successfully!');
      onUpload(); // Refresh file list
    } catch (error) {
      console.error('Error:', error);
      alert(`Failed to upload file: ${error.message}`);
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
          accept=".pdf"
          onChange={handleFileUpload}
          className="hidden"
          id="file-upload"
          disabled={uploading}
        />
        <label htmlFor="file-upload">
          <span className={`px-6 py-2.5 bg-blue-500 text-white font-medium rounded-lg cursor-pointer inline-block transition-all hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 ${
            uploading ? 'opacity-50 cursor-not-allowed' : ''
          }`}>
            Choose PDF File
          </span>
        </label>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Upload a PDF document to enable AI-powered question answering
        </p>
      </div>

      <Modal isOpen={uploading}>
        <h3 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Processing Document</h3>
        <p className="text-gray-600 dark:text-gray-300 mb-4">
          Please wait while we extract information and build search vectors...
        </p>
        <Loader />
      </Modal>
    </>
  );
}

export default FileUpload;