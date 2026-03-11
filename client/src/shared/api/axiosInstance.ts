import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || '/api';

/**
 * Public API client for requests without authorization.
 * Used for: login, register, forgot-password, etc.
 */
export const publicApiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// TODO: Add privateApiClient with authorization interceptor
