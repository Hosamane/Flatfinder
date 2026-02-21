import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/service/api.service';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './profile.html'
})
export class TenantProfileComponent implements OnInit {

  profile: any = {
    tenant_type: '',
    date_of_birth: '',
    college_name: '',
    department: '',
    company_name: '',
    designation: '',
    id_proof_type: '',
    id_proof_number: ''
  };

  loading = false;
  profileExists = false;

  constructor(private api: ApiService) {}

  ngOnInit() {
  this.api.getTenantProfile().subscribe({
    next: (res: any) => {

      if (!res.profile_exists) {
        console.log("Profile not created");
        this.profileExists = false;
      } else {
        console.log("Profile loaded", res);
        this.profile = res;
        this.profileExists = true;
      }

    },
    error: (err) => {
      console.log("Error:", err);
    }
  });
}

  loadProfile() {
    this.api.getTenantProfile().subscribe({
      next: (res: any) => {
        if (res.profile_exists === false) {
          this.profileExists = false;
        } else {
          this.profile = res;
          this.profileExists = true;
        }
      },
      error: () => {
        this.profileExists = false;
      }
    });
  }

  saveProfile() {
    this.loading = true;

    this.api.updateTenantProfile(this.profile).subscribe({
      next: (res) => {
        this.profile = res;
        this.profileExists = true;
        this.loading = false;
        alert("Profile saved successfully");
      },
      error: () => {
        this.loading = false;
        alert("Failed to save profile");
      }
    });
  }

}