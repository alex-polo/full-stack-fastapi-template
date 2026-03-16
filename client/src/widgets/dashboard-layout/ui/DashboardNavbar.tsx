import { ROUTE_PATHS, SITE_CONFIG } from '@/shared/config';
import { ThemeToggleButton } from '@/shared/ui';
import { Logout as LogoutIcon, Menu as MenuIcon } from '@mui/icons-material';
import { AppBar, Box, Button, IconButton, Toolbar } from '@mui/material';
// Импортируем твои логотипы
import { HeaderLogoDesktop, HeaderLogoMobile } from '@/shared/ui/logo';

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

      {/* Вставляем логотип вместо обычного Typography */}
      <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
        <HeaderLogoDesktop
          headerLogoText={SITE_CONFIG.NAME}
          href={ROUTE_PATHS.DASHBOARD} // В дашборде лого ведет на главную дашборда
        />
        <HeaderLogoMobile
          headerLogoText={SITE_CONFIG.SHORT_NAME}
          href={ROUTE_PATHS.DASHBOARD}
        />
      </Box>

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
