import axios from 'axios';
import { useAuth } from './auth.jsx';

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const useApi = () => {
  const { token } = useAuth();
  instance.defaults.headers.Authorization = token ? `Bearer ${token}` : '';
  return instance;
};

export default instance;
