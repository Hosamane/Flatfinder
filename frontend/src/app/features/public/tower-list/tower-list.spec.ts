import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TowerListComponent } from './tower-list';

describe('TowerList', () => {
  let component: TowerListComponent;
  let fixture: ComponentFixture<TowerListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TowerListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TowerListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
