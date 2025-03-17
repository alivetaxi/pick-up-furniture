import { NgFor, NgIf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { REST_URL } from '../app.config';

@Component({
  selector: 'app-list',
  standalone: true,
  imports: [NgFor, NgIf],
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss'
})
export class ListComponent {
  items: any[] = [];

  constructor(private http: HttpClient) {
    this.fetchItems();
  }

  fetchItems() {
    return this.http.get<any[]>(`${REST_URL}/get-items`).subscribe({
      next: (data) => {
        this.items = data;
      },
      error: (err) => {
        console.error('Error fetching items:', err);
      }
    });
  }
}
