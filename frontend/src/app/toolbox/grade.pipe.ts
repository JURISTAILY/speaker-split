import { Pipe, PipeTransform } from '@angular/core';
import { Call, CallDetail } from './../models';

declare var d3: any;

@Pipe({
  name: 'grade'
})
export class GradePipe implements PipeTransform {
  static gradeFromJSON(scales : any) : any {
    let result = {};
    for (let key in scales) {
      result[key] = d3.scaleLinear().domain(scales[key].domain).range(scales[key].range);
    }
    return result;
  }

  static readonly JSON = {
    "operator_speech_ratio" : {
      "domain" : [0,  0.01,0.2,0.3,0.35,0.4,0.55,0.8,   1],
      "range"  : [1,     1,  3,  7,  10,  8,   3,  1,   1],
      "width" : 1
    },
    "client_speech_ratio" : {
      "domain" : [0,  0.01,0.2,0.3,0.35,0.4,0.55,0.8,   100],
      "range"  : [1,     1,  3,  7,  10,  8,   3,  1,     1],
      "width" : 1
    },
    "operator_speech_duration" : {
      "domain" : [0,    10, 30, 120, 240, 300, 900, 1500,   2000],
      "range"  : [1,     1,  8,  10,   8,   6,   3,    1,      1],
      "width" : 1
    },
    "client_speech_duration" : {
      "domain" : [0,     5, 20,  60, 120, 200, 500, 1000,   2000],
      "range"  : [1,     1,  8,  10,   8,   6,   3,    1,      1],
      "width" : 1
    },
    "operator_to_client_speech_ratio" : {
      "domain" : [-1,     0, 0.1, 0.3, 0.5, 0.6, 0.8, 0.9,   100],
      "range"  : [ 1,     1,   1,   2,   8,  10,   2,   1,     1],
      "width" : 1
    },
    "client_longest_speech_segment_duration" : {
      "domain" : [-1,     0,  10, 30, 50, 80,    100],
      "range"  : [ 1,     1,   3, 10,  5,  1,      1],
      "width" : 1
    },
    "operator_longest_speech_segment_duration" : {
      "domain" : [-1,     0,  10, 30, 50, 80,    100],
      "range"  : [ 1,     1,   3, 10,  5,  1,      1],
      "width" : 1
    },
    "both_interruptions_ratio" : {
      "domain" : [-1,     0, 0.01, 0.1, 0.3, 0.5,     100],
      "range"  : [10,    10,    9,   5,   2,   1,       1],
      "width" : 1
    },
    "both_interruptions_count" : {
      "domain" : [-1,     0, 2, 4, 15, 20, 30,    100],
      "range"  : [10,    10, 9, 8,  5,  3,  1,      1],
      "width" : 1
    },
    "both_interruptions_duration" : {
      "domain" : [-1,     0, 3, 8, 15,     100],
      "range"  : [10,    10, 5, 2,  1,       1],
      "width" : 1
    },
    "operator_interruptions_ratio" : {
      "domain" : [-1,     0, 0.01, 0.1, 0.3, 0.5,     100],
      "range"  : [10,    10,    9,   5,   2,   1,       1],
      "width" : 1
    },
    "operator_interruptions_count" : {
      "domain" : [-1,     0, 2, 4, 15, 20, 30,    100],
      "range"  : [10,    10, 9, 8,  5,  3,  1,      1],
      "width" : 1
    },
    "operator_interruptions_duration" : {
      "domain" : [-1,     0, 1, 2,  7, 10, 15,    100],
      "range"  : [10,    10, 9, 8,  5,  3,  1,      1],
      "width" : 1
    },
    "client_interruptions_ratio" : {
      "domain" : [-1,     0, 0.01, 0.1, 0.3, 0.5,     100],
      "range"  : [10,    10,    9,   5,   2,   1,       1],
      "width" : 1
    },
    "client_interruptions_count" : {
      "domain" : [-1,     0, 2, 4, 15, 20, 30,    100],
      "range"  : [10,    10, 9, 8,  5,  3,  1,      1],
      "width" : 1
    },
    "client_interruptions_duration" : {
      "domain" : [-1,     0, 3, 8, 15,     100],
      "range"  : [10,    10, 5, 2,  1,       1],
      "width" : 1
    },
    "both_silence_ratio" : {
      "domain" : [ 0,    0.2, 0.3, 0.5, 0.8,     100],
      "range"  : [10,    10,    5,   3,   1,       1],
      "width" : 1
    },
    "both_silence_duration" : {
      "domain" : [ 0,    20, 30, 50, 80,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    },
    "both_longest_silence_segment_duration" : {
      "domain" : [ 0,     5, 10, 20, 40,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    },
    "operator_silence_ratio" : {
      "domain" : [ 0,    20, 30, 50, 80,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    },
    "operator_silence_duration" : {
      "domain" : [ 0,    20, 30, 50, 80,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    },
    "operator_longest_silence_segment_duration" : {
      "domain" : [ 0,    20, 30, 50, 80,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    },
    "client_silence_ratio" : {
      "domain" : [ 0,    20, 30, 50, 80,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    },
    "client_silence_duration" : {
      "domain" : [ 0,    10, 40, 50, 80,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    },
    "client_longest_silence_segment_duration" : {
      "domain" : [ 0,     5, 10, 20, 30,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    },
    "operator_freezing_duration" : {
      "domain" : [ 0,     5, 10, 20, 30,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    },
    "client_freezing_duration" : {
      "domain" : [ 0,     5, 10, 20, 30,     100],
      "range"  : [10,    10,  5,  3,  1,       1],
      "width" : 1
    }
  };

  static readonly GRADE_FUNCTIONS = GradePipe.gradeFromJSON(GradePipe.JSON);
  static readonly WEIGHT = (function(data) {
    let result = {};
    for (let i in data) {
      result[i] = data[i].width;
    }
    return result;
  })(GradePipe.JSON);

  transform(call : Call): number;
  transform(details : CallDetail[]) : number;
  transform(detail : CallDetail): number;
  transform(value: number, key: string): number;
  transform(value : any) : number {
    if (typeof value === "number") {
      let key = arguments[1];
      if (key in GradePipe.GRADE_FUNCTIONS) {
        return GradePipe.GRADE_FUNCTIONS[key](value);
      }
      return NaN;
    } else if (Array.isArray(value)) {
      let details = value;
      let result = 0;
      let rez = 0;
      for (let i of details) {
        let weight = i.name in GradePipe.WEIGHT ? GradePipe.WEIGHT[i.name] : 1;
        let grade = this.transform(i);
        if (grade >= 1 && grade <= 10) {
          result += grade * weight;
          rez += weight;
        }
      }
      return result / rez;
    } else if ("details" in value) {
      let call = value;
      return this.transform(call.details);
    } else {
      let detail = value;
      if (typeof detail.value !== "number") {
        return this.transform(detail.children);
      }
      return this.transform(detail.value, detail.name);
    }
  }
}
