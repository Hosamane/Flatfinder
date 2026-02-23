// import { Component, OnInit } from '@angular/core';
// import { RouterLink, RouterOutlet,Router } from '@angular/router';
// import { CommonModule } from '@angular/common';
// import { FormsModule } from '@angular/forms';
// import { FilterService } from '../../../core/services/filter/filter.service';
// import { AuthService } from '../../../core/services/auth/auth.service';
// import { ApiService } from '../../../core/service/api.service';
// // import { Route } from '@angular/router';
// @Component({
//   selector: 'app-public-layout',
//   standalone: true,
//   imports: [CommonModule, FormsModule, RouterOutlet, RouterLink],
//   templateUrl: './layout.html'
// })
// export class LayoutComponent implements OnInit{

 


//   localities: string[] = [];
//   constructor(public filter: FilterService,
//     public auth: AuthService,
//     private router: Router,
//     private api:ApiService
//   ) {}


//   ngOnInit(): void {
//     this.api.getTowers().subscribe(data=>{
//       const unique = [...new Set(data.map((t:any)=> t.locality))];
//       this.localities = unique;
//     })
//   }
//   resetFilters() {
//     this.filter.moveInDate = new Date().toISOString().split('T')[0];
//     this.filter.selectedType = '';
//     this.filter.selectedFurnishing = '';
//     this.filter.selectedParking = '';
//     this.filter.minRent = null;
//     this.filter.maxRent = null;
//     this.filter.sortOption = '';
//     this.filter.selectedLocality = '';
//   }

//    logout() {
//     this.auth.logout();
//     this.router.navigate(['/']);
//   }

// }



import { Component, OnInit } from '@angular/core';
import { RouterLink, RouterOutlet, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FilterService } from '../../../core/services/filter/filter.service';
import { AuthService } from '../../../core/services/auth/auth.service';
import { ApiService } from '../../../core/service/api.service';

@Component({
  selector: 'app-public-layout',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterOutlet, RouterLink],
  templateUrl: './layout.html'
})
export class LayoutComponent implements OnInit {

  // 🔹 Existing
  localities: string[] = [];

  // 🔥 New dynamic filters
  flatTypes: string[] = [];
  furnishingTypes: string[] = [];
  balconyTypes: string[] = [];

  constructor(
    public filter: FilterService,
    public auth: AuthService,
    private router: Router,
    private api: ApiService
  ) {}

  ngOnInit(): void {

    // ✅ Existing locality logic (UNCHANGED)
    this.api.getTowers().subscribe(data => {
      const unique = [...new Set(data.map((t: any) => t.locality))];
      this.localities = unique;
    });

    // 🔥 NEW: Fetch enum filter options
    this.api.getUnitFilterOptions().subscribe((res: any) => {
      this.flatTypes = res.flat_types;
      this.furnishingTypes = res.furnishing_types;
      this.balconyTypes = res.balcony_types;
    });


    

    

  }

  resetFilters() {
    this.filter.moveInDate = new Date().toISOString().split('T')[0];
    this.filter.selectedType = '';
    this.filter.selectedFurnishing = '';
    this.filter.selectedParking = '';
    this.filter.selectedBalcony = '';   // 🔥 Add this
    this.filter.minRent = null;
    this.filter.maxRent = null;
    this.filter.sortOption = '';
    this.filter.selectedLocality = '';
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/']);
  }




 

}