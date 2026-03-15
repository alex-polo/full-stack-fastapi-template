import { Breadcrumbs } from '@/widgets/breadcrumbs';
import { Box, Container } from '@mui/material';
import { Outlet } from 'react-router-dom';

export const BaseLayout = () => {
  return (
    <Box
    // sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}
    >
      {/* Здесь может быть Header */}
      <Container
        component="main"
        // sx={{ flexGrow: 1, py: 3 }}
      >
        <Breadcrumbs /> {/* Виджет всегда над контентом */}
        <Outlet />
        {/* Сюда будут подставляться твои страницы (Home, Dashboard) */}
      </Container>
      {/* Здесь может быть Footer */}
    </Box>
  );
};
