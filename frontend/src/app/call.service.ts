import { Injectable, EventEmitter } from '@angular/core';
import { Http, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Call, CallTranscript, CallDetail, CallSource } from './models';
import { PARAMS_KEY_RESOLVE } from './speech-resolve'

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
    let adapted : Array<Call> = new Array<Call>(arr.length);

    let findParam = function (key : string, data : any) : any {
      const TO_JSON_KEY = {
        sa : "sa",
        operatorSpeechDuration : "operator_speech_duration",
        clientInterruptions : "client_interruptions",
        operatorSilenceDuration : "operator_silence_duration",
        legibility : "legibility"
      };
      let sought = key in TO_JSON_KEY ? TO_JSON_KEY[key] : key;
      for (let key in data) {
        if (typeof(data[key]) === "object" && !Array.isArray(data[key])) {
          for (let param of data[key].params) {
            if (param.name === sought) {
              return param.value;
            }
          }
        }
      }
      return NaN;
    };

    for (let id in arr) {
      let i = arr[id];
      adapted[id] = {
        id: i.id,
        duration : i.duration,
        sa : findParam("sa", i.info),
        operatorSpeechDuration : findParam("operatorSpeechDuration", i.info),
        clientInterruptions : findParam("clientInterruptions", i.info),
        operatorInterruptions : findParam("operatorInterruptions", i.info),
        operatorSilenceDuration : findParam("operatorSilenceDuration", i.info),
        legibility : findParam("legibility", i.info),
        isIncoming : i.isIncoming,
        grade : i.grade,
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
        details : (function(info : any) : Array<CallDetail> {
          let paramToDatail = function(sublist : Array<any>) : Array<CallDetail> {
            if (typeof(sublist) === "undefined") {
              return new Array<CallDetail>();
            }
            let result : Array<CallDetail> = new Array<CallDetail>(sublist.length);
            for (let id in sublist) {
              result[id] = {
                children : [],
                title : PARAMS_KEY_RESOLVE(sublist[id].name),
                value : sublist[id].value,
                grade : sublist[id].grade
              }
            }
            return result;
          };

          if (Array.isArray(info)) {
            let result : Array<CallDetail> = new Array<CallDetail>(info.length);
            for (let i in info) {
              result[i] = {
                children : paramToDatail(info[i].params),
                title : PARAMS_KEY_RESOLVE(info[i].name),
                value : null,
                grade : info[i].grade
              }
            }
            return result;
          } else if (typeof(info) === "object") {
            let result : Array<CallDetail> = new Array<CallDetail>(Object.keys(info).length);
            let i = 0;
            for (let key in info) {
              result[i++] = {
                children : paramToDatail(info[key].params),
                title : PARAMS_KEY_RESOLVE(key),
                value : null,
                grade : info[key].grade
              }
            }
            return result;
          } else {
            return new Array<CallDetail>();
          }
        })(i.info),
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
      };
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
