import { Routes } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { ListComponent } from './list/list.component';

export const routes: Routes = [
    { path: 'upload', component: UploadComponent },
    { path: '', component: ListComponent }
];

