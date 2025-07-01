import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useChat } from '../../contexts/ChatContext';
import { useCart } from '../../contexts/CartContext';
import {
  FiUser,
  FiLogOut,
  FiMenu,
  FiX,
  FiMessageCircle,
  FiShoppingBag,
  FiHome,
  FiWifi,
  FiWifiOff,
  FiShoppingCart,
  FiHeart
} from 'react-icons/fi';
import './Navbar.css';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const { connected, hasActiveSession } = useChat();
  const { getTotalItems, getWishlistCount } = useCart();
  const location = useLocation();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMobileMenuOpen(false);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  const isActivePath = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo */}
        <Link to="/" className="navbar-logo" onClick={closeMobileMenu}>
          <FiMessageCircle className="logo-icon" />
          <span>ShopBot</span>
        </Link>

        {/* Desktop Navigation */}
        <div className="navbar-menu">
          <Link 
            to="/" 
            className={`navbar-link ${isActivePath('/') ? 'active' : ''}`}
          >
            <FiHome />
            <span>Home</span>
          </Link>
          
          {isAuthenticated && (
            <>
              <Link 
                to="/chat" 
                className={`navbar-link ${isActivePath('/chat') ? 'active' : ''}`}
              >
                <FiMessageCircle />
                <span>Chat</span>
                {hasActiveSession && <span className="active-indicator" />}
              </Link>
              
              <Link
                to="/products"
                className={`navbar-link ${isActivePath('/products') ? 'active' : ''}`}
              >
                <FiShoppingBag />
                <span>Products</span>
              </Link>

              <Link
                to="/wishlist"
                className={`navbar-link ${isActivePath('/wishlist') ? 'active' : ''}`}
              >
                <FiHeart />
                <span>Wishlist</span>
                {getWishlistCount() > 0 && <span className="badge">{getWishlistCount()}</span>}
              </Link>

              <Link
                to="/cart"
                className={`navbar-link ${isActivePath('/cart') ? 'active' : ''}`}
              >
                <FiShoppingCart />
                <span>Cart</span>
                {getTotalItems() > 0 && <span className="badge">{getTotalItems()}</span>}
              </Link>
            </>
          )}
        </div>

        {/* User Menu */}
        <div className="navbar-user">
          {/* Connection Status */}
          {isAuthenticated && (
            <div className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
              {connected ? <FiWifi /> : <FiWifiOff />}
              <span className="tooltip">
                {connected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          )}

          {isAuthenticated ? (
            <div className="user-menu">
              <Link 
                to="/profile" 
                className={`user-link ${isActivePath('/profile') ? 'active' : ''}`}
              >
                <FiUser />
                <span>{user?.username}</span>
              </Link>
              
              <button 
                onClick={handleLogout}
                className="logout-btn"
                title="Logout"
              >
                <FiLogOut />
              </button>
            </div>
          ) : (
            <div className="auth-links">
              <Link 
                to="/login" 
                className={`auth-link ${isActivePath('/login') ? 'active' : ''}`}
              >
                Login
              </Link>
              <Link 
                to="/register" 
                className={`auth-link register ${isActivePath('/register') ? 'active' : ''}`}
              >
                Register
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button 
          className="mobile-menu-btn"
          onClick={toggleMobileMenu}
          aria-label="Toggle mobile menu"
        >
          {isMobileMenuOpen ? <FiX /> : <FiMenu />}
        </button>
      </div>

      {/* Mobile Menu */}
      <div className={`mobile-menu ${isMobileMenuOpen ? 'open' : ''}`}>
        <div className="mobile-menu-content">
          <Link 
            to="/" 
            className={`mobile-link ${isActivePath('/') ? 'active' : ''}`}
            onClick={closeMobileMenu}
          >
            <FiHome />
            <span>Home</span>
          </Link>
          
          {isAuthenticated ? (
            <>
              <Link 
                to="/chat" 
                className={`mobile-link ${isActivePath('/chat') ? 'active' : ''}`}
                onClick={closeMobileMenu}
              >
                <FiMessageCircle />
                <span>Chat</span>
                {hasActiveSession && <span className="active-indicator" />}
              </Link>
              
              <Link 
                to="/products" 
                className={`mobile-link ${isActivePath('/products') ? 'active' : ''}`}
                onClick={closeMobileMenu}
              >
                <FiShoppingBag />
                <span>Products</span>
              </Link>
              
              <Link 
                to="/profile" 
                className={`mobile-link ${isActivePath('/profile') ? 'active' : ''}`}
                onClick={closeMobileMenu}
              >
                <FiUser />
                <span>Profile</span>
              </Link>
              
              <div className="mobile-user-info">
                <span>Logged in as: {user?.username}</span>
                <div className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
                  {connected ? <FiWifi /> : <FiWifiOff />}
                  <span>{connected ? 'Connected' : 'Disconnected'}</span>
                </div>
              </div>
              
              <button 
                onClick={handleLogout}
                className="mobile-logout-btn"
              >
                <FiLogOut />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <div className="mobile-auth-links">
              <Link 
                to="/login" 
                className={`mobile-link ${isActivePath('/login') ? 'active' : ''}`}
                onClick={closeMobileMenu}
              >
                Login
              </Link>
              <Link 
                to="/register" 
                className={`mobile-link register ${isActivePath('/register') ? 'active' : ''}`}
                onClick={closeMobileMenu}
              >
                Register
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div 
          className="mobile-menu-overlay"
          onClick={closeMobileMenu}
        />
      )}
    </nav>
  );
};

export default Navbar;
