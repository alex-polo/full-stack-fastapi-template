// import { queryClient } from './queryClient';

export class TokenStore {
  private accessToken: string | null = null;
  private onTokenChange: ((token: string | null) => void) | null = null;

  setAccessToken(token: string) {
    this.accessToken = token;
    // queryClient.setQueryData(['session'], { isAuth: true });
    this.onTokenChange?.(token);
  }

  getAccessToken() {
    return this.accessToken;
  }

  removeAccessToken() {
    this.accessToken = null;
    // queryClient.setQueryData(['session'], { isAuth: false });
    // queryClient.clear();
    this.onTokenChange?.(null);
  }

  hasRefreshToken(): boolean {
    return document.cookie.includes('refresh_token');
  }

  subscribe(callback: (token: string | null) => void) {
    this.onTokenChange = callback;
  }
}

export const tokenStore = new TokenStore();
