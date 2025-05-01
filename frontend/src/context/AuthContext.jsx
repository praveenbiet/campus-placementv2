import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// Configure axios defaults
const api = axios.create({
  baseURL: 'http://localhost:5000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  }
});

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [userType, setUserType] = useState(null);

  useEffect(() => {
    const studentToken = localStorage.getItem('studentToken');
    const adminToken = localStorage.getItem('adminToken');
    
    if (studentToken) {
      setUserType('student');
      api.defaults.headers.common['Authorization'] = `Bearer ${studentToken}`;
      fetchUserProfile('student');
    } else if (adminToken) {
      setUserType('admin');
      api.defaults.headers.common['Authorization'] = `Bearer ${adminToken}`;
      fetchUserProfile('admin');
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserProfile = async (type) => {
    try {
      const endpoint = type === 'student' 
        ? '/api/student/profile'
        : '/api/admin/profile';
      
      const response = await api.get(endpoint);
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user profile:', error);
      handleLogout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials, type) => {
    try {
      const endpoint = type === 'student'
        ? '/api/auth/student/login'
        : '/api/auth/admin/login';
      
      const response = await api.post(endpoint, credentials);
      const { token } = response.data;
      
      if (type === 'student') {
        localStorage.setItem('studentToken', token);
      } else {
        localStorage.setItem('adminToken', token);
      }
      
      setUserType(type);
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      await fetchUserProfile(type);
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('studentToken');
    localStorage.removeItem('adminToken');
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
    setUserType(null);
  };

  const value = {
    user,
    userType,
    loading,
    login,
    logout: handleLogout,
    api,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 