import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const ProtectedRoute = ({ children, requiredUserType }) => {
  const { user, userType, loading } = useAuth();
  const navigate = useNavigate();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user || userType !== requiredUserType) {
    return <Navigate to={requiredUserType === 'admin' ? '/admin/login' : '/student/login'} replace />;
  }

  return children;
};

export default ProtectedRoute; 