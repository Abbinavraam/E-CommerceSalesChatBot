import React, { useState, useEffect, useRef } from 'react';
import { useChat } from '../contexts/ChatContext';
import { useAuth } from '../contexts/AuthContext';
import {
  FiSend,
  FiPlus,
  FiMessageCircle,
  FiUser,
  FiCpu,
  FiClock,
  FiWifi,
  FiWifiOff
} from 'react-icons/fi';
import LoadingSpinner from '../components/UI/LoadingSpinner';
import './Chat.css';

const Chat = () => {
  const [message, setMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const { user } = useAuth();
  const {
    currentSession,
    messages,
    sessions,
    loading,
    typing,
    connected,
    startNewSession,
    sendMessage,
    switchSession,
    hasActiveSession
  } = useChat();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages, typing]);

  // Focus input when component mounts
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!message.trim() || isSending) {
      return;
    }

    const messageToSend = message.trim();
    setMessage('');
    setIsSending(true);

    try {
      await sendMessage(messageToSend);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsSending(false);
    }
  };

  const handleNewChat = async () => {
    try {
      await startNewSession();
    } catch (error) {
      console.error('Failed to start new chat:', error);
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString();
    }
  };

  const renderMessage = (msg, index) => {
    const isBot = msg.message_type === 'bot';
    const isUser = msg.message_type === 'user';

    return (
      <div key={msg.id || index} className={`message ${isBot ? 'bot' : 'user'}`}>
        <div className="message-avatar">
          {isBot ? <FiCpu /> : <FiUser />}
        </div>
        <div className="message-content">
          <div className="message-bubble">
            <p>{msg.content}</p>
          </div>
          <div className="message-meta">
            <span className="message-time">
              <FiClock size={12} />
              {formatTimestamp(msg.timestamp)}
            </span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        {/* Sidebar */}
        <div className="chat-sidebar">
          <div className="sidebar-header">
            <h2>Chat Sessions</h2>
            <button 
              className="btn btn-primary btn-sm"
              onClick={handleNewChat}
              disabled={loading}
            >
              <FiPlus />
              New Chat
            </button>
          </div>

          <div className="sessions-list">
            {sessions.length === 0 ? (
              <div className="empty-sessions">
                <FiMessageCircle size={48} />
                <p>No chat sessions yet</p>
                <button 
                  className="btn btn-outline btn-sm"
                  onClick={handleNewChat}
                  disabled={loading}
                >
                  Start Your First Chat
                </button>
              </div>
            ) : (
              sessions.map((session) => (
                <div
                  key={session.session_id}
                  className={`session-item ${
                    currentSession?.session_id === session.session_id ? 'active' : ''
                  }`}
                  onClick={() => switchSession(session)}
                >
                  <div className="session-info">
                    <div className="session-title">
                      Chat Session
                    </div>
                    <div className="session-date">
                      {formatDate(session.started_at)}
                    </div>
                  </div>
                  <div className="session-status">
                    {session.is_active && (
                      <span className="status-indicator active"></span>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="sidebar-footer">
            <div className="connection-status">
              {connected ? (
                <div className="status-connected">
                  <FiWifi />
                  <span>Connected</span>
                </div>
              ) : (
                <div className="status-disconnected">
                  <FiWifiOff />
                  <span>Disconnected</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="chat-main">
          {!hasActiveSession ? (
            <div className="chat-welcome">
              <div className="welcome-content">
                <FiMessageCircle size={64} />
                <h2>Welcome to ShopBot, {user?.username}!</h2>
                <p>
                  I'm your AI shopping assistant. I can help you find products, 
                  compare prices, and make informed purchasing decisions.
                </p>
                <button 
                  className="btn btn-primary btn-lg"
                  onClick={handleNewChat}
                  disabled={loading}
                >
                  <FiPlus />
                  Start Shopping Chat
                </button>
              </div>
            </div>
          ) : (
            <>
              {/* Chat Header */}
              <div className="chat-header">
                <div className="chat-info">
                  <h3>Shopping Assistant</h3>
                  <span className="chat-status">
                    {typing ? 'Typing...' : 'Online'}
                  </span>
                </div>
              </div>

              {/* Messages Area */}
              <div className="messages-container">
                {loading && messages.length === 0 ? (
                  <div className="loading-messages">
                    <LoadingSpinner />
                    <p>Loading chat history...</p>
                  </div>
                ) : (
                  <div className="messages-list">
                    {messages.map((msg, index) => renderMessage(msg, index))}
                    
                    {typing && (
                      <div className="message bot typing-indicator">
                        <div className="message-avatar">
                          <FiCpu />
                        </div>
                        <div className="message-content">
                          <div className="message-bubble">
                            <div className="typing-dots">
                              <span></span>
                              <span></span>
                              <span></span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    
                    <div ref={messagesEndRef} />
                  </div>
                )}
              </div>

              {/* Message Input */}
              <div className="chat-input-container">
                <form onSubmit={handleSubmit} className="chat-input-form">
                  <div className="input-wrapper">
                    <input
                      ref={inputRef}
                      type="text"
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      placeholder="Ask me about products, prices, or recommendations..."
                      className="chat-input"
                      disabled={isSending || !connected}
                    />
                    <button
                      type="submit"
                      className="send-button"
                      disabled={!message.trim() || isSending || !connected}
                    >
                      {isSending ? (
                        <LoadingSpinner size="small" />
                      ) : (
                        <FiSend />
                      )}
                    </button>
                  </div>
                </form>
                
                <div className="input-suggestions">
                  <button 
                    className="suggestion-chip"
                    onClick={() => setMessage("I'm looking for a laptop for programming")}
                    disabled={isSending}
                  >
                    Find programming laptops
                  </button>
                  <button 
                    className="suggestion-chip"
                    onClick={() => setMessage("What are the best smartphones under $500?")}
                    disabled={isSending}
                  >
                    Budget smartphones
                  </button>
                  <button 
                    className="suggestion-chip"
                    onClick={() => setMessage("Show me trending products")}
                    disabled={isSending}
                  >
                    Trending products
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Chat;