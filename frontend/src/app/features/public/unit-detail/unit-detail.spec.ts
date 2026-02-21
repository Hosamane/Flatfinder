import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitDetail } from './unit-detail';

describe('UnitDetail', () => {
  let component: UnitDetail;
  let fixture: ComponentFixture<UnitDetail>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnitDetail]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitDetail);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
