import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',

    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  colorSchemes: {
    dark: true,
  },
});
