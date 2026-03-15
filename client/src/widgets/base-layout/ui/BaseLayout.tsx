import { Breadcrumbs } from '@/widgets/breadcrumbs';
import { Box, Container } from '@mui/material';
import { Outlet } from 'react-router-dom';

export const BaseLayout = () => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Container component="main" sx={{ flexGrow: 1, py: 3 }}>
        <Breadcrumbs />
        <Outlet />
      </Container>
    </Box>
  );
};
