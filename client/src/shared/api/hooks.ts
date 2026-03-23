import { useQuery } from '@tanstack/react-query';

export interface SessionData {
  isAuth: boolean;
}

export const useSession = () => {
  return useQuery<SessionData>({
    queryKey: ['session'],
    enabled: false,
  });
};
