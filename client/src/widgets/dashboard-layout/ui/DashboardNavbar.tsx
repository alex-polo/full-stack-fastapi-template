import { SITE_CONFIG } from '@/shared/config';
import { ThemeToggleButton } from '@/shared/ui';
import { Logout as LogoutIcon, Menu as MenuIcon } from '@mui/icons-material';
import {
  AppBar,
  Box,
  Button,
  IconButton,
  Toolbar,
  Typography,
} from '@mui/material';

interface NavbarProps {
  onToggleDrawer: () => void;
  onLogout: () => void;
}

export const DashboardNavbar = ({ onToggleDrawer, onLogout }: NavbarProps) => (
  <AppBar
    position="fixed"
    sx={{
      zIndex: theme => theme.zIndex.drawer + 1,
      boxShadow: theme => theme.shadows[4],
    }}
  >
    <Toolbar>
      <IconButton
        color="inherit"
        edge="start"
        onClick={onToggleDrawer}
        sx={{ mr: 2 }}
      >
        <MenuIcon />
      </IconButton>
      <Typography variant="h6" noWrap sx={{ flexGrow: 1, fontWeight: 700 }}>
        {SITE_CONFIG.NAME}
      </Typography>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <ThemeToggleButton />
        <Button
          color="inherit"
          startIcon={<LogoutIcon />}
          onClick={onLogout}
          sx={{ textTransform: 'none' }}
        >
          Выход
        </Button>
      </Box>
    </Toolbar>
  </AppBar>
);
