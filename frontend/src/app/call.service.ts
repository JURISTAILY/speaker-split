import { Injectable, EventEmitter } from '@angular/core';
import { Http, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Call } from './models';
import { CALLS } from './mock-calls'

@Injectable()
export class CallService {
  private API_URL = 'http://demo.avto-podborka.ru/api/calls';

  constructor(private http: Http) { }

  private getRawCalls(): Promise<any[]> {
    return this.http.get(this.API_URL)
                    .toPromise()
                    .then(response => response.json().data)
                    .catch(this.handleError);
  }

  private convertCalls(arr: any[]): Call[] {
    return CALLS;
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occured', error);
    return Promise.reject(error.message || error);
  }

  getCalls(): Promise<Call[]> {
    return this.getRawCalls()
               .then(rawCalls => this.convertCalls(rawCalls))
               .catch(this.handleError);
  }

}
