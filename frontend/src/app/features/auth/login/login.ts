import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../../core/service/api.service';
import { AuthService } from '../../../core/services/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule,RouterLink],
  templateUrl: './login.html'
})
export class LoginComponent {

  email: string = '';
  password: string = '';
  loading: boolean = false;

  constructor(
    private api: ApiService,
    private auth: AuthService,
    private router: Router
  ) {}

  login() {
    this.loading = true;

    this.api.login(this.email, this.password)
      .subscribe({
        next: (response: any) => {

          this.auth.login(response.access_token);

          const redirectUrl = localStorage.getItem('redirect_after_login');

          if (redirectUrl) {
            localStorage.removeItem('redirect_after_login');
            this.router.navigateByUrl(redirectUrl);
          } else {
            this.router.navigate(['/']);
          }

        },
        error: () => {
          alert("Invalid credentials");
          this.loading = false;
        }
      });
  }
}
