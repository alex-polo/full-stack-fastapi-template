import { ROUTE_PATHS } from '@/shared/config';
import { MutationCache, QueryCache, QueryClient } from '@tanstack/react-query';
import { isAxiosError } from 'axios';
import { tokenStore } from './tokenStore';

const handleApiError = (error: unknown) => {
  if (isAxiosError(error)) {
    const status = error.response?.status;

    if (status === 401) {
      console.warn('Session expired or access denied. Redirecting to login...');

      if (typeof window !== 'undefined') {
        window.location.href = ROUTE_PATHS.LOGIN;
      }
    }

    console.error(`[API Error] ${status}:`, error.response?.data);
  } else {
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
      retry: (failureCount, error: any) => {
        if (error?.response?.status === 401) return false;
        return failureCount < 2;
      },
      refetchOnWindowFocus: false,
      staleTime: 1 * 60 * 1000,
    },
  },
});

queryClient.setQueryData(['session'], {
  isAuth: !!tokenStore.getAccessToken(),
});
