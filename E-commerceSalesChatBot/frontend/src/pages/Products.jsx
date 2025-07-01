import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FiSearch,
  FiFilter,
  FiGrid,
  FiList,
  FiStar,
  FiShoppingCart,
  FiHeart,
  FiEye,
  FiChevronDown,
  FiX
} from 'react-icons/fi';
import { productsAPI } from '../services/api';
import LoadingSpinner from '../components/UI/LoadingSpinner';
import { toast } from 'react-toastify';
import { useCart } from '../contexts/CartContext';
import './Products.css';

const Products = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [priceRange, setPriceRange] = useState({ min: 0, max: 1000 });
  const [sortBy, setSortBy] = useState('name');
  const [viewMode, setViewMode] = useState('grid');
  const [showFilters, setShowFilters] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showProductModal, setShowProductModal] = useState(false);

  // Use cart context
  const { addToCart: addToCartContext, toggleWishlist, isInWishlist } = useCart();

  // Wrapper function to preserve scroll position
  const addToCart = (product) => {
    const scrollPosition = window.pageYOffset;
    addToCartContext(product);
    // Restore scroll position after state update
    setTimeout(() => {
      window.scrollTo(0, scrollPosition);
    }, 0);
  };

  useEffect(() => {
    loadProducts();
    loadCategories();
  }, [currentPage, selectedCategory, sortBy, searchQuery]);

  const openProductModal = (product) => {
    setSelectedProduct(product);
    setShowProductModal(true);
  };

  const closeProductModal = () => {
    setSelectedProduct(null);
    setShowProductModal(false);
  };

  const buyNow = (product) => {
    // Add to cart first
    addToCart(product);
    // Then navigate to cart page without page reload
    setTimeout(() => {
      navigate('/cart');
    }, 500);
  };

  const loadProducts = async () => {
    try {
      setLoading(true);
      const params = {
        page: currentPage,
        limit: 12,
        category: selectedCategory,
        sort: sortBy,
        search: searchQuery,
        min_price: priceRange.min,
        max_price: priceRange.max
      };

      const response = await productsAPI.getProducts(params);
      setProducts(response.data.products || []);
      setTotalPages(response.data.total_pages || 1);
    } catch (error) {
      console.error('Failed to load products:', error);
      toast.error('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await productsAPI.getCategories();
      setCategories(response.data || []);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadProducts();
  };

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    setCurrentPage(1);
  };

  const handleSortChange = (sort) => {
    setSortBy(sort);
    setCurrentPage(1);
  };

  const handlePriceRangeChange = (min, max) => {
    setPriceRange({ min, max });
    setCurrentPage(1);
  };

  const clearFilters = () => {
    setSelectedCategory('');
    setPriceRange({ min: 0, max: 1000 });
    setSearchQuery('');
    setCurrentPage(1);
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<FiStar key={i} className="star filled" fill="currentColor" />);
    }

    if (hasHalfStar) {
      stars.push(<FiStar key="half" className="star half" />);
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<FiStar key={`empty-${i}`} className="star empty" />);
    }

    return stars;
  };

  const ProductCard = ({ product }) => (
    <div className={`product-card ${viewMode}`}>
      <div className="product-image">
        <img
          src={product.image_url || '/placeholder-product.svg'}
          alt={product.name}
          onError={(e) => {
            e.target.src = '/placeholder-product.svg';
          }}
          loading="lazy"
        />
        <div className="product-overlay">
          <button
            className={`btn btn-icon ${isInWishlist(product.id) ? 'active' : ''}`}
            title={isInWishlist(product.id) ? "Remove from Wishlist" : "Add to Wishlist"}
            onClick={() => toggleWishlist(product)}
          >
            <FiHeart fill={isInWishlist(product.id) ? "currentColor" : "none"} />
          </button>
          <button
            className="btn btn-icon"
            title="Quick View"
            onClick={() => openProductModal(product)}
          >
            <FiEye />
          </button>
        </div>
      </div>
      
      <div className="product-info">
        <div className="product-category">{product.category}</div>
        <h3 className="product-name">{product.name}</h3>
        <p className="product-description">{product.description}</p>
        
        <div className="product-rating">
          <div className="stars">
            {renderStars(product.rating || (3.5 + Math.random() * 1.5))}
          </div>
          <span className="rating-text">({(product.rating || (3.5 + Math.random() * 1.5)).toFixed(1)})</span>
        </div>
        
        <div className="product-price">
          {product.original_price && product.original_price > product.price && (
            <span className="original-price">{formatPrice(product.original_price)}</span>
          )}
          <span className="current-price">{formatPrice(product.price)}</span>
        </div>
        
        <div className="product-actions">
          <button
            className="btn btn-secondary"
            onClick={() => addToCart(product)}
            disabled={product.stock === 0}
          >
            <FiShoppingCart />
            {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
          </button>

          <button
            className="btn btn-primary"
            onClick={() => buyNow(product)}
            disabled={product.stock === 0}
          >
            Buy Now
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="products-page">
      <div className="container">
        {/* Page Header */}
        <div className="page-header">
          <h1>Products</h1>
          <p>Discover amazing products with the help of our AI assistant</p>
        </div>

        {/* Search and Filters */}
        <div className="products-controls">
          <div className="search-section">
            <form onSubmit={handleSearch} className="search-form">
              <div className="search-input-group">
                <FiSearch className="search-icon" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search products..."
                  className="search-input"
                />
                <button type="submit" className="btn btn-primary">
                  Search
                </button>
              </div>
            </form>
          </div>

          <div className="controls-row">
            <div className="filters-toggle">
              <button 
                className="btn btn-outline"
                onClick={() => setShowFilters(!showFilters)}
              >
                <FiFilter />
                Filters
                <FiChevronDown className={showFilters ? 'rotated' : ''} />
              </button>
            </div>

            <div className="view-controls">
              <div className="sort-dropdown">
                <select 
                  value={sortBy} 
                  onChange={(e) => handleSortChange(e.target.value)}
                  className="sort-select"
                >
                  <option value="name">Sort by Name</option>
                  <option value="price_asc">Price: Low to High</option>
                  <option value="price_desc">Price: High to Low</option>
                  <option value="rating">Rating</option>
                  <option value="newest">Newest</option>
                </select>
              </div>

              <div className="view-mode-toggle">
                <button 
                  className={`btn btn-icon ${viewMode === 'grid' ? 'active' : ''}`}
                  onClick={() => setViewMode('grid')}
                >
                  <FiGrid />
                </button>
                <button 
                  className={`btn btn-icon ${viewMode === 'list' ? 'active' : ''}`}
                  onClick={() => setViewMode('list')}
                >
                  <FiList />
                </button>
              </div>
            </div>
          </div>

          {/* Filters Panel */}
          {showFilters && (
            <div className="filters-panel">
              <div className="filters-content">
                <div className="filter-group">
                  <h4>Category</h4>
                  <div className="category-filters">
                    <button 
                      className={`filter-chip ${selectedCategory === '' ? 'active' : ''}`}
                      onClick={() => handleCategoryChange('')}
                    >
                      All Categories
                    </button>
                    {categories.map((category) => (
                      <button 
                        key={category}
                        className={`filter-chip ${selectedCategory === category ? 'active' : ''}`}
                        onClick={() => handleCategoryChange(category)}
                      >
                        {category}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="filter-group">
                  <h4>Price Range</h4>
                  <div className="price-range">
                    <input
                      type="range"
                      min="0"
                      max="1000"
                      value={priceRange.min}
                      onChange={(e) => handlePriceRangeChange(parseInt(e.target.value), priceRange.max)}
                      className="range-slider"
                    />
                    <input
                      type="range"
                      min="0"
                      max="1000"
                      value={priceRange.max}
                      onChange={(e) => handlePriceRangeChange(priceRange.min, parseInt(e.target.value))}
                      className="range-slider"
                    />
                    <div className="price-labels">
                      <span>{formatPrice(priceRange.min)}</span>
                      <span>{formatPrice(priceRange.max)}</span>
                    </div>
                  </div>
                </div>

                <div className="filter-actions">
                  <button className="btn btn-outline" onClick={clearFilters}>
                    <FiX />
                    Clear Filters
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Products Grid */}
        <div className="products-section">
          {loading ? (
            <div className="loading-container">
              <LoadingSpinner />
              <p>Loading products...</p>
            </div>
          ) : products.length === 0 ? (
            <div className="empty-products">
              <FiSearch size={64} />
              <h3>No products found</h3>
              <p>Try adjusting your search criteria or filters</p>
              <button className="btn btn-primary" onClick={clearFilters}>
                Clear Filters
              </button>
            </div>
          ) : (
            <>
              <div className={`products-grid ${viewMode}`}>
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="pagination">
                  <button 
                    className="btn btn-outline"
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                  >
                    Previous
                  </button>
                  
                  <div className="page-numbers">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                      <button
                        key={page}
                        className={`btn ${page === currentPage ? 'btn-primary' : 'btn-outline'}`}
                        onClick={() => setCurrentPage(page)}
                      >
                        {page}
                      </button>
                    ))}
                  </div>
                  
                  <button 
                    className="btn btn-outline"
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Product Modal */}
      {showProductModal && selectedProduct && (
        <div className="modal-overlay" onClick={closeProductModal}>
          <div className="product-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeProductModal}>
              <FiX />
            </button>

            <div className="modal-content">
              <div className="modal-image">
                <img
                  src={selectedProduct.image_url || '/placeholder-product.svg'}
                  alt={selectedProduct.name}
                  onError={(e) => {
                    e.target.src = '/placeholder-product.svg';
                  }}
                />
              </div>

              <div className="modal-info">
                <div className="product-category">{selectedProduct.category}</div>
                <h2 className="product-name">{selectedProduct.name}</h2>
                <p className="product-description">{selectedProduct.description}</p>

                <div className="product-rating">
                  <div className="stars">
                    {renderStars(selectedProduct.rating || (3.5 + Math.random() * 1.5))}
                  </div>
                  <span className="rating-text">
                    ({(selectedProduct.rating || (3.5 + Math.random() * 1.5)).toFixed(1)})
                  </span>
                </div>

                <div className="product-price">
                  <span className="current-price">${selectedProduct.price}</span>
                  {selectedProduct.original_price && selectedProduct.original_price > selectedProduct.price && (
                    <span className="original-price">${selectedProduct.original_price}</span>
                  )}
                </div>

                <div className="product-stock">
                  <span className={`stock-status ${selectedProduct.stock > 0 ? 'in-stock' : 'out-of-stock'}`}>
                    {selectedProduct.stock > 0 ? `${selectedProduct.stock} in stock` : 'Out of stock'}
                  </span>
                </div>

                <div className="modal-actions">
                  <button
                    className={`btn btn-icon ${isInWishlist(selectedProduct.id) ? 'active' : ''}`}
                    onClick={() => toggleWishlist(selectedProduct)}
                    title={isInWishlist(selectedProduct.id) ? "Remove from Wishlist" : "Add to Wishlist"}
                  >
                    <FiHeart fill={isInWishlist(selectedProduct.id) ? "currentColor" : "none"} />
                    {isInWishlist(selectedProduct.id) ? "Remove from Wishlist" : "Add to Wishlist"}
                  </button>

                  <button
                    className="btn btn-secondary"
                    onClick={() => addToCart(selectedProduct)}
                    disabled={selectedProduct.stock === 0}
                  >
                    <FiShoppingCart />
                    {selectedProduct.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
                  </button>

                  <button
                    className="btn btn-primary"
                    onClick={() => buyNow(selectedProduct)}
                    disabled={selectedProduct.stock === 0}
                  >
                    Buy Now
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Products;