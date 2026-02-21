import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
// Removed the RouterOutlet import line from here

@Component({
  selector: 'app-root',
  imports: [RouterOutlet], // Correct! Keep this empty until you actually need RouterOutlet or other components
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}