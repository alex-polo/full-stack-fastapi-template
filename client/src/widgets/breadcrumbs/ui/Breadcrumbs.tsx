import { useBreadcrumbs } from '@/shared/lib';
import {
  Box,
  Link,
  Breadcrumbs as MuiBreadcrumbs,
  Typography,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

export const Breadcrumbs = () => {
  const { breadcrumbs } = useBreadcrumbs();

  if (breadcrumbs.length === 0) return null;

  return (
    <Box sx={{ mb: 2 }}>
      <MuiBreadcrumbs aria-label="breadcrumb">
        {breadcrumbs.map((crumb, index) => {
          const isLast = index === breadcrumbs.length - 1;

          return isLast ? (
            <Typography key={crumb.path} color="text.primary">
              {crumb.label}
            </Typography>
          ) : (
            <Link
              key={crumb.path}
              component={RouterLink}
              underline="hover"
              color="inherit"
              to={crumb.path}
            >
              {crumb.label}
            </Link>
          );
        })}
      </MuiBreadcrumbs>
    </Box>
  );
};
