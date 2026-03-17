export class TokenStore {
  private accessToken: string | null = null;

  setAccessToken(token: string) {
    this.accessToken = token;
  }

  getAccessToken() {
    return this.accessToken;
  }

  removeAccessToken() {
    this.accessToken = null;
  }

  hasRefreshToken(): boolean {
    return document.cookie.includes('refresh_token');
  }
}

export const tokenStore = new TokenStore();
