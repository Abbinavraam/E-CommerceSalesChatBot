import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useChat } from '../contexts/ChatContext';
import { 
  FiUser, 
  FiMail, 
  FiEdit3, 
  FiSave, 
  FiX,
  FiMessageCircle,
  FiShoppingBag,
  FiClock,
  FiSettings,
  FiLogOut
} from 'react-icons/fi';
import LoadingSpinner from '../components/UI/LoadingSpinner';
import { toast } from 'react-toastify';
import './Profile.css';

const Profile = () => {
  const { user, updateProfile, logout } = useAuth();
  const { sessions } = useChat();
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    bio: ''
  });

  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username || '',
        email: user.email || '',
        firstName: user.first_name || '',
        lastName: user.last_name || '',
        bio: user.bio || ''
      });
    }
  }, [user]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      const result = await updateProfile({
        first_name: formData.firstName,
        last_name: formData.lastName,
        bio: formData.bio
      });

      if (result.success) {
        setIsEditing(false);
        toast.success('Profile updated successfully!');
      }
    } catch (error) {
      console.error('Failed to update profile:', error);
      toast.error('Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      username: user.username || '',
      email: user.email || '',
      firstName: user.first_name || '',
      lastName: user.last_name || '',
      bio: user.bio || ''
    });
    setIsEditing(false);
  };

  const handleLogout = () => {
    logout();
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getInitials = (username) => {
    return username ? username.substring(0, 2).toUpperCase() : 'U';
  };

  const activeSessions = sessions.filter(session => session.is_active);
  const totalSessions = sessions.length;

  return (
    <div className="profile-page">
      <div className="container">
        <div className="profile-container">
          {/* Profile Header */}
          <div className="profile-header">
            <div className="profile-avatar">
              <div className="avatar-circle">
                {user?.avatar_url ? (
                  <img src={user.avatar_url} alt="Profile" />
                ) : (
                  <span className="avatar-initials">
                    {getInitials(user?.username)}
                  </span>
                )}
              </div>
            </div>
            
            <div className="profile-info">
              <h1 className="profile-name">
                {user?.first_name && user?.last_name 
                  ? `${user.first_name} ${user.last_name}`
                  : user?.username
                }
              </h1>
              <p className="profile-username">@{user?.username}</p>
              <p className="profile-email">{user?.email}</p>
              {user?.created_at && (
                <p className="profile-joined">
                  Member since {formatDate(user.created_at)}
                </p>
              )}
            </div>

            <div className="profile-actions">
              {!isEditing ? (
                <button 
                  className="btn btn-primary"
                  onClick={() => setIsEditing(true)}
                >
                  <FiEdit3 />
                  Edit Profile
                </button>
              ) : (
                <div className="edit-actions">
                  <button 
                    className="btn btn-primary"
                    onClick={handleSave}
                    disabled={isLoading}
                  >
                    {isLoading ? <LoadingSpinner size="small" /> : <FiSave />}
                    Save
                  </button>
                  <button 
                    className="btn btn-outline"
                    onClick={handleCancel}
                    disabled={isLoading}
                  >
                    <FiX />
                    Cancel
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="profile-content">
            {/* Profile Details */}
            <div className="profile-section">
              <div className="section-header">
                <h2>Profile Details</h2>
              </div>
              
              <div className="profile-form">
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Username</label>
                    <div className="input-group">
                      <FiUser className="input-icon" />
                      <input
                        type="text"
                        name="username"
                        value={formData.username}
                        className="form-input"
                        disabled={true}
                        placeholder="Username"
                      />
                    </div>
                    <small className="form-help">Username cannot be changed</small>
                  </div>

                  <div className="form-group">
                    <label className="form-label">Email</label>
                    <div className="input-group">
                      <FiMail className="input-icon" />
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        className="form-input"
                        disabled={true}
                        placeholder="Email address"
                      />
                    </div>
                    <small className="form-help">Email cannot be changed</small>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">First Name</label>
                    <input
                      type="text"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleInputChange}
                      className="form-input"
                      disabled={!isEditing}
                      placeholder="Enter your first name"
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Last Name</label>
                    <input
                      type="text"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleInputChange}
                      className="form-input"
                      disabled={!isEditing}
                      placeholder="Enter your last name"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Bio</label>
                  <textarea
                    name="bio"
                    value={formData.bio}
                    onChange={handleInputChange}
                    className="form-textarea"
                    disabled={!isEditing}
                    placeholder="Tell us about yourself..."
                    rows={4}
                  />
                </div>
              </div>
            </div>

            {/* Activity Stats */}
            <div className="profile-section">
              <div className="section-header">
                <h2>Activity Overview</h2>
              </div>
              
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-icon">
                    <FiMessageCircle />
                  </div>
                  <div className="stat-content">
                    <div className="stat-number">{totalSessions}</div>
                    <div className="stat-label">Total Chat Sessions</div>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-icon">
                    <FiClock />
                  </div>
                  <div className="stat-content">
                    <div className="stat-number">{activeSessions.length}</div>
                    <div className="stat-label">Active Sessions</div>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-icon">
                    <FiShoppingBag />
                  </div>
                  <div className="stat-content">
                    <div className="stat-number">0</div>
                    <div className="stat-label">Products Viewed</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Sessions */}
            <div className="profile-section">
              <div className="section-header">
                <h2>Recent Chat Sessions</h2>
              </div>
              
              {sessions.length === 0 ? (
                <div className="empty-state">
                  <FiMessageCircle size={48} />
                  <h3>No chat sessions yet</h3>
                  <p>Start chatting with our AI assistant to see your session history here.</p>
                </div>
              ) : (
                <div className="sessions-list">
                  {sessions.slice(0, 5).map((session) => (
                    <div key={session.session_id} className="session-item">
                      <div className="session-info">
                        <div className="session-title">
                          Chat Session
                        </div>
                        <div className="session-date">
                          {formatDate(session.started_at)}
                        </div>
                      </div>
                      <div className="session-status">
                        <span className={`status-badge ${session.is_active ? 'active' : 'inactive'}`}>
                          {session.is_active ? 'Active' : 'Completed'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Account Settings */}
            <div className="profile-section">
              <div className="section-header">
                <h2>Account Settings</h2>
              </div>
              
              <div className="settings-list">
                <div className="setting-item">
                  <div className="setting-info">
                    <FiSettings className="setting-icon" />
                    <div>
                      <div className="setting-title">Account Preferences</div>
                      <div className="setting-description">Manage your account settings and preferences</div>
                    </div>
                  </div>
                  <button className="btn btn-outline btn-sm">
                    Configure
                  </button>
                </div>

                <div className="setting-item danger">
                  <div className="setting-info">
                    <FiLogOut className="setting-icon" />
                    <div>
                      <div className="setting-title">Sign Out</div>
                      <div className="setting-description">Sign out of your account</div>
                    </div>
                  </div>
                  <button 
                    className="btn btn-danger btn-sm"
                    onClick={handleLogout}
                  >
                    Sign Out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;