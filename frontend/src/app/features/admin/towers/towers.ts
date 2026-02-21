import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './towers.html'
})
export class AdminTowersComponent implements OnInit {

  towers: any[] = [];
  loading = true;

  name = '';
  code = '';
  locality='';

  editMode = false;
  editCode = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadTowers();
  }

  loadTowers() {
    this.api.getTowersAll().subscribe((data: any) => {
      this.towers = data;
      this.loading = false;
    });
  }

  saveTower() {

    if (this.editMode) {
      this.api.updateTower(this.editCode, {
        name: this.name,
        code: this.code,
        locality : this.locality
      }).subscribe(() => {
        this.resetForm();
        this.loadTowers();
      });
    } else {
      this.api.createTower({
        name: this.name,
        code: this.code,
        locality: this.locality
      }).subscribe(() => {
        this.resetForm();
        this.loadTowers();
      });
    }
  }

  editTower(tower: any) {
    this.editMode = true;
    this.editCode = tower.code;
    this.name = tower.name;
    this.code = tower.code;
    this.locality = tower.locality;
  }

  deleteTower(code: string) {
    if (confirm("Delete this tower?")) {
      this.api.deleteTower(code).subscribe(() => {
        this.loadTowers();
      });
    }
  }

  resetForm() {
    this.name = '';
    this.code = '';
    this.locality = '';
    this.editMode = false;
  }

}
