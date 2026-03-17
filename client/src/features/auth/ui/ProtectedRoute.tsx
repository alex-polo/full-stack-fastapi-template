import type { ReactElement } from 'react';
import { Navigate, Outlet } from 'react-router-dom';

export const ProtectedRoute = (): ReactElement => {
  const isAuthenticated = Boolean(localStorage.getItem('token'));

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};
