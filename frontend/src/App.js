import React, { useState, useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import FileUpload from './components/FileUpload';
import { BiMessageDetail, BiSearch } from 'react-icons/bi';
import { MdDarkMode, MdLightMode } from 'react-icons/md';

const API_URL = 'http://127.0.0.1:8000'; // Update if necessary

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [messages, setMessages] = useState([]);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  const handleNewMessage = (message, isClear = false) => {
    if (isClear) {
      setMessages([]);
      localStorage.removeItem('chatHistory');
    } else {
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
    try {
      const response = await fetch(`${API_URL}/files`);
      const data = await response.json();
      setUploadedFiles(data.files || []);
    } catch (error) {
      console.error('Error fetching files:', error);
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
    <div className={`h-screen flex ${isDarkMode ? 'dark' : ''}`}>
      {/* Sidebar */}
      <div className="w-64 bg-light-100 dark:bg-dark-300 border-r border-light-300 dark:border-dark-100">
        <div className="flex items-center px-4 py-3 border-b border-light-300 dark:border-dark-100">
          <h1 className="text-xl font-semibold dark:text-white">ChatBot</h1>
          <button className="ml-auto" onClick={toggleTheme}>
            {isDarkMode ? <MdLightMode className="w-5 h-5" /> : <MdDarkMode className="w-5 h-5" />}
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
            <h1 className="text-3xl font-bold mb-4 dark:text-white">ChatBot</h1>
            <p className="text-gray-600 dark:text-gray-400 mb-4">Chat with the smartest AI - Experience the power of AI with us</p>

            <div className="space-y-4 h-[calc(100vh-240px)] flex flex-col">
              <FileUpload onUpload={fetchUploadedFiles} />
              <div>
                <h2 className="text-lg font-semibold mb-2 dark:text-white">Uploaded Files</h2>
                <ul className="list-disc pl-5 text-gray-800 dark:text-gray-300">
                  {uploadedFiles.map((file, index) => (
                    <li key={index}>{file}</li>
                  ))}
                </ul>
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
  );
}

export default App;