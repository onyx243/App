import { Navigate } from 'react-router-dom';
import { useAuth } from './auth.jsx';

export default function RequireRole({ roles, children }) {
  const { user } = useAuth();
  if (!user || !roles.includes(user.role)) {
    return <Navigate to="/login" />;
  }
  return children;
}
