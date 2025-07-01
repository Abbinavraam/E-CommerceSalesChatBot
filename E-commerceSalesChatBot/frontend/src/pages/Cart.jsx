import React from 'react';
import {
  FiShoppingCart,
  FiTrash2,
  FiPlus,
  FiMinus,
  FiHeart
} from 'react-icons/fi';
import { Link } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import './Cart.css';

const Cart = () => {
  const {
    cart,
    updateQuantity,
    removeFromCart,
    clearCart,
    getTotalPrice,
    getTotalItems,
    addToWishlist,
    isInWishlist
  } = useCart();

  const moveToWishlist = (product) => {
    addToWishlist(product);
    removeFromCart(product.id);
  };

  const addToWishlistOnly = (product) => {
    addToWishlist(product);
    // Don't remove from cart - just add to wishlist
  };

  if (cart.length === 0) {
    return (
      <div className="cart-page">
        <div className="container">
          <div className="page-header">
            <h1>Shopping Cart</h1>
            <p>Your cart is ready for checkout</p>
          </div>
          
          <div className="empty-cart">
            <FiShoppingCart size={64} />
            <h2>Your cart is empty</h2>
            <p>Add some products to your cart to get started</p>
            <Link to="/products" className="btn btn-primary">
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <div className="container">
        <div className="page-header">
          <h1>Shopping Cart</h1>
          <p>{getTotalItems()} item{getTotalItems() !== 1 ? 's' : ''} in your cart</p>
        </div>

        <div className="cart-content">
          <div className="cart-items">
            {cart.map(item => (
              <div key={item.id} className="cart-item">
                <div className="item-image">
                  <img 
                    src={item.image_url || '/placeholder-product.svg'} 
                    alt={item.name}
                    onError={(e) => {
                      e.target.src = '/placeholder-product.svg';
                    }}
                  />
                </div>
                
                <div className="item-info">
                  <div className="item-category">{item.category}</div>
                  <h3 className="item-name">{item.name}</h3>
                  <p className="item-description">{item.description}</p>
                  <div className="item-price">
                    <span className="current-price">${item.price}</span>
                    {item.original_price && item.original_price > item.price && (
                      <span className="original-price">${item.original_price}</span>
                    )}
                  </div>
                </div>
                
                <div className="item-controls">
                  <div className="quantity-controls">
                    <button 
                      className="btn btn-icon"
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    >
                      <FiMinus />
                    </button>
                    <span className="quantity">{item.quantity}</span>
                    <button 
                      className="btn btn-icon"
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      disabled={item.quantity >= item.stock}
                    >
                      <FiPlus />
                    </button>
                  </div>
                  
                  <div className="item-total">
                    ${(item.price * item.quantity).toFixed(2)}
                  </div>
                  
                  <div className="item-actions">
                    <button
                      className={`btn btn-icon ${isInWishlist(item.id) ? 'active' : ''}`}
                      onClick={() => addToWishlistOnly(item)}
                      title={isInWishlist(item.id) ? "Already in wishlist" : "Add to wishlist"}
                    >
                      <FiHeart fill={isInWishlist(item.id) ? "currentColor" : "none"} />
                    </button>
                    <button 
                      className="btn btn-icon btn-danger"
                      onClick={() => removeFromCart(item.id)}
                      title="Remove from cart"
                    >
                      <FiTrash2 />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="cart-summary">
            <div className="summary-card">
              <h3>Order Summary</h3>
              
              <div className="summary-row">
                <span>Subtotal ({getTotalItems()} items)</span>
                <span>${getTotalPrice().toFixed(2)}</span>
              </div>
              
              <div className="summary-row">
                <span>Shipping</span>
                <span>Free</span>
              </div>
              
              <div className="summary-row">
                <span>Tax</span>
                <span>${(getTotalPrice() * 0.08).toFixed(2)}</span>
              </div>
              
              <div className="summary-divider"></div>
              
              <div className="summary-row total">
                <span>Total</span>
                <span>${(getTotalPrice() * 1.08).toFixed(2)}</span>
              </div>
              
              <div className="summary-actions">
                <button className="btn btn-primary btn-lg">
                  Proceed to Checkout
                </button>
                
                <button 
                  className="btn btn-secondary"
                  onClick={clearCart}
                >
                  Clear Cart
                </button>
                
                <Link to="/products" className="btn btn-outline">
                  Continue Shopping
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
