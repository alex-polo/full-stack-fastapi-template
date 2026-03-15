import { BaseLayout } from '@/app/layouts/base-layout';
import { lazy } from 'react';
import { createBrowserRouter } from 'react-router-dom';

const HomePage = lazy(() =>
  import('@/pages/home').then(module => ({ default: module.HomePage }))
);

const DashboardPage = lazy(() =>
  import('@/pages/dashboard').then(module => ({
    default: module.DashboardPage,
  }))
);

export const router = createBrowserRouter([
  {
    path: '/',
    element: <BaseLayout />,
    children: [
      {
        path: '/',
        element: <HomePage />,
      },
      {
        path: '/dashboard',
        element: <DashboardPage />,
      },
    ],
  },
]);
