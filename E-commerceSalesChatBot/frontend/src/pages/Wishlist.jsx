import React from 'react';
import {
  FiHeart,
  FiShoppingCart,
  FiTrash2,
  FiEye,
  FiStar
} from 'react-icons/fi';
import { Link } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import './Wishlist.css';

const Wishlist = () => {
  const {
    wishlist,
    addToCart,
    removeFromWishlist
  } = useCart();

  const moveToCart = (product) => {
    addToCart(product);
    removeFromWishlist(product.id);
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<FiStar key={i} className="star filled" fill="currentColor" />);
    }

    if (hasHalfStar) {
      stars.push(<FiStar key="half" className="star half" fill="currentColor" style={{opacity: 0.5}} />);
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<FiStar key={`empty-${i}`} className="star empty" />);
    }

    return stars;
  };

  if (wishlist.length === 0) {
    return (
      <div className="wishlist-page">
        <div className="container">
          <div className="page-header">
            <h1>My Wishlist</h1>
            <p>Save your favorite items for later</p>
          </div>
          
          <div className="empty-wishlist">
            <FiHeart size={64} />
            <h2>Your wishlist is empty</h2>
            <p>Start adding products you love to your wishlist</p>
            <Link to="/products" className="btn btn-primary">
              Browse Products
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="wishlist-page">
      <div className="container">
        <div className="page-header">
          <h1>My Wishlist</h1>
          <p>{wishlist.length} item{wishlist.length !== 1 ? 's' : ''} in your wishlist</p>
        </div>

        <div className="wishlist-grid">
          {wishlist.map(product => (
            <div key={product.id} className="wishlist-item">
              <div className="product-image">
                <img 
                  src={product.image_url || '/placeholder-product.svg'} 
                  alt={product.name}
                  onError={(e) => {
                    e.target.src = '/placeholder-product.svg';
                  }}
                />
              </div>
              
              <div className="product-info">
                <div className="product-category">{product.category}</div>
                <h3 className="product-name">{product.name}</h3>
                <p className="product-description">{product.description}</p>
                
                <div className="product-rating">
                  <div className="stars">
                    {renderStars(product.rating || 4.0)}
                  </div>
                  <span className="rating-text">({(product.rating || 4.0).toFixed(1)})</span>
                </div>
                
                <div className="product-price">
                  <span className="current-price">${product.price}</span>
                  {product.original_price && product.original_price > product.price && (
                    <span className="original-price">${product.original_price}</span>
                  )}
                </div>
                
                <div className="product-stock">
                  <span className={`stock-status ${product.stock > 0 ? 'in-stock' : 'out-of-stock'}`}>
                    {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
                  </span>
                </div>
              </div>
              
              <div className="product-actions">
                <button 
                  className="btn btn-primary"
                  onClick={() => moveToCart(product)}
                  disabled={product.stock === 0}
                >
                  <FiShoppingCart />
                  Move to Cart
                </button>
                
                <button 
                  className="btn btn-secondary"
                  onClick={() => addToCart(product)}
                  disabled={product.stock === 0}
                >
                  <FiShoppingCart />
                  Add to Cart
                </button>
                
                <button 
                  className="btn btn-icon btn-danger"
                  onClick={() => removeFromWishlist(product.id)}
                  title="Remove from wishlist"
                >
                  <FiTrash2 />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Wishlist;
