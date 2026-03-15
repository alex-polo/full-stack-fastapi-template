import { ProtectedRoute } from '@/features';
import { BaseLayout, DashboardLayout } from '@/widgets';
import { lazy } from 'react';
import { createBrowserRouter } from 'react-router-dom';

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
      { path: '/', element: <HomePage /> },
      { path: '/login', element: <LoginPage /> },
    ],
  },

  // Private pages
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <DashboardLayout />,
        children: [
          { path: '/dashboard', element: <DashboardPage /> },
          // { path: '/settings', element: <SettingsPage /> },
        ],
      },
    ],
  },
]);
