import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ApiService } from '../../../core/service/api.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './register.html'
})
export class RegisterComponent {

  name: string = '';
  email: string = '';
  password: string = '';
  loading: boolean = false;

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  register() {
    this.loading = true;

    this.api.register(this.name, this.email, this.password)
      .subscribe({
        next: () => {
          alert("Registration successful. Please login.");
          this.router.navigate(['/login']);
        },
        error: () => {
          alert("Registration failed");
          this.loading = false;
        }
      });
  }
}
