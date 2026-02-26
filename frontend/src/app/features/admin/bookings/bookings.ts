import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { error } from 'console';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './bookings.html'
})
export class AdminBookingsComponent implements OnInit {

  bookings: any[] = [];
  loading = true;
  vacateDates: {[key:number]: string}={};

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

  moveOut(id: number) {
    const date=this.vacateDates[id];

    if(!date){
      alert("Please select a vacate date");
      return;
    }

    this.api.moveOutBooking(id,date).subscribe({
      next: ()=>{
        alert("Booking completed");
        this.loadBookings();
      },
      error: (err) =>{
        alert(err.error?.error || "Moved out failed");
        console.error(err);}
    });
  }



  // cancel(id:number){
  //   if(!confirm("Are you sure you want to cancel this booking?")) return;

  //   this.api.cancelBooking(id).subscribe({
  //     next: ()=>{
  //       alert("Booking cancelled");
  //       this.loadBookings();
  //     },
  //     error: (err) =>{
  //       alert(err.error?.error || "Failed to cancel booking");
  //       console.error(err);
  //     }
  //   });
  // }




  isBeforeLeaseStart(leaseStart: string): boolean{
    const today = new Date();
    const leaseStartDate = new Date(leaseStart);
    return today<leaseStartDate;
  }
}
