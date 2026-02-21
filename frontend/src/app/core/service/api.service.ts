import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Unit } from '../models/unit.model';
import { environment } from '../../../environments/environment';
@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = environment.apiUrl; 
//   'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  // getTowers(): Observable<any> {
  //   return this.http.get(`${this.baseUrl}/public/towers`);
  // }
// getTowers(locality?: string) {
//   // if (locality) {
//   //   return this.http.get<any[]>(
//   //     `${this.baseUrl}/towers?locality=${locality}`
//   //   );
//   // }

//   if(locality){
//     return this.http.get<any[]>(`${this.baseUrl}/public/towers?locality=${locality}`);
//   }
//   // return this.http.get<any[]>(`${this.baseUrl}/public/towers`);
//   return this.http.get<any[]>(`${this.baseUrl}/public/towers`);

// }


getTowers(locality?: string) {
  let url = `${this.baseUrl}/public/towers`;
  if (locality){
    url+= `?locality=${locality}`;
  }

  return this.http.get<any[]>(url);

}
//   getUnitsByTower(code: string): Observable<any> {
//     return this.http.get(`${this.baseUrl}/towers/${code}/units`);
//   }

getUnitsByTower(code: string, moveInDate?: string) {
  let url = `${this.baseUrl}/public/towers/${code}/units`;

  if (moveInDate) {
    url += `?move_in_date=${moveInDate}`;
  }

  return this.http.get<Unit[]>(url);
}
getUnitByCode(code: string) {
  return this.http.get(`${this.baseUrl}/public/units/${code}`);
}
bookUnit(unitCode: string, leaseStart: string, leaseEnd: string) {
  return this.http.post(
    `${this.baseUrl}/bookings/`,
    {
      unit_code: unitCode,
      lease_start: leaseStart,
      lease_end: leaseEnd
    },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}


login(email: string, password: string) {
  return this.http.post(
    `${this.baseUrl}/auth/login`,
    { email, password }
  );
}

register(name: string, email: string, password: string) {
  return this.http.post(
    `${this.baseUrl}/auth/register`,
    { name, email, password }
  );
}


getMyBookings() {
  return this.http.get(`${this.baseUrl}/bookings/my`);
}

getAllBookings() {
  return this.http.get(
    `${this.baseUrl}/admin/bookings`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}

updateBookingStatus(id: number, status: string) {
  return this.http.put(
    `${this.baseUrl}/admin/bookings/${id}`,
    { status },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}

getTowersAll() {
  return this.http.get(
    `${this.baseUrl}/admin/towers`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}


createTower(data: any) {
  return this.http.post(`${this.baseUrl}/admin/towers`, data);
}


updateTower(code: string, data: any) {
  return this.http.put(
    `${this.baseUrl}/admin/towers/${code}`,
    data,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}

deleteTower(code: string) {
  return this.http.delete(
    `${this.baseUrl}/admin/towers/${code}`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}


getUnits() {
  return this.http.get(
    `${this.baseUrl}/admin/units`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}

// createUnit(data: any) {
//   return this.http.post(
//     `${this.baseUrl}/admin/units`,
//     data,
//     {
//       headers: {
//         Authorization: `Bearer ${localStorage.getItem('access_token')}`
//       }
//     }
//   );
// }


createUnit(towerCode: string, data: any) {
  return this.http.post(
    `${this.baseUrl}/admin/towers/${towerCode}/units`,
    data,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}

updateUnit(code: string, data: any) {
  return this.http.put(
    `${this.baseUrl}/admin/units/${code}`,
    data,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}

deleteUnit(code: string) {
  return this.http.delete(
    `${this.baseUrl}/admin/units/${code}`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    }
  );
}

bulkCreateUnits(code: string, data: any) {
  return this.http.post(
    `${this.baseUrl}/admin/towers/${code}/units/bulk`,
    data,
    
  );
}
uploadUnitImage(unitCode: string, file: File) {

  const formData = new FormData();
  formData.append('image', file);

  return this.http.post(
    `${this.baseUrl}/admin/units/${unitCode}/upload-image`,
    formData,
    
  );
}

getUnitDetail(unitCode: string) {
  return this.http.get<any>(`${this.baseUrl}/units/${unitCode}`);
}



getUnitFilterOptions() {
  return this.http.get<any>(
    `${this.baseUrl}/public/unit-filter-options`
  );
}

getTenantProfile() {
  return this.http.get(`${this.baseUrl}/tenant/tenant-profile`);
}

updateTenantProfile(data: any) {
  return this.http.put(`${this.baseUrl}/tenant/tenant-profile`, data);
}
getAdminDashboard() {
  return this.http.get(`${this.baseUrl}/admin/dashboard`);
}

}
