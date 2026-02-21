import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  imports: [CommonModule],
  templateUrl: './bookings.html'
})
export class AdminBookingsComponent implements OnInit {

  bookings: any[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadBookings();
  }

 loadBookings() {
  this.api.getAllBookings().subscribe({
    next: (data: any) => {
      console.log("BOOKINGS DATA:", data);  // 🔥 ADD THIS
      this.bookings = data;
      this.loading = false;
    },
    error: (err) => {
      console.error("ERROR:", err);
      alert("Failed to load bookings");
      this.loading = false;
    }
  });
}


  updateStatus(id: number, status: string) {
    this.api.updateBookingStatus(id, status)
      .subscribe(() => {
        this.loadBookings();
      });
  }
}
