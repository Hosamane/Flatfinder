import { Routes } from '@angular/router';
import { TowerListComponent } from './features/public/tower-list/tower-list';
import { UnitListComponent } from './features/public/unit-list/unit-list';
import { App } from './app';
import { UnitDetailComponent } from './features/public/unit-detail/unit-detail';
import { LayoutComponent } from './features/public/layout/layout';
import { LoginComponent } from './features/auth/login/login';
import { RegisterComponent } from './features/auth/register/register';
import { MyBookingsComponent } from './features/user/my-bookings/my-bookings';
import { AdminLoginComponent } from './features/admin/admin-login/admin-login';
import { adminGuard } from './core/guards/admin-guard';
import { DashboardComponent } from './features/admin/dashboard/dashboard';
import { AdminLayout } from './features/admin/admin-layout/admin-layout';
import { AdminBookingsComponent } from './features/admin/bookings/bookings';
import { AdminTowersComponent } from './features/admin/towers/towers';
import { AdminUnitsComponent } from './features/admin/units/units';
import { AdminBulkUnitsComponent } from './features/admin/bulk-units/bulk-units';
import { CsvUploads } from './features/admin/csv-uploads/csv-uploads';
import { TenantProfileComponent } from './features/user/tenant/profile';
import { RenderMode } from '@angular/ssr';
// import { App } from './app';

export const routes: Routes = [

{
    path: 'admin/login',
    component: AdminLoginComponent
},
{
    path: 'admin',
    component: AdminLayout,
    canActivate: [adminGuard],
    children: [
        {
            path:'dashboard',
            component: DashboardComponent
        },
        {
            path:'bookings',
            component: AdminBookingsComponent
        },
        {
            path:'towers',
            component:AdminTowersComponent
        },
        {
            path:'units',
            component:AdminUnitsComponent
        },
        {
            path:'bulk-units',
            component: AdminBulkUnitsComponent
        },
        {
            path:'csv-upload',
            component: CsvUploads
        },
    ]

},
{
  path: '',
  component: LayoutComponent,
  children: [
    { path: 'tower/:code', component: UnitListComponent },
    
        { path: 'unit/:unitCode', component: UnitDetailComponent },
    { path: '', component: TowerListComponent }
  ]
},
 { path: 'login', component: LoginComponent},
 {path:'register',component:RegisterComponent},
 {path:'my-bookings', component:MyBookingsComponent},
 {path:'tenant-profile', component: TenantProfileComponent}

];
