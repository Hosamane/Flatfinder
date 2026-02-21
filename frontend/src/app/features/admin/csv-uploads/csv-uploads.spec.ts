import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CsvUploads } from './csv-uploads';

describe('CsvUploads', () => {
  let component: CsvUploads;
  let fixture: ComponentFixture<CsvUploads>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CsvUploads]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CsvUploads);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
