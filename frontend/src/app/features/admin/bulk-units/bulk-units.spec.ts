import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminBulkUnitsComponent } from './bulk-units';

describe('BulkUnits', () => {
  let component: AdminBulkUnitsComponent;
  let fixture: ComponentFixture<AdminBulkUnitsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminBulkUnitsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminBulkUnitsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
