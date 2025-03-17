import { Component } from '@angular/core';
import { NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { REST_URL } from '../app.config';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [FormsModule, NgIf],
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
  name: string = '';
  description: string = '';
  files: File[] = [];
  isUploading = false;
  uploadSuccess = false;

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.files = Array.from(event.target.files);
  }

  onSubmit() {
    if (!this.name || !this.description || this.files.length === 0) {
      alert("Please fill out all fields and select at least one image.");
      return;
    }

    this.isUploading = true;

    const formData = new FormData();
    formData.append('name', this.name);
    formData.append('description', this.description);
    
    this.files.forEach((file, index) => {
      formData.append(`images`, file); // Multiple files
    });

    this.http.post(`${REST_URL}/upload-item`, formData).subscribe({
      next: (response) => {
        console.log('Upload success:', response);
        this.uploadSuccess = true;
        this.isUploading = false;
      },
      error: (error) => {
        console.error('Upload failed:', error);
        this.isUploading = false;
      }
    });
  }
}