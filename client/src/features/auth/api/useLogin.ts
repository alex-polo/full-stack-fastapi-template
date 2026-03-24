import { $api, API_ENDPOINTS, tokenStore } from '@/shared/api';
import { ROUTE_PATHS } from '@/shared/config';
import { notify } from '@/shared/lib';
import { useMutation } from '@tanstack/react-query';
import { useLocation, useNavigate } from 'react-router-dom';
import type { LoginFormValues } from '../model/types';

export const useLogin = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || ROUTE_PATHS.DASHBOARD;

  return useMutation({
    mutationFn: async (data: LoginFormValues) => {
      const params = new URLSearchParams();
      params.append('username', data.username);
      params.append('password', data.password);

      const response = await $api.post(API_ENDPOINTS.AUTH.LOGIN, params, {
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
      const message =
        error.response?.data?.detail || 'Неверный логин или пароль';
      notify.error(
        message === 'LOGIN_BAD_CREDENTIALS'
          ? 'Неверный логин или пароль'
          : message
      );
      console.log(error);
    },
  });
};
