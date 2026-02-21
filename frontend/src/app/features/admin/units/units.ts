import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../core/service/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './units.html'
})
export class AdminUnitsComponent implements OnInit {

  units: any[] = [];
  towers: any[] = [];

  loading = true;
  editMode = false;
  editCode = '';

  form: any = {
    tower_code: '',
    wing: '',
    floor_number: '',
    flat_number: '',
    rent: '',
    available_from: '',
    flat_type: '',
    furnishing: '',
    balcony_type: '',
    parking: false,
    facing_direction: ''
  };

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadUnits();
    this.loadTowers();
  }

 loadUnits() {
  this.loading = true;
  this.api.getUnits().subscribe({
    next: (data: any) => {
      console.log("Units:", data);   // 🔥 Debug
      this.units = data;
      this.loading = false;
    },
    error: (err) => {
      console.error(err);
      this.loading = false;
    }
  });
}


  loadTowers() {
    this.api.getTowers().subscribe((data: any) => {
      this.towers = data;
    });
  }

  saveUnit() {
 if (!this.form.tower_code) {
    alert("Please select tower");
    return;
  }
  console.log("Tower Code:", this.form.tower_code);
    if (this.editMode) {
      this.api.updateUnit(this.editCode, this.form)
        .subscribe(() => {
          this.resetForm();
          this.loadUnits();
        });
    } else {
      this.api.createUnit(this.form.tower_code,this.form)
        .subscribe(() => {
          this.resetForm();
          this.loadUnits();
        });
    }
  }

  editUnit(unit: any) {
    console.log("Unit from backend:", unit);
    this.editMode = true;
    this.editCode = unit.unit_code;
    this.form = { ...unit,
      tower_code: unit.tower_code
      // tower_code:this.towers.find(t=>t.id === unit.tower_id)?.code 
     };
      console.log("Form after edit:", this.form);
  }

  deleteUnit(code: string) {
    if (confirm("Delete unit?")) {
      this.api.deleteUnit(code)
        .subscribe(() => this.loadUnits());
    }
  }

  resetForm() {
  this.editMode = false;
  this.form = {
    tower_code: '',
    wing: '',
    floor_number: '',
    flat_number: '',
    rent: '',
    available_from: '',
    flat_type: '',
    furnishing: '',
    balcony_type: '',
    parking: false,
    facing_direction: ''
  };
}


  onFileSelected(event: any, unitCode: string) {

  const file = event.target.files[0];
  if (!file) return;

  this.api.uploadUnitImage(unitCode, file)
    .subscribe({
      next: () => {
        alert("Image uploaded");
        this.loadUnits();
      },
      error: () => {
        alert("Upload failed");
      }
    });
}


}
