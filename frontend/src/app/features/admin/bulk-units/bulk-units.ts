import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './bulk-units.html',
  styleUrls: ['./bulk-units.css']
})
export class AdminBulkUnitsComponent implements OnInit {

  towers: any[] = [];
  selectedTower = '';

  form: any = {
    wing: '',
    floor_number: '',
    start_flat: '',
    end_flat: '',
    rent: '',
    available_from: '',
    flat_type: '',
    furnishing: '',
    balcony_type: '',
    parking: false,
    facing_direction: '',
    is_active: true
  };

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getTowers().subscribe((data: any) => {
      this.towers = data;
    });
  }

  createBulk() {

    if (!this.selectedTower) {
      alert("Select tower first");
      return;
    }

    this.api.bulkCreateUnits(this.selectedTower, this.form)
      .subscribe({
        next: () => {
          alert("Units created successfully");
        },
        error: (err) => {
          console.error(err);
          alert("Bulk creation failed");
        }
      });
  }
}
