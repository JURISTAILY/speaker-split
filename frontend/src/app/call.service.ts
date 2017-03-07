import { Injectable, EventEmitter } from '@angular/core';
import { Http, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { environment } from '../environments/environment';

import { Call, CallTranscript, CallDetail, CallSource } from './models';
import { ColumnDescription } from './dialogue-view/column-description'

@Injectable()
export class CallService {
  private CALLS_URL = environment.apiUrl + environment.callsPath;

  constructor(private http: Http) {
  }

  private getRawCalls() : Promise<any[]> {
    return this.http.get(this.CALLS_URL)
                    .toPromise()
                    .then(response => response.json().data)
                    .catch(this.handleError);
  }

  private getRawComputedCallDebug(callName): Promise<any[]> {
    return this.http.get(environment.apiUrl + environment.calcPath + callName)
                    .toPromise()
                    .then(response => response.json())
                    .catch(this.handleError);
  }

  private static fromDataForMainTable(datum : any) {
    let arr = ColumnDescription.DIALOGUE_VIEW_COLUMNS;
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
    for (let itm of data.info) {
      for (let param of itm.params) {
        if (param.name === sought) {
          return param.value;
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

  getComputedCallDebug(callName : string) : Promise<Array<Call>> {
    return this.getRawComputedCallDebug(callName).then(rawCall => {
      return [
        {
          id : 0,
          tableValues : (function(data) {
            let arr = ColumnDescription.DIALOGUE_VIEW_COLUMNS;
            let result = Array<any>(arr.length)
            let info = data['info'];
            for (let id in arr) {
              if (arr[id].jsonKey in data) {
                result[id] = data[arr[id].jsonKey];
              } else if (arr[id].jsonKey in info) {
                result[id] = info[arr[id].jsonKey];
              }
              result[id] = arr[id].pipe.transform(result[id]);
            }
            return result;
          })(rawCall),
          name: rawCall['filename'],
          isIncoming : rawCall['is_incoming'],
          transcripts : [],
          details : [{
            children : (data => {
              let result = [];
              for (let i in data) {
                result.push({
                  children : null,
                  title : i,
                  value : data[i],
                  name : i
                });
              }
              return result;
            })(rawCall['info']),
            title : "Все параметры сразу",
            value : null,
            name : ''
          }],
          sources : [],
          debug : rawCall['debug']
        } as Call
      ];
    });
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
