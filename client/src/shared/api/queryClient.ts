import { ROUTE_PATHS } from '@/shared/config';
import { MutationCache, QueryCache, QueryClient } from '@tanstack/react-query';
import { isAxiosError } from 'axios';

const handleApiError = (error: unknown) => {
  // Check if the error is a standard Axios error
  if (isAxiosError(error)) {
    const status = error.response?.status;

    // Handle session expiration (401) or insufficient permissions (403)
    if (status === 401 || status === 403) {
      console.warn('Session expired or access denied. Redirecting to login...');

      // Clear authentication artifacts from local storage
      localStorage.removeItem('token');

      // Perform a full redirect to the login page to reset the app state
      if (typeof window !== 'undefined') {
        window.location.href = ROUTE_PATHS.LOGIN;
      }
    }

    // Log the API error details for debugging (status and response body)
    console.error(`[API Error] ${status}:`, error.response?.data);
  } else {
    // Handle non-Axios or unexpected errors
    console.error('[Unknown Error]:', error);
  }
};

export const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: handleApiError,
  }),
  mutationCache: new MutationCache({
    onError: handleApiError,
  }),
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 1 * 60 * 1000,
    },
  },
});
