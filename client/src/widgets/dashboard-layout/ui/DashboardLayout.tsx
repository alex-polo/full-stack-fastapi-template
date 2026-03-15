import { Box, Toolbar } from '@mui/material';
import { Outlet } from 'react-router-dom';

export const DashboardLayout = () => {
  return (
    <Box sx={{ display: 'flex' }}>
      {/* Здесь будет виджет Sidebar */}
      <Box component="nav" sx={{ width: 240, flexShrink: 0 }}>
        {/* Заглушка сайдбара */}
      </Box>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar /> {/* Отступ под Header, если он фиксированный */}
        <Outlet />
      </Box>
    </Box>
  );
};
