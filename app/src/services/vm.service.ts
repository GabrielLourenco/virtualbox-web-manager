import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root',
})
export class VMService {

  private url = 'http://127.0.0.1:5000/vms';
  
  constructor(private http: HttpClient) { }

  get(): any {
    return this.http.get(this.url)
  }

  post(params): any{
    return this.http.post(this.url, params)
  }

}
