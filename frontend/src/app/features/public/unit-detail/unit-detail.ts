import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';

import { AuthService } from '../../../core/services/auth/auth.service';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-unit-detail',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './unit-detail.html'
})
export class UnitDetailComponent implements OnInit {

  unit: any;
  today: string = new Date().toISOString().split('T')[0];

leaseStart: string = '';
leaseEnd: string = '';

minEndDate: string = this.today;

  constructor(
   private route: ActivatedRoute,
  private api: ApiService,
  private router: Router,
  private auth: AuthService
  ) {}

  ngOnInit() {
  const unitCode = this.route.snapshot.params['unitCode'];
  console.log("Unit code:", unitCode);


  this.api.getUnitDetail(unitCode)
  .subscribe({next: (res) => {
    this.unit = res;
  }});
  this.api.getUnitByCode(unitCode)
    .subscribe({
      next: (data) => {
        console.log("Unit data:", data);
        this.unit = data;
      },
      error: (err) => {
        console.error("Error loading unit:", err);
      }
    });
}


onStartDateChange() {
  this.minEndDate = this.leaseStart;

  if (this.leaseEnd && this.leaseEnd <= this.leaseStart) {
    this.leaseEnd = '';
  }
}

bookUnit() {

  if (!this.auth.isLoggedIn()) {
    localStorage.setItem('redirect_after_login', this.router.url);
    this.router.navigate(['/login']);
    return;
  }

  if (!this.leaseStart || !this.leaseEnd) {
    alert("Please select lease dates");
    return;
  }

  const start = new Date(this.leaseStart);
  const end = new Date(this.leaseEnd);

  const diffTime = end.getTime() - start.getTime();
  const diffDays = diffTime / (1000 * 3600 * 24);

  if (diffDays < 30) {
    alert("Minimum lease duration is 30 days");
    return;
  }

  this.api.bookUnit(this.unit.unit_code, this.leaseStart, this.leaseEnd)
    .subscribe({
      next: () => alert("Booking request sent"),
      error: () => alert("Booking failed")
    });
}



}
