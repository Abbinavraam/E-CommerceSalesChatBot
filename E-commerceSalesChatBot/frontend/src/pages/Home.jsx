import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  FiMessageCircle, 
  FiSearch, 
  FiShoppingBag, 
  FiZap,
  FiUsers,
  FiTrendingUp,
  FiArrowRight,
  FiStar,
  FiShield,
  FiClock
} from 'react-icons/fi';
import './Home.css';

const Home = () => {
  const { isAuthenticated } = useAuth();

  const features = [
    {
      icon: <FiMessageCircle />,
      title: 'AI-Powered Chat',
      description: 'Engage with our intelligent chatbot that understands your shopping needs and provides personalized recommendations.'
    },
    {
      icon: <FiSearch />,
      title: 'Smart Product Search',
      description: 'Find exactly what you\'re looking for with our advanced search capabilities and natural language processing.'
    },
    {
      icon: <FiShoppingBag />,
      title: 'Seamless Shopping',
      description: 'Browse, compare, and discover products effortlessly with our intuitive shopping experience.'
    },
    {
      icon: <FiZap />,
      title: 'Real-time Responses',
      description: 'Get instant answers and recommendations with our lightning-fast response system.'
    },
    {
      icon: <FiUsers />,
      title: 'Personalized Experience',
      description: 'Enjoy a tailored shopping journey based on your preferences and shopping history.'
    },
    {
      icon: <FiTrendingUp />,
      title: 'Trending Products',
      description: 'Stay updated with the latest trends and popular products in your favorite categories.'
    }
  ];

  const stats = [
    { number: '10K+', label: 'Happy Customers' },
    { number: '100+', label: 'Products Available' },
    { number: '24/7', label: 'Customer Support' },
    { number: '99.9%', label: 'Uptime' }
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Regular Customer',
      content: 'ShopBot made my shopping experience so much easier! The AI understands exactly what I\'m looking for.',
      rating: 5
    },
    {
      name: 'Mike Chen',
      role: 'Tech Enthusiast',
      content: 'The real-time chat feature is incredible. I get instant help finding the perfect tech products.',
      rating: 5
    },
    {
      name: 'Emily Davis',
      role: 'Busy Professional',
      content: 'I love how personalized the recommendations are. It saves me so much time when shopping online.',
      rating: 5
    }
  ];

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-container">
          <div className="hero-content">
            <div className="hero-text">
              <h1 className="hero-title">
                Your Intelligent
                <span className="hero-highlight"> Shopping Assistant</span>
              </h1>
              <p className="hero-description">
                Experience the future of online shopping with our AI-powered chatbot. 
                Get personalized recommendations, instant support, and seamless product discovery.
              </p>
              <div className="hero-actions">
                {isAuthenticated ? (
                  <Link to="/chat" className="btn btn-primary btn-lg hero-btn">
                    <FiMessageCircle />
                    Start Chatting
                    <FiArrowRight />
                  </Link>
                ) : (
                  <>
                    <Link to="/register" className="btn btn-primary btn-lg hero-btn">
                      Get Started
                      <FiArrowRight />
                    </Link>
                    <Link to="/login" className="btn btn-outline btn-lg hero-btn">
                      Sign In
                    </Link>
                  </>
                )}
              </div>
            </div>
            <div className="hero-visual">
              <div className="hero-chat-preview">
                <div className="chat-bubble bot">
                  <FiMessageCircle className="chat-icon" />
                  <span>Hi! I'm your shopping assistant. How can I help you find the perfect product today?</span>
                </div>
                <div className="chat-bubble user">
                  <span>I'm looking for a laptop for programming</span>
                </div>
                <div className="chat-bubble bot">
                  <span>Great! I found some excellent programming laptops for you...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Why Choose ShopBot?</h2>
            <p className="section-description">
              Discover the powerful features that make shopping smarter and more enjoyable
            </p>
          </div>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card">
                <div className="feature-icon">
                  {feature.icon}
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            {stats.map((stat, index) => (
              <div key={index} className="stat-item">
                <div className="stat-number">{stat.number}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">How It Works</h2>
            <p className="section-description">
              Get started with ShopBot in three simple steps
            </p>
          </div>
          <div className="steps-container">
            <div className="step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Sign Up</h3>
                <p>Create your account and set up your preferences</p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Start Chatting</h3>
                <p>Tell our AI what you're looking for in natural language</p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Find & Shop</h3>
                <p>Discover perfect products and make informed decisions</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">What Our Customers Say</h2>
            <p className="section-description">
              Join thousands of satisfied customers who love shopping with ShopBot
            </p>
          </div>
          <div className="testimonials-grid">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="testimonial-card">
                <div className="testimonial-rating">
                  {Array.from({ length: testimonial.rating }).map((_, i) => (
                    <FiStar key={i} className="star-filled" fill="currentColor" />
                  ))}
                </div>
                <p className="testimonial-content">"{testimonial.content}"</p>
                <div className="testimonial-author">
                  <div className="author-info">
                    <div className="author-name">{testimonial.name}</div>
                    <div className="author-role">{testimonial.role}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2 className="cta-title">Ready to Transform Your Shopping Experience?</h2>
            <p className="cta-description">
              Join ShopBot today and discover a smarter way to shop online
            </p>
            <div className="cta-actions">
              {isAuthenticated ? (
                <Link to="/chat" className="btn btn-primary btn-lg">
                  <FiMessageCircle />
                  Start Shopping Now
                </Link>
              ) : (
                <Link to="/register" className="btn btn-primary btn-lg">
                  Get Started Free
                  <FiArrowRight />
                </Link>
              )}
            </div>
            <div className="cta-features">
              <div className="cta-feature">
                <FiShield />
                <span>Secure & Private</span>
              </div>
              <div className="cta-feature">
                <FiClock />
                <span>24/7 Available</span>
              </div>
              <div className="cta-feature">
                <FiZap />
                <span>Instant Responses</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;