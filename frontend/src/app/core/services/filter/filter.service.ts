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


  // private filterSource = new BehaviorSubject<void>(undefined);
  // filterChanged$ = this.filterSource.asObservable();

  // private triggerFilterChange() {
  //   this.filterSource.next();
  // }


  resetFilters() {
  this.moveInDate = new Date().toISOString().split('T')[0];
  this.selectedType = '';
  this.selectedFurnishing = '';
  this.selectedParking = '';
  this.selectedBalcony = '';
  this.minRent = null;
  this.maxRent = null;
  this.sortOption = '';
  this.selectedLocality = '';


  //  this.triggerFilterChange();
}

  setMoveInDate(date: string) {
    this.moveInDate = date;
    //  this.triggerFilterChange();
  }

 

  setType(type: string) {
    this.selectedType = type;
    //  this.triggerFilterChange();
  }

  setFurnishing(furnishing: string) {
    this.selectedFurnishing = furnishing;
    //  this.triggerFilterChange();
  }

  setParking(parking: string) {
    this.selectedParking = parking;
    //  this.triggerFilterChange();
  }

  setBalcony(balcony: string) {
    this.selectedBalcony = balcony;
    //  this.triggerFilterChange();
  }
  private localitySource = new BehaviorSubject<string>('');
  locality$ = this.localitySource.asObservable();
  setLocality(value: string) {
    this.selectedLocality = value;
    this.localitySource.next(value);
  }
}
