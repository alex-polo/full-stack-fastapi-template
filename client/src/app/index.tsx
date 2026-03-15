import { router } from '@/app/providers';
import { theme } from '@/shared/config';
import { BreadcrumbsProvider } from '@/shared/lib';
import { GlobalLoader } from '@/shared/ui/loaders';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { Suspense } from 'react';
import { RouterProvider } from 'react-router-dom';

export const App = () => {
  return (
    <BreadcrumbsProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Suspense fallback={<GlobalLoader />}>
          <RouterProvider router={router} />
        </Suspense>
      </ThemeProvider>
    </BreadcrumbsProvider>
  );
};
