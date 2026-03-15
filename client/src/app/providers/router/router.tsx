import { ProtectedRoute } from '@/features';
import { ROUTE_PATHS } from '@/shared/config';
import { AuthLayout, BaseLayout, DashboardLayout } from '@/widgets';
import { lazy } from 'react';
import { createBrowserRouter } from 'react-router-dom';

const NotFoundPage = lazy(() =>
  import('@/pages/not-found').then(m => ({ default: m.NotFoundPage }))
);

const HomePage = lazy(() =>
  import('@/pages/home').then(module => ({ default: module.HomePage }))
);

const LoginPage = lazy(() =>
  import('@/pages/login').then(module => ({ default: module.LoginPage }))
);
const DashboardPage = lazy(() =>
  import('@/pages/dashboard').then(module => ({
    default: module.DashboardPage,
  }))
);

export const router = createBrowserRouter([
  // Public pages
  {
    element: <BaseLayout />,
    children: [
      {
        path: '/',
        element: <HomePage />,
        handle: { crumb: () => ({ label: 'Главная', path: ROUTE_PATHS.HOME }) },
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
  // Auth pages
  {
    element: <AuthLayout />,
    children: [
      {
        path: ROUTE_PATHS.LOGIN,
        element: <LoginPage />,
      },
    ],
  },

  // Private pages
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <DashboardLayout />,
        children: [
          { path: ROUTE_PATHS.DASHBOARD, element: <DashboardPage /> },
          // { path: '/settings', element: <SettingsPage /> },
        ],
      },
    ],
  },
]);
