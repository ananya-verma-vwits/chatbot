import React, { useState, useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import FileUpload from './components/FileUpload';
import { BiMessageDetail, BiSearch, BiTrash } from 'react-icons/bi';
import { MdDarkMode, MdLightMode } from 'react-icons/md';
import { ThemeProvider } from 'styled-components';
import { lightTheme, darkTheme } from './theme';
import { GlobalStyles } from './GlobalStyles';

const API_URL = 'http://localhost:8000';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [messages, setMessages] = useState([]);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  const handleNewMessage = (message, isClear = false) => {
    if (isClear) {
      setMessages([]);
      localStorage.removeItem('chatHistory');
    } else if (message) {
      const timestamp = new Date().toISOString();
      const messageWithMeta = {
        ...message,
        id: `msg_${timestamp}`,
        timestamp,
      };
      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages, messageWithMeta];
        localStorage.setItem('chatHistory', JSON.stringify(updatedMessages));
        return updatedMessages;
      });
    }
  };

  const fetchUploadedFiles = async () => {
    setIsLoading(true);
    try {
      // First try to get list of files from upload endpoint
      const response = await fetch(`${API_URL}/upload/status`);
      const data = await response.json();
      
      if (data.files && data.files.length > 0) {
        // If we have file names, show them
        setUploadedFiles(data.files);
      } else {
        // Fall back to checking FAISS status
        const faissResponse = await fetch(`${API_URL}/chat/status`);
        const faissData = await faissResponse.json();
        
        if (faissData.status === 'initialized') {
          setUploadedFiles([`${faissData.document_count} documents processed`]);
        } else {
          setUploadedFiles(['No documents uploaded']);
        }
      }
    } catch (error) {
      console.error('Error fetching files:', error);
      setUploadedFiles(['Error checking document status']);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteFile = async (filename) => {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) {
      return;
    }
    
    try {
      const response = await fetch(`${API_URL}/upload/${filename}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Delete failed');
      }
      
      // Refresh the file list
      fetchUploadedFiles();
      
      // Show success message
      alert(`File ${filename} deleted successfully`);
    } catch (error) {
      console.error('Error deleting file:', error);
      alert(`Failed to delete file: ${error.message}`);
    }
  };

  useEffect(() => {
    const savedMessages = localStorage.getItem('chatHistory');
    if (savedMessages) {
      setMessages(JSON.parse(savedMessages));
    }
    fetchUploadedFiles();
  }, []);

  return (
    <ThemeProvider theme={isDarkMode ? darkTheme : lightTheme}>
      <GlobalStyles />
      <div className={`h-screen flex ${isDarkMode ? 'dark' : ''}`}>
        {/* Sidebar */}
        <div className="w-64 bg-light-100 dark:bg-dark-300 border-r border-light-300 dark:border-dark-100">
          <div className="flex items-center px-4 py-3 border-b border-light-300 dark:border-dark-100">
            <h1 className="text-xl font-semibold dark:text-white">AVA Chatbot</h1>
            <button className="ml-auto" onClick={toggleTheme}>
              {isDarkMode ? <MdLightMode className="w-5 h-5 text-white" /> : <MdDarkMode className="w-5 h-5" />}
            </button>
          </div>

          {/* Sidebar Menu */}
          <nav className="p-4">
            <button className="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:bg-light-200 dark:hover:bg-dark-200 p-2 rounded-lg w-full">
              <BiMessageDetail className="w-5 h-5" />
              <span>Chats</span>
            </button>
            <button className="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:bg-light-200 dark:hover:bg-dark-200 p-2 rounded-lg w-full mt-2">
              <BiSearch className="w-5 h-5" />
              <span>Search</span>
            </button>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col bg-light-200 dark:bg-dark-200 overflow-hidden">
          <main className="flex-1 overflow-auto">
            <div className="max-w-4xl mx-auto p-6 h-full">
              <h1 className="text-3xl font-bold mb-4 dark:text-white">AVA Chatbot</h1>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Chat with your documents using vector search technology
              </p>

              <div className="space-y-4 h-[calc(100vh-240px)] flex flex-col">
                <FileUpload onUpload={fetchUploadedFiles} />
                <div>
                  <h2 className="text-lg font-semibold mb-2 dark:text-white">Uploaded Files</h2>
                  {isLoading ? (
                    <p className="text-gray-600 dark:text-gray-300">Checking document status...</p>
                  ) : (
                    <ul className="list-disc pl-5 text-gray-800 dark:text-gray-300">
                      {uploadedFiles.map((file, index) => (
                        <li key={index} className="flex items-center justify-between py-1">
                          <span>{file}</span>
                          <button 
                            onClick={() => deleteFile(file)}
                            className="text-red-500 hover:text-red-700 transition-colors"
                            title="Delete file"
                          >
                            <BiTrash className="w-5 h-5" />
                          </button>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
                <ChatWindow messages={messages} onNewMessage={handleNewMessage} />
                <button
                  className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                  onClick={() => handleNewMessage(null, true)}
                >
                  Clear Chat History
                </button>
              </div>
            </div>
          </main>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;