import react from '@vitejs/plugin-react';
import path from 'node:path';
import { defineConfig } from 'vite';

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  plugins: [react()],

  // server: {
  //   proxy: {
  //     '/api': 'http://localhost:8085',
  //   },
  //   host: '0.0.0.0',
  //   port: 5173,
  // },
});
