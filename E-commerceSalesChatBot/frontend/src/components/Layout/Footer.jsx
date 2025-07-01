import React from 'react';
import { Link } from 'react-router-dom';
import {
  FiMessageCircle,
  FiExternalLink,
  FiMail,
  FiHeart,
  FiShield,
  FiHelpCircle
} from 'react-icons/fi';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        {/* Main Footer Content */}
        <div className="footer-content">
          {/* Brand Section */}
          <div className="footer-section">
            <div className="footer-brand">
              <FiMessageCircle className="footer-logo-icon" />
              <span className="footer-brand-name">ShopBot</span>
            </div>
            <p className="footer-description">
              Your intelligent shopping assistant powered by AI. 
              Find the perfect products with conversational ease.
            </p>
            <div className="footer-social">
              <a 
                href="https://github.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="social-link"
                aria-label="GitHub"
              >
                <FiExternalLink />
              </a>
              <a 
                href="mailto:support@shopbot.com" 
                className="social-link"
                aria-label="Email"
              >
                <FiMail />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div className="footer-section">
            <h3 className="footer-title">Quick Links</h3>
            <ul className="footer-links">
              <li>
                <Link to="/" className="footer-link">Home</Link>
              </li>
              <li>
                <Link to="/chat" className="footer-link">Chat</Link>
              </li>
              <li>
                <Link to="/products" className="footer-link">Products</Link>
              </li>
              <li>
                <Link to="/profile" className="footer-link">Profile</Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div className="footer-section">
            <h3 className="footer-title">Support</h3>
            <ul className="footer-links">
              <li>
                <a href="#help" className="footer-link">
                  <FiHelpCircle className="link-icon" />
                  Help Center
                </a>
              </li>
              <li>
                <a href="#privacy" className="footer-link">
                  <FiShield className="link-icon" />
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#terms" className="footer-link">
                  Terms of Service
                </a>
              </li>
              <li>
                <a href="#contact" className="footer-link">
                  Contact Us
                </a>
              </li>
            </ul>
          </div>

          {/* Features */}
          <div className="footer-section">
            <h3 className="footer-title">Features</h3>
            <ul className="footer-links">
              <li>
                <span className="footer-link">AI-Powered Search</span>
              </li>
              <li>
                <span className="footer-link">Real-time Chat</span>
              </li>
              <li>
                <span className="footer-link">Product Recommendations</span>
              </li>
              <li>
                <span className="footer-link">Session History</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="footer-bottom">
          <div className="footer-bottom-content">
            <p className="copyright">
              © {currentYear} ShopBot. All rights reserved.
            </p>
            <p className="made-with-love">
              Made with <FiHeart className="heart-icon" /> for better shopping experience
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
