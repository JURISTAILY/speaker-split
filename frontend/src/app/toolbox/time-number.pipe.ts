import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'timeNumber'})
export class TimeNumberPipe implements PipeTransform {
  transform(s: number): string {
    if (!isFinite(s)) {
        return "—";
    }
    let h = Math.floor(s / 3600);
    s -= h * 3600;
    let m = Math.floor(s / 60);
    s -= m * 60;
    let ms = s - Math.floor(s);
    s = Math.floor(s);
    if (ms) {
        ms *= 10;
        ms = Math.round(ms);
        while (ms !== 0 && ms / 10 === Math.floor(ms / 10)) {
            ms /= 10;
        }
    }
    let result = '';
    if (h) {
        result += h;
        if (m > 9) {
            result += ':' + m;
        } else {
            result += ':0' + m;
        }
        if (s > 9) {
            result += ':' + s;
        } else {
            result += ':0' + s;
        }
    } else {
        result += m > 9 ? m : ('0' + m);
        if (s > 9) {
            result += ':' + s;
        } else {
            result += ':0' + s;
        }
    }
    if (ms) {
        result += '.' + ms;
    }
    return result;
  }
}