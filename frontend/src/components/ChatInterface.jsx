// frontend/src/components/ChatInterface.jsx
import { useState, useRef, useEffect } from 'react';
import ApiService from '../services/api';
import MessageList from './MessageList'; // Import the MessageList component

const ChatInterface = ({ userId }) => {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([
    { id: 1, sender: 'ai', content: "Hello! I'm your AI assistant. How can I help you manage your tasks today?", timestamp: new Date() }
  ]);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e?.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await ApiService.sendMessage(userId, userMessage.content, conversationId);

      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      const aiMessage = {
        id: Date.now() + 1,
        sender: 'ai',
        content: response.response,
        toolCalls: response.tool_calls,
        taskUpdates: response.task_updates,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        sender: 'ai',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 dark:bg-gray-800 rounded-xl shadow-lg p-4">
      <div className="flex-grow overflow-y-auto mb-4">
        <MessageList messages={messages} />
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white dark:bg-gray-700 px-4 py-2 rounded-xl animate-pulse">
              AI is typing...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="mt-auto">
        <div className="flex gap-0">
          <textarea
            rows={1}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message here..."
            className="flex-grow px-4 py-2 border border-gray-300 rounded-l-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            disabled={isLoading}
          />
          <button
            type="submit"
            className={`px-4 py-2 rounded-r-xl text-white
              ${isLoading || !inputValue.trim()
                ? 'bg-blue-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
              }`}
            disabled={isLoading || !inputValue.trim()}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
