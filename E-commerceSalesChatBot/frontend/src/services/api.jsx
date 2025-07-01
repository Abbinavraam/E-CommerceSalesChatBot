import axios from 'axios';
import { toast } from 'react-toastify';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production'
    ? '' // Use relative URLs in production (Vercel will handle routing)
    : '', // Use relative URLs in development (Vite proxy)
  timeout: 10000,
  // Remove default headers to avoid preflight issues
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token && token.trim()) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // Remove Authorization header if no token to avoid preflight
    if (!token || !token.trim()) {
      delete config.headers.Authorization;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Handle network errors
    if (!error.response) {
      toast.error('Network error. Please check your connection.');
      return Promise.reject(error);
    }

    const { status, data } = error.response;

    // Handle different HTTP status codes
    switch (status) {
      case 401:
        // Unauthorized - token expired or invalid
        if (!originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            // Try to refresh token
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
              const response = await axios.post(
                `${api.defaults.baseURL}/api/auth/refresh`,
                {},
                {
                  headers: {
                    Authorization: `Bearer ${refreshToken}`,
                  },
                }
              );
              
              const { access_token } = response.data;
              localStorage.setItem('token', access_token);
              
              // Retry original request with new token
              originalRequest.headers.Authorization = `Bearer ${access_token}`;
              return api(originalRequest);
            }
          } catch (refreshError) {
            // Refresh failed, redirect to login
            localStorage.removeItem('token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
        
        // If retry failed or no refresh token, redirect to login
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        break;

      case 403:
        toast.error('Access forbidden. You don\'t have permission to perform this action.');
        break;

      case 404:
        toast.error('Resource not found.');
        break;

      case 422:
        // Validation errors
        if (data.errors) {
          Object.values(data.errors).forEach(errorArray => {
            errorArray.forEach(errorMessage => {
              toast.error(errorMessage);
            });
          });
        } else {
          toast.error(data.message || 'Validation error occurred.');
        }
        break;

      case 429:
        toast.error('Too many requests. Please try again later.');
        break;

      case 500:
        toast.error('Server error. Please try again later.');
        break;

      default:
        toast.error(data.message || 'An unexpected error occurred.');
    }

    return Promise.reject(error);
  }
);

// API methods for different endpoints
export const authAPI = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  register: (userData) => api.post('/api/auth/register', userData),
  refresh: () => api.post('/api/auth/refresh'),
  profile: () => api.get('/api/auth/profile'),
  updateProfile: (data) => api.put('/api/auth/profile', data),
};

export const chatAPI = {
  startSession: () => api.post('/api/chat/start'),
  sendMessage: (data) => api.post('/api/chat/message', data),
  getHistory: (sessionId) => api.get(`/api/chat/history/${sessionId}`),
  getSessions: () => api.get('/api/chat/sessions'),
};

export const productsAPI = {
  getProducts: (params) => api.get('/api/products', { params }),
  getProduct: (id) => api.get(`/api/products/${id}`),
  searchProducts: (query) => api.get('/api/products/search', { params: { q: query } }),
  getCategories: () => api.get('/api/products/categories'),
  getRecommendations: () => api.get('/api/products/recommendations'),
  getPriceRange: () => api.get('/api/products/price-range'),
};

// Utility functions
export const handleApiError = (error, defaultMessage = 'An error occurred') => {
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.response?.data?.error) {
    return error.response.data.error;
  }
  if (error.message) {
    return error.message;
  }
  return defaultMessage;
};

export const isNetworkError = (error) => {
  return !error.response && error.code === 'NETWORK_ERROR';
};

export const isTimeoutError = (error) => {
  return error.code === 'ECONNABORTED';
};

export default api;