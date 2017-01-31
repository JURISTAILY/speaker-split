import { Injectable } from '@angular/core';

import { Call } from './models';
import { CALLS } from './mock-calls'

@Injectable()
export class CallService {

  constructor() { }

  getCalls(): Promise<Call[]> {
    return new Promise(resolve => {
      setTimeout(() => resolve(CALLS), 2000)
    });
  }

}
