import React, { useState, useRef, useEffect } from 'react';
import LoadingDots from './common/LoadingDots';



function ChatWindow({ messages, onNewMessage }) {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const messageContainerRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
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
      timestamp: new Date()
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
        timestamp: new Date()
      };
      onNewMessage(botMessage);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { text: error.message || 'Sorry, there was an error processing your request.', isUser: false };
      onNewMessage(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-white dark:bg-dark-200 rounded-2xl shadow-lg overflow-hidden min-h-[calc(100vh-240px)]">
      <div className="flex-grow p-6 overflow-y-auto scroll-smooth max-h-[60vh] space-y-4 scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-dark-100" ref={messageContainerRef}>
        {messages.map((message, index) => (
          <div key={index} className={`flex items-start space-x-3 ${message.isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
            <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white relative ${message.isUser ? 'bg-blue-500' : 'bg-gray-500 dark:bg-gray-600'}`}>
              {message.isUser ? '👤' : '🤖'}
            </div>
            <div className={`flex flex-col ${message.isUser ? 'items-end' : 'items-start'}`}>
              <div className={`px-4 py-2 rounded-2xl max-w-md shadow-sm ${
                message.isUser 
                ? 'bg-blue-500 text-white rounded-br-sm' 
                : 'bg-gray-100 dark:bg-dark-100 text-gray-800 dark:text-gray-200 rounded-bl-sm'
              }`}>
                {message.text}
              </div>
              <span className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 rounded-full bg-gray-500 dark:bg-gray-600 flex items-center justify-center text-white">
              🤖
            </div>
            <div className="bg-gray-100 dark:bg-dark-100 px-4 py-2 rounded-2xl rounded-bl-sm">
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
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-dark-100 dark:text-white"
            onKeyPress={(e) => e.key === 'Enter' && handleSubmit(e)}
            disabled={isLoading}
          />
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className={`px-6 py-2 bg-blue-500 text-white font-semibold rounded-lg transition-transform hover:translate-y-[-1px] ${
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