import { $api, API_ENDPOINTS, tokenStore } from '@/shared/api';
import { ROUTE_PATHS } from '@/shared/config';
import { useMutation } from '@tanstack/react-query';
import { useLocation, useNavigate } from 'react-router-dom';
import type { LoginFormValues } from '../model/types';

export const useLogin = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || ROUTE_PATHS.DASHBOARD;

  return useMutation({
    mutationFn: async (data: LoginFormValues) => {
      const response = await $api.post(API_ENDPOINTS.AUTH.LOGIN, data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      return response.data;
    },
    onSuccess: data => {
      tokenStore.setAccessToken(data.access_token);

      navigate(from, { replace: true });
    },
    onError: (error: any) => {
      // Show error message into toast
      console.error('Login failed:', error.response?.data);
    },
  });
};
