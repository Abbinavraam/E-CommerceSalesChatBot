import { io } from 'socket.io-client';

class SocketService {
  constructor() {
    this.socket = null;
    this.connected = false;
  }

  connect() {
    if (this.socket && this.connected) {
      return;
    }

    const token = localStorage.getItem('token');
    const serverUrl = import.meta.env.VITE_SOCKET_URL || import.meta.env.VITE_API_URL || 'http://localhost:5000';

    this.socket = io(serverUrl, {
      auth: {
        token: token
      },
      transports: ['websocket', 'polling'],
      timeout: 20000,
      forceNew: true
    });

    this.socket.on('connect', () => {
      this.connected = true;
      console.log('Socket.IO connected');
    });

    this.socket.on('disconnect', (reason) => {
      this.connected = false;
      console.log('Socket.IO disconnected:', reason);
      
      // Attempt to reconnect if disconnection was unexpected
      if (reason === 'io server disconnect') {
        // Server initiated disconnect, don't reconnect
        return;
      }
      
      // Auto-reconnect for other reasons
      setTimeout(() => {
        if (!this.connected) {
          this.connect();
        }
      }, 5000);
    });

    this.socket.on('connect_error', (error) => {
      console.error('Socket.IO connection error:', error);
      this.connected = false;
    });

    this.socket.on('error', (error) => {
      console.error('Socket.IO error:', error);
    });

    return this.socket;
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.connected = false;
    }
  }

  // Join a chat session room
  joinSession(sessionId) {
    if (this.socket && this.connected) {
      this.socket.emit('join', { session_id: sessionId });
    }
  }

  // Leave a chat session room
  leaveSession(sessionId) {
    if (this.socket && this.connected) {
      this.socket.emit('leave', { session_id: sessionId });
    }
  }

  // Send a message
  sendMessage(sessionId, message) {
    if (this.socket && this.connected) {
      this.socket.emit('message', {
        session_id: sessionId,
        content: message
      });
    }
  }

  // Emit typing indicator
  startTyping(sessionId) {
    if (this.socket && this.connected) {
      this.socket.emit('typing', { session_id: sessionId });
    }
  }

  // Stop typing indicator
  stopTyping(sessionId) {
    if (this.socket && this.connected) {
      this.socket.emit('stop_typing', { session_id: sessionId });
    }
  }

  // Listen for events
  on(event, callback) {
    if (this.socket) {
      this.socket.on(event, callback);
    }
  }

  // Remove event listener
  off(event, callback) {
    if (this.socket) {
      this.socket.off(event, callback);
    }
  }

  // Emit custom events
  emit(event, data) {
    if (this.socket && this.connected) {
      this.socket.emit(event, data);
    }
  }

  // Get connection status
  isConnected() {
    return this.connected && this.socket?.connected;
  }

  // Get socket ID
  getSocketId() {
    return this.socket?.id;
  }

  // Reconnect manually
  reconnect() {
    if (this.socket) {
      this.socket.connect();
    } else {
      this.connect();
    }
  }
}

// Create and export a singleton instance
const socketService = new SocketService();
export default socketService;