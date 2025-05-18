import {
  useState, useEffect, createContext, useContext
} from 'react';
import jwtDecode from 'jwt-decode';
import api, { setupInterceptors } from './api.js';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refresh'));
  const [user, setUser] = useState(null);

  const setTokens = (t, r) => {
    setToken(t);
    setRefreshToken(r);
    localStorage.setItem('token', t);
    localStorage.setItem('refresh', r);
  };

  useEffect(() => {
    if (token) {
      try {
        const payload = jwtDecode(token);
        setUser({ id: payload.id, role: payload.role });
      } catch (e) {
        logout();
      }
    }
  }, [token]);

  const logout = () => {
    setToken(null);
    setRefreshToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
  };

  setupInterceptors({ token, refreshToken, setTokens, logout });

  return (
    <AuthContext.Provider value={{ token, refreshToken, user, setTokens, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
