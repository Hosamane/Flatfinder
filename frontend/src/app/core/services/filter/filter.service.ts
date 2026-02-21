import { Injectable } from '@angular/core';

import { BehaviorSubject } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class FilterService {

  moveInDate: string = new Date().toISOString().split('T')[0];
  selectedType: string = '';
  selectedFurnishing: string = '';
  selectedParking: string = '';
  minRent: number | null = null;
  maxRent: number | null = null;
  sortOption: string = '';
  selectedLocality: string = '';
  selectedBalcony: string = '';




  setMoveInDate(date: string) {
    this.moveInDate = date;
  }

 

  setType(type: string) {
    this.selectedType = type;
  }

  setFurnishing(furnishing: string) {
    this.selectedFurnishing = furnishing;
  }

  setParking(parking: string) {
    this.selectedParking = parking;
  }

  setBalcony(balcony: string) {
    this.selectedBalcony = balcony;
  }
  private localitySource = new BehaviorSubject<string>('');
  locality$ = this.localitySource.asObservable();
  setLocality(value: string) {
    this.selectedLocality = value;
    this.localitySource.next(value);
  }
}
