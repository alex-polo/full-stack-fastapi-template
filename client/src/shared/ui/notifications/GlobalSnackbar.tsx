import { notify } from '@/shared/lib';
import { Alert, Snackbar } from '@mui/material';
import { useEffect, useState } from 'react';

export const GlobalSnackbar = () => {
  const [state, setState] = useState({
    open: false,
    message: '',
    severity: 'info' as any,
  });

  useEffect(() => {
    return notify.subscribe(({ message, severity }) => {
      setState({ open: true, message, severity });
    });
  }, []);

  const handleClose = () => setState(prev => ({ ...prev, open: false }));

  return (
    <Snackbar
      open={state.open}
      autoHideDuration={4000}
      onClose={handleClose}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
    >
      <Alert onClose={handleClose} severity={state.severity} variant="filled">
        {state.message}
      </Alert>
    </Snackbar>
  );
};
