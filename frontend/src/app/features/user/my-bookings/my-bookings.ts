// import { Component, OnInit } from '@angular/core';
// import { ApiService } from '../../../core/service/api.service';
// import { CommonModule } from '@angular/common';
// import { FormsModule } from '@angular/forms';
// import { RouterLink } from '@angular/router';

// @Component({
//   standalone: true,
//   imports: [CommonModule,FormsModule],
//   templateUrl: './my-bookings.html'
// })
// export class MyBookingsComponent implements OnInit {
// loading: boolean = true;

//   bookings: any[] = [];

//   constructor(private api: ApiService) {}

//   ngOnInit() {
//     this.api.getMyBookings().subscribe({
//       next: (data: any) => {
//         this.bookings = data;
//         this.loading = false;
//       },
//       error: () => {
//         alert("Failed to load bookings");
//         this.loading = false;
//       }
//     });
//   }
// }



import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './my-bookings.html'
})
export class MyBookingsComponent implements OnInit {

  loading: boolean = true;
  bookings: any[] = [];
  errorMessage: string = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getMyBookings().subscribe({
      next: (data: any) => {
        this.bookings = data;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = "Failed to load bookings";
        this.loading = false;
      }
    });
  }
}