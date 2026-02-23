import { Component, ElementRef, OnInit, ViewChild, viewChild } from '@angular/core';
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
  selectedFile: File | null=null;  // upload file
  currentImageUrl: string | null = null;
  originalImageUrl: string | null = null;
  
  @ViewChild('fileInput') fileInput! : ElementRef;
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
    facing_direction: '',
    is_active: false
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

//   saveUnit() {
//  if (!this.form.tower_code) {
//     alert("Please select tower");
//     return;
//   }
//   console.log("Tower Code:", this.form.tower_code);
//     if (this.editMode) {
//       this.api.updateUnit(this.editCode, this.form)
//         .subscribe(() => {
//           this.resetForm();
//           this.loadUnits();
//         });
//     } else {
//       this.api.createUnit(this.form.tower_code,this.form)
//         .subscribe(() => {
//           this.resetForm();
//           this.loadUnits();
//         });
//     }
//   }



// saveUnit(){
//   if(!this.form.tower_code){
//     alert("Please select Tower");
//     return;
//   }


//   if(this.editMode){
//     this.api.updateUnit(this.editCode,this.form)
//             .subscribe(() => {
//               if(this.selectedFile){
//                 this.api.uploadUnitImage(this.editCode,this.selectedFile)
//                         .subscribe();
//               }
//               this.afterSave();
//               this.resetForm();
//             });
//   }
//   else
//   {
//     this.api.createUnit(this.form.tower_code,this.form)
//             .subscribe((res:any)=>{
//               const createCode = res.unit_code;

//               if(this.selectedFile){
//                 this.api.uploadUnitImage(createCode,this.selectedFile).subscribe();
//               }

//               this.afterSave();
//               this.resetForm();
//             });
//   }
// }



saveUnit() {
  if (!this.form.tower_code) {
    alert("Please select Tower");
    return;
  }

  if (this.editMode) {

    this.api.updateUnit(this.editCode, this.form)
      .subscribe(() => {

        if (this.selectedFile) {
          this.api.uploadUnitImage(this.editCode, this.selectedFile)
            .subscribe(() => {
              this.afterSave();
            });
        } else {
          this.afterSave();
        }

      });

  } else {

    this.api.createUnit(this.form.tower_code, this.form)
      .subscribe((res: any) => {

        const createdCode = res.unit_code;

        if (this.selectedFile) {
          this.api.uploadUnitImage(createdCode, this.selectedFile)
            .subscribe(() => {
              this.afterSave();
            });
        } else {
          this.afterSave();
        }

      });

  }
}
  editUnit(unit: any) {
    console.log("Unit from backend:", unit);
    this.editMode = true;
    this.editCode = unit.unit_code;
    this.form = { ...unit,
      is_active: unit.is_active,
      tower_code: unit.tower_code
      // tower_code:this.towers.find(t=>t.id === unit.tower_id)?.code 
     };
     this.currentImageUrl = unit.image_url || null;
     this.originalImageUrl = unit.image_url || null;
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
  this.editCode = '';
  this.selectedFile=null;  ////////////
  this.currentImageUrl=null;           ////////
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
    facing_direction: '',
    is_active: false
  };
}


//   onFileSelected(event: any, unitCode: string) {

//   const file = event.target.files[0];
//   if (!file) return;

//   this.api.uploadUnitImage(unitCode, file)
//     .subscribe({
//       next: () => {
//         alert("Image uploaded");
//         this.loadUnits();
//       },
//       error: () => {
//         alert("Upload failed");
//       }
//     });
// }

// onFileSelected(event: any){         //////    
//   const file = event.target.files[0];
//   if(!file) return;
//   this.selectedFile = file;
// }

afterSave(){                        ///////////
  this.selectedFile = null;

  if(this.fileInput){
    this.fileInput.nativeElement.value = '';
  }
  this.resetForm();
  this.loadUnits();
}

// uploadImage(event: any) {
//   const file = event.target.files[0];
//   if (!file || !this.editCode) return;

//   this.api.uploadUnitImage(this.editCode, file)
//     .subscribe({
//       next: (res: any) => {
//         this.currentImageUrl = res.image_url;
//         alert("Image uploaded / replaced");
//       },
//       error: () => alert("Upload failed")
//     });
// }

deleteImage() {
  if (!this.editCode) return;
  if (!confirm("Delete image?")) return;

  this.api.deleteUnitImage(this.editCode)
    .subscribe({
      next: () => {
        this.currentImageUrl = null;
        alert("Image deleted");
      },
      error: () => alert("Delete failed")
    });
}


onImageSelected(event: any) {
  const file = event.target.files[0];
  if (!file) return;

  this.selectedFile = file;

  // Preview before upload
  const reader = new FileReader();
  reader.onload = () => {
    this.currentImageUrl = reader.result as string;
  };
  reader.readAsDataURL(file);
}
removeImage() {

  // CASE 1: New image selected (not uploaded yet)
  if (this.selectedFile) {
    this.selectedFile = null;
    this.currentImageUrl = this.originalImageUrl;
    return;
  }

  // CASE 2: Editing and existing image in DB
  if (this.editMode && this.originalImageUrl) {

    if (!confirm("Delete this image permanently?")) return;

    this.api.deleteUnitImage(this.editCode)
      .subscribe(() => {
        this.originalImageUrl = null;
        this.currentImageUrl = null;
      });

  }

}
}
