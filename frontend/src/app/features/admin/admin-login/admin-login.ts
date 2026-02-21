import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ApiService } from '../../../core/service/api.service';
import { AuthService } from '../../../core/services/auth/auth.service';
@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-login.html'
})
export class AdminLoginComponent {

  email = '';
  password = '';
  loading = false;

  constructor(
    private api: ApiService,
    private auth: AuthService,
    private router: Router
  ) {}

  login() {
    this.loading = true;

    this.api.login(this.email, this.password)
      .subscribe({
        next: (res: any) => {

          if (res.role !== 'ADMIN') {
            alert("Access denied. Not an admin.");
            this.loading = false;
            return;
          }

          this.auth.login(res.access_token);
          this.router.navigate(['/admin/dashboard']);
        },
        error: () => {
          alert("Invalid credentials");
          this.loading = false;
        }
      });
  }
}
