import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html'
})
export class DashboardComponent implements OnInit {

  data: any = {};

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getAdminDashboard().subscribe(res => {
      this.data = res;
    });
  }

}