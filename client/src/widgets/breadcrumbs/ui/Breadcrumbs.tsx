import {
  Box,
  Link,
  Breadcrumbs as MuiBreadcrumbs,
  Typography,
} from '@mui/material';
import { Link as RouterLink, useMatches } from 'react-router-dom';

export const Breadcrumbs = () => {
  const matches = useMatches();

  const crumbs = matches
    .filter((match: any) => Boolean(match.handle?.crumb))
    .map((match: any) => match.handle.crumb());

  if (crumbs.length === 0 || (crumbs.length === 1 && crumbs[0].path === '/')) {
    return null;
  }

  return (
    <Box sx={{ mb: 2 }}>
      <MuiBreadcrumbs aria-label="breadcrumb">
        {crumbs.map((crumb, index) => {
          const isLast = index === crumbs.length - 1;

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
