import { useSession } from '@/shared/api';
import { ROUTE_PATHS } from '@/shared/config';
import type { ReactElement } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';

export const ProtectedRoute = (): ReactElement => {
  const location = useLocation();
  const { data: session } = useSession();

  const isAuth = session?.isAuth;

  if (!isAuth) {
    return (
      <Navigate to={ROUTE_PATHS.LOGIN} state={{ from: location }} replace />
    );
  }

  return <Outlet />;
};
