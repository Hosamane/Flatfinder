import { Component } from '@angular/core';

import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { environment } from '../../../../environments/environment';
@Component({
  selector: 'app-csv-uploads',
  imports: [CommonModule,FormsModule],
  templateUrl: './csv-uploads.html'
})
export class CsvUploads {
  private baseUrl = environment.apiUrl;

  selectedFile: File | null = null;
  result: any = null;
  loading = false;

  constructor(private http: HttpClient) {}

  onFileSelect(event: any) {
    this.selectedFile = event.target.files[0];
  }

 uploadFile() {
  if (!this.selectedFile) {
    alert("Please select a CSV file");
    return;
  }

  const formData = new FormData();
  formData.append('admin_csv', this.selectedFile);

  this.loading = true;

  this.http.post(`${this.baseUrl}/admin/csv-upload`, formData)
    .subscribe({
      next: (res) => {
        this.result = res;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        alert("Upload failed");
        this.loading = false;
      }
    });
}



}