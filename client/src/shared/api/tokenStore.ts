import { queryClient } from './queryClient';

export class TokenStore {
  private accessToken: string | null = null;

  setAccessToken(token: string) {
    this.accessToken = token;
    queryClient.setQueryData(['session'], { isAuth: true });
  }

  getAccessToken() {
    return this.accessToken;
  }

  removeAccessToken() {
    this.accessToken = null;
    queryClient.setQueryData(['session'], { isAuth: false });
    queryClient.clear();
  }

  hasRefreshToken(): boolean {
    return document.cookie.includes('refresh_token');
  }
}

export const tokenStore = new TokenStore();
