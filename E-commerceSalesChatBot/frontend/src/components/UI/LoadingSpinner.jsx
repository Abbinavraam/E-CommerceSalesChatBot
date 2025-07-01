import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ 
  size = 'medium', 
  color = 'primary', 
  text = '', 
  overlay = false,
  className = '' 
}) => {
  const sizeClasses = {
    small: 'spinner-small',
    medium: 'spinner-medium',
    large: 'spinner-large'
  };

  const colorClasses = {
    primary: 'spinner-primary',
    secondary: 'spinner-secondary',
    white: 'spinner-white'
  };

  const spinnerContent = (
    <div className={`loading-spinner ${className}`}>
      <div className={`spinner ${sizeClasses[size]} ${colorClasses[color]}`}>
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
      </div>
      {text && <p className="spinner-text">{text}</p>}
    </div>
  );

  if (overlay) {
    return (
      <div className="spinner-overlay">
        {spinnerContent}
      </div>
    );
  }

  return spinnerContent;
};

// Skeleton loader component for better UX
export const SkeletonLoader = ({ 
  width = '100%', 
  height = '20px', 
  borderRadius = '4px',
  className = '' 
}) => {
  return (
    <div 
      className={`skeleton-loader ${className}`}
      style={{ 
        width, 
        height, 
        borderRadius 
      }}
    />
  );
};

// Card skeleton for product cards
export const CardSkeleton = ({ count = 1 }) => {
  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <div key={index} className="card-skeleton">
          <SkeletonLoader height="200px" borderRadius="8px 8px 0 0" />
          <div className="card-skeleton-content">
            <SkeletonLoader height="24px" width="80%" />
            <SkeletonLoader height="16px" width="60%" />
            <SkeletonLoader height="20px" width="40%" />
          </div>
        </div>
      ))}
    </>
  );
};

// Message skeleton for chat
export const MessageSkeleton = ({ count = 3 }) => {
  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <div key={index} className={`message-skeleton ${index % 2 === 0 ? 'user' : 'bot'}`}>
          <SkeletonLoader height="16px" width="70%" />
          <SkeletonLoader height="16px" width="50%" />
        </div>
      ))}
    </>
  );
};

export default LoadingSpinner;