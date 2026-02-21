import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private platformId = inject(PLATFORM_ID);

  private isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }

  isLoggedIn(): boolean {
    if (this.isBrowser()) {
      return !!localStorage.getItem('access_token');
    }
    return false;
  }

  getToken(): string | null {
    if (this.isBrowser()) {
      return localStorage.getItem('access_token');
    }
    return null;
  }

  login(token: string) {
    if (this.isBrowser()) {
      localStorage.setItem('access_token', token);
    }
  }

  logout() {
    if (this.isBrowser()) {
      localStorage.removeItem('access_token');
    }
  }
}