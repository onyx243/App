import axios from 'axios';
import toast from 'react-hot-toast';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const setupInterceptors = (store) => {
  api.interceptors.request.use((config) => {
    if (store.token) config.headers.Authorization = `Bearer ${store.token}`;
    return config;
  });

  let refreshing = null;
  api.interceptors.response.use(
    (r) => r,
    async (error) => {
      const { config, response } = error;
      if (response && response.status === 401 && store.refreshToken && !config._retry) {
        if (!refreshing) {
          refreshing = api.post('/auth/refresh', { refresh_token: store.refreshToken })
            .then(({ data }) => {
              store.setTokens(data.access_token, data.refresh_token);
            })
            .catch(() => { store.logout(); })
            .finally(() => { refreshing = null; });
        }
        await refreshing;
        config._retry = true;
        return api(config);
      }
      toast.error(response?.data?.detail || 'Error');
      throw error;
    },
  );
};

export default api;
