import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { toast } from 'react-toastify';
import { useAuth } from './AuthContext';
import api from '../services/api';
import socketService from '../services/socketService';

const ChatContext = createContext();

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export const ChatProvider = ({ children }) => {
  const { user, isAuthenticated } = useAuth();
  const [currentSession, setCurrentSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [typing, setTyping] = useState(false);
  const [connected, setConnected] = useState(false);

  // Initialize connection state when user is authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      // Since we're using HTTP API instead of WebSocket, set connected to true
      setConnected(true);
      console.log('Chat connected via HTTP API');
    } else {
      setConnected(false);
      console.log('Chat disconnected');
    }
  }, [isAuthenticated, user]);

  // Join current session room when session changes
  useEffect(() => {
    if (currentSession && connected) {
      socketService.joinSession(currentSession.session_id);
    }
  }, [currentSession, connected]);

  const startNewSession = async () => {
    try {
      setLoading(true);
      const response = await api.post('/api/chat/start');
      const newSession = {
        session_id: response.data.session_id,
        started_at: new Date().toISOString(),
        is_active: true
      };
      
      setCurrentSession(newSession);
      setMessages([]);
      setSessions(prev => [newSession, ...prev]);
      
      // Add welcome message
      const welcomeMessage = {
        id: 'welcome',
        content: 'Hello! I\'m your shopping assistant. How can I help you find the perfect product today?',
        message_type: 'bot',
        timestamp: new Date().toISOString()
      };
      setMessages([welcomeMessage]);
      
      return newSession;
    } catch (error) {
      console.error('Failed to start chat session:', error);
      toast.error('Failed to start chat session');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async (content) => {
    if (!currentSession || !content.trim()) {
      return;
    }

    try {
      setTyping(true);
      
      // Add user message immediately for better UX
      const userMessage = {
        id: `temp-${Date.now()}`,
        content: content.trim(),
        message_type: 'user',
        timestamp: new Date().toISOString(),
        session_id: currentSession.session_id
      };
      
      setMessages(prev => [...prev, userMessage]);

      const response = await api.post('/api/chat/message', {
        content: content.trim(),
        session_id: currentSession.session_id
      });

      // Replace temporary message with actual message from server
      setMessages(prev => {
        const filtered = prev.filter(msg => msg.id !== userMessage.id);
        return [...filtered, response.data.user_message, response.data.bot_message];
      });

    } catch (error) {
      console.error('Failed to send message:', error);
      toast.error('Failed to send message');
      
      // Remove temporary message on error
      setMessages(prev => prev.filter(msg => msg.id !== `temp-${Date.now()}`));
    } finally {
      setTyping(false);
    }
  };

  const loadChatHistory = async (sessionId) => {
    try {
      setLoading(true);
      const response = await api.get(`/api/chat/history/${sessionId}`);
      setMessages(response.data);
    } catch (error) {
      console.error('Failed to load chat history:', error);
      toast.error('Failed to load chat history');
    } finally {
      setLoading(false);
    }
  };

  const loadUserSessions = async () => {
    try {
      const response = await api.get('/api/chat/sessions');
      setSessions(response.data);
    } catch (error) {
      console.error('Failed to load chat sessions:', error);
      toast.error('Failed to load chat sessions');
    }
  };

  const switchSession = async (session) => {
    if (currentSession?.session_id === session.session_id) {
      return;
    }

    setCurrentSession(session);
    await loadChatHistory(session.session_id);
  };

  const clearCurrentSession = () => {
    setCurrentSession(null);
    setMessages([]);
  };

  const resetChat = useCallback(() => {
    setMessages([]);
    setCurrentSession(null);
    setTyping(false);
  }, []);

  // Auto-load sessions when user is authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      loadUserSessions();
    } else {
      // Clear chat data when user logs out
      resetChat();
      setSessions([]);
    }
  }, [isAuthenticated, user, resetChat]);

  const value = {
    // State
    currentSession,
    messages,
    sessions,
    loading,
    typing,
    connected,
    
    // Actions
    startNewSession,
    sendMessage,
    loadChatHistory,
    loadUserSessions,
    switchSession,
    clearCurrentSession,
    resetChat,
    
    // Computed values
    hasActiveSession: !!currentSession,
    messageCount: messages.length
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};