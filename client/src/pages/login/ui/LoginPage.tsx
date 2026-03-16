import { zodResolver } from '@hookform/resolvers/zod';
import { Box, Button, TextField, Typography } from '@mui/material';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

const loginSchema = z.object({
  email: z.email('Введите корректный email'),

  password: z
    .string()
    .min(6, { error: 'Пароль должен быть не менее 6 символов' }),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export const LoginPage = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    mode: 'onBlur',
  });

  const onSubmit = (data: LoginFormValues) => {
    console.log('Данные готовы для FastAPI:', data);
    // TODO: mutate login
  };

  return (
    <>
      <Typography
        variant="h5"
        align="center"
        gutterBottom
        sx={{ fontWeight: 700 }}
      >
        Вход
      </Typography>

      <Box
        component="form"
        onSubmit={handleSubmit(onSubmit)}
        noValidate
        sx={{ mt: 2, width: '100%' }}
      >
        <TextField
          {...register('email')}
          label="Email"
          fullWidth
          margin="normal"
          error={!!errors.email}
          helperText={errors.email?.message}
          disabled={isSubmitting}
        />

        <TextField
          {...register('password')}
          label="Пароль"
          type="password"
          fullWidth
          margin="normal"
          error={!!errors.password}
          helperText={errors.password?.message}
          disabled={isSubmitting}
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          size="large"
          disabled={isSubmitting}
          sx={{ mt: 3, mb: 2, py: 1.5, borderRadius: 2 }}
        >
          {isSubmitting ? 'Вход...' : 'Войти'}
        </Button>
      </Box>
    </>
  );
};
