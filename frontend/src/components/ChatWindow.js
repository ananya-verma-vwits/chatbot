import React, { useState, useRef, useEffect } from 'react';
import { FaRobot } from 'react-icons/fa'; // AI icon
import LoadingDots from './common/LoadingDots';

function ChatWindow({ messages, onNewMessage }) {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const currentInput = input;
    setInput('');
    setIsLoading(true);

    const userMessage = {
      text: currentInput,
      isUser: true,
      timestamp: new Date(),
    };
    onNewMessage(userMessage);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: currentInput }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Error: ${response.status}`);
      }

      const data = await response.json();
      const botMessage = {
        text: data.response,
        isUser: false,
        timestamp: new Date(),
      };
      onNewMessage(botMessage);
    } catch (error) {
      const errorMessage = {
        text: error.message || 'Sorry, there was an error processing your request.',
        isUser: false,
        timestamp: new Date(),
        isError: true,
      };
      onNewMessage(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const renderMessageContent = (message) => {
    if (message.isError) {
      return <span className="text-red-500">{message.text}</span>;
    }

    // Check if the message contains structured data (e.g., bullet points or bold text)
    const lines = message.text.split('\n');
    return (
      <div>
        {lines.map((line, index) => {
          if (line.startsWith('**')) {
            // Render bold text
            return (
              <p key={index} className="font-bold">
                {line.replace('**', '').trim()}
              </p>
            );
          } else if (line.startsWith('*')) {
            // Render bullet points
            return (
              <li key={index} className="list-disc pl-5">
                {line.replace('*', '').trim()}
              </li>
            );
          }
          return <p key={index}>{line}</p>;
        })}
      </div>
    );
  };

  return (
    <div className="flex-1 flex flex-col bg-white dark:bg-dark-200 rounded-2xl shadow-lg overflow-hidden min-h-[calc(100vh-400px)]">
      <div className="flex-grow p-6 overflow-y-auto scroll-smooth max-h-[60vh] space-y-4 scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-dark-100">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500 dark:text-gray-400 text-center">
              Upload a document and ask questions about its content!
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex items-start space-x-3 ${
              message.isUser ? 'flex-row-reverse space-x-reverse' : ''
            }`}
          >
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center text-white ${
                message.isUser
                  ? 'bg-blue-500'
                  : message.isError
                  ? 'bg-red-500'
                  : 'bg-purple-600 dark:bg-purple-700'
              }`}
            >
              {message.isUser ? '👤' : <FaRobot className="w-5 h-5" />}
            </div>
            <div className={`flex flex-col ${message.isUser ? 'items-end' : 'items-start'}`}>
              <div
                className={`px-4 py-2 rounded-2xl max-w-md shadow-sm ${
                  message.isUser
                    ? 'bg-blue-500 text-white rounded-br-sm'
                    : message.isError
                    ? 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-bl-sm'
                    : 'bg-gray-100 dark:bg-dark-100 text-gray-800 dark:text-gray-200 rounded-bl-sm'
                }`}
              >
                {renderMessageContent(message)}
              </div>
              <span className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                {new Date(message.timestamp).toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </span>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 rounded-full bg-purple-600 dark:bg-purple-700 flex items-center justify-center text-white">
              <FaRobot className="w-5 h-5" />
            </div>
            <div className="bg-gray-100 dark:bg-dark-100 px-4 py-3 rounded-2xl rounded-bl-sm">
              <LoadingDots />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="border-t border-gray-200 dark:border-dark-100 p-4 bg-white dark:bg-dark-200">
        <div className="flex space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your documents..."
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-dark-100 dark:text-white"
            onKeyPress={(e) => e.key === 'Enter' && handleSubmit(e)}
            disabled={isLoading}
          />
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className={`px-6 py-2 bg-blue-500 text-white font-semibold rounded-lg transition-colors ${
              isLoading ? 'opacity-70 cursor-not-allowed' : 'hover:bg-blue-600'
            }`}
          >
            {isLoading ? <LoadingDots /> : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;