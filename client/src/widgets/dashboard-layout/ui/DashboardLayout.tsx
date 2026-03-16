import { ROUTE_PATHS } from '@/shared/config';
import { Footer } from '@/widgets';
import {
  Dashboard as DashIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { Box } from '@mui/material';
import { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { DashboardNavbar } from './DashboardNavbar';
import { DashboardSidebar } from './DashboardSidebar';

const DRAWER_WIDTH = 240;

export const DashboardLayout = () => {
  const [open, setOpen] = useState(true);
  const navigate = useNavigate();

  const navItems = [
    { text: 'Dashboard', icon: <DashIcon />, path: ROUTE_PATHS.DASHBOARD },
    { text: 'Profile', icon: <PersonIcon />, path: '/app/profile' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/app/settings' },
  ];

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <DashboardNavbar
        onToggleDrawer={() => setOpen(!open)}
        onLogout={() => navigate(ROUTE_PATHS.HOME)}
      />

      <DashboardSidebar
        open={open}
        onClose={() => setOpen(false)}
        items={navItems}
        width={DRAWER_WIDTH}
      />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          minHeight: 'calc(100vh - 64px)',
          marginTop: '64px',
          width: { sm: open ? `calc(100% - ${DRAWER_WIDTH}px)` : '100%' },
          maxWidth: '100%',
          overflowX: 'hidden',
          transition: theme => theme.transitions.create(['width', 'margin']),
          backgroundColor: 'background.default',
        }}
      >
        <Box sx={{ p: 3, flexGrow: 1 }}>
          <Outlet />
        </Box>
        <Footer />
      </Box>
    </Box>
  );
};
