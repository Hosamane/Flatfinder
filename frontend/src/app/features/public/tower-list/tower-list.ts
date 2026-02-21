// import { Component, OnInit } from '@angular/core';
// import { Router } from '@angular/router';
// import { ApiService } from '../../../core/service/api.service';
// import { CommonModule } from '@angular/common';
// // import { CommonModule } from '@angular/common';
// import { FilterService } from '../../../core/services/filter/filter.service';
// @Component({
//   selector: 'app-tower-list',
//   standalone: true,
//   imports:[CommonModule],
//   templateUrl: './tower-list.html'
// })
// // export class TowerListComponent implements OnInit {

// //   towers: any[] = [];

// //   constructor(private api: ApiService, private router: Router) {}

// //   ngOnInit() {
// //     this.api.getTowers().subscribe(data => {
// //       this.towers = data;
// //     });
// //   }
// // ngOnInit() {
// //   this.api.getTowers().subscribe({
// //     next: (data) => {
// //       console.log("TOWERS:", data);
// //       this.towers = data;
// //     },
// //     error: (err) => {
// //       console.error("ERROR:", err);
// //     }
// //   });
// // }


// //   ngOnInit() {
// //   this.api.getTowers().subscribe({
// //     next: (data) => {
// //       console.log("TOWERS:", data);
// //       this.towers = data;
// //     },
// //     error: (err) => {
// //       console.error("ERROR:", err);
// //     }
// //   });
// // }

// //   goToTower(code: string) {
// //     this.router.navigate(['/tower', code]);
// //   }
// // }


// export class TowerListComponent implements OnInit {

//   towers: any[] = [];
//   loading = true;

//   constructor(
//     private api: ApiService, 
//     private router: Router,
//     private filter:FilterService) {}


// //   ngDoCheck() {
// //   this.loadTowers();
// // }
//   // ngOnInit() {
//   //    this.loadTowers();
//   //   this.api.getTowers(this.filter.selectedLocality).subscribe({
//   //     next: (data) => {
//   //       this.towers = data;
//   //       this.loading = false;
//   //     },
//   //     error: () => this.loading = false
//   //   });
//   // }


//   ngOnInit() {
//   this.api.getTowers().subscribe(data => {

//     // Extract unique localities
//     const unique = [...new Set(data.map((t: any) => t.locality))];

//     this.localities = unique;
//   });
// }


//   openTower(code: string) {
//     this.router.navigate(['/tower', code]);
//   }


//   loadTowers() {
//   this.api.getTowers(this.filter.selectedLocality)
//     .subscribe(data => {
//       this.towers = data;
//     });
// }
// }


import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';
import { FilterService } from '../../../core/services/filter/filter.service';

@Component({
  selector: 'app-tower-list',
  standalone: true,
  imports:[CommonModule],
  templateUrl: './tower-list.html'
})
export class TowerListComponent implements OnInit {

  towers: any[] = [];
  loading = true;
  towerCount = 0;

  constructor(
    private api: ApiService, 
    private router: Router,
    public filter: FilterService
  ) {}

  ngOnInit() {

  this.filter.locality$.subscribe(() => {
    this.loadTowers();
  });

  this.loadTowers();
}

  loadTowers() {
    this.loading = true;

    this.api.getTowers(this.filter.selectedLocality)
      .subscribe(data => {
        this.towers = data;
        this.towerCount = data.length;
        this.loading = false;
      });
  }

  openTower(code: string) {
    this.router.navigate(['/tower', code]);
  }

  
}