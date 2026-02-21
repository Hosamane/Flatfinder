import { Component, OnInit, DoCheck } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { FilterService } from '../../../core/services/filter/filter.service';

@Component({
  selector: 'app-unit-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './unit-list.html'
})



export class UnitListComponent implements OnInit,DoCheck {
  
  units: any[] = [];
  filteredUnits: any[] = [];
loading: boolean = true;
  towerCode!: string;
  moveInDate: string = '';

  // Filters
  // sortOption: string = '';
  // selectedType: string = '';
  // selectedFurnishing: string = '';
  // selectedParking: string = '';
  // minRent: number | null = null;
  // maxRent: number | null = null;
  
  
  constructor(
    private route: ActivatedRoute,
    private api: ApiService,
    private router: Router,
    public filter: FilterService
  ) {}
ngDoCheck() {
  this.applyFilters();
}

  ngOnInit() {
    this.towerCode = this.route.snapshot.params['code'];
    this.moveInDate = new Date().toISOString().split('T')[0];
    this.loadUnits();
  }

  // loadUnits() {
  //   this.api.getUnitsByTower(this.towerCode, this.moveInDate)
  //     .subscribe(data => {
  //       this.units = data as any[];
  //       this.applyFilters();
  //     });
  // }

loadUnits() {
  this.loading = true;

  this.api.getUnitsByTower(
    this.towerCode,
    this.filter.moveInDate
  ).subscribe(data => {
    this.units = data as any[];
    this.applyFilters();
    this.loading = false;
  });
}

applyFilters() {
  let tempUnits = [...this.units];

  if (this.filter.selectedType) {
    tempUnits = tempUnits.filter(u =>
      u.flat_type === this.filter.selectedType
    );
  }

  if (this.filter.selectedFurnishing) {
    tempUnits = tempUnits.filter(u =>
      u.furnishing === this.filter.selectedFurnishing
    );
  }

  if (this.filter.selectedParking) {
    const needsParking = this.filter.selectedParking === 'yes';
    tempUnits = tempUnits.filter(u =>
      u.parking === needsParking
    );
  }

  if (this.filter.minRent !== null) {
    tempUnits = tempUnits.filter(u =>
      Number(u.rent) >= this.filter.minRent!
    );
  }

  if (this.filter.maxRent !== null) {
    tempUnits = tempUnits.filter(u =>
      Number(u.rent) <= this.filter.maxRent!
    );
  }

  if (this.filter.sortOption === 'rentLow') {
    tempUnits.sort((a, b) => Number(a.rent) - Number(b.rent));
  } else if (this.filter.sortOption === 'rentHigh') {
    tempUnits.sort((a, b) => Number(b.rent) - Number(a.rent));
  }

  this.filteredUnits = tempUnits;
}


  // 🔥 Sorting logic
      goToUnit(code: string) {
        this.router.navigate(['/unit', code]);
      }
  
}


