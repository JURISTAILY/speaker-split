import { Injectable, EventEmitter } from '@angular/core';
import { Http, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Call, CallTranscript, CallDetail, CallSource } from './models';
import { DialogueViewComponent } from './dialogue-view/dialogue-view.component'

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

  private static fromDataForMainTable(datum : any) {
    let arr = DialogueViewComponent.COLUMNS;
    let result = Array<any>(arr.length)
    for (let id in arr) {
      result[id] = arr[id].pipe.transform(CallService.findParam(arr[id].jsonKey, datum), '1.0-1');
    }
    return result;
  }

  private static findParam(sought : string, data : any) : any {
    if (sought in data) {
      return data[sought];
    }
    for (let key in data.info) {
      if (typeof(data.info[key]) === "object" && !Array.isArray(data.info[key])) {
        for (let param of data.info[key].params) {
          if (param.name === sought) {
            return param.value;
          }
        }
      }
    }
    return NaN;
  }

  private static infoToDetails(info : any) : Array<CallDetail> {
    let paramToDatail = function(sublist : Array<any>) : Array<CallDetail> {
      if (typeof(sublist) === "undefined") {
        return new Array<CallDetail>();
      }
      let result : Array<CallDetail> = new Array<CallDetail>(sublist.length);
      for (let id in sublist) {
        result[id] = {
          name : sublist[id].name,
          children : [],
          title : sublist[id].name_rus,
          value : sublist[id].value
        } as CallDetail
      }
      return result;
    };

    if (Array.isArray(info)) {
      let result : Array<CallDetail> = new Array<CallDetail>(info.length);
      for (let i in info) {
        result[i] = {
          children : paramToDatail(info[i].params),
          title : info[i].name_rus,
          name : info[i].name,
          value : null
        } as CallDetail
      }
      return result;
    } else {
      return new Array<CallDetail>();
    }
  }

  private convertCalls(arr: any[]): Call[] {
    let adapted : Array<Call> = new Array<Call>(arr.length);


    let independentFrontedId = 0;
    for (let id in arr) {
      let i = arr[id];
      adapted[id] = {
        id : independentFrontedId++,
        tableValues : CallService.fromDataForMainTable(i),
        name: i.id,
        isIncoming : i.isIncoming,
        transcripts : (function(transcripts : Array<any>) : CallTranscript[] {
          if (typeof(transcripts) === "undefined") {
            return new Array<CallTranscript>();
          }
          let res : Array<CallTranscript> = new Array<CallTranscript>(transcripts.length);
          for (let id in transcripts) {
            let transcript = transcripts[id];
            res[id] = {
              'begin' : transcript['begin'],
              'end' : transcript['end'],
              transcript: transcript.phrase,
              isOperator : transcript.speaker === "operator"
            };
          }
          return res;
        })(i.transcript),
        details : CallService.infoToDetails(i.info),
        sources : (function(sources : Array<any>) : CallSource[] {
          if (typeof(sources) === "undefined") {
            return new Array<CallSource>();
          }
          let src : Array<CallSource> = new Array<CallSource>(sources.length);
          for (let id in sources) {
            src[id] = { source : sources[id] };
          }
          return src;
        })(i.sources),
      } as Call;
    }

    return adapted;
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
