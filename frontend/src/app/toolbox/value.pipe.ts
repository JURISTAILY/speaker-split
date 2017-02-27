import { Pipe, PipeTransform } from '@angular/core';
import { PercentPipe, DecimalPipe } from '@angular/common';

import { CallDetail } from '../models'

import { TimeNumberPipe } from './time-number.pipe'

@Pipe({
  name: 'value'
})
export class ValuePipe implements PipeTransform {

  __last(arr: Array<string>) : string {
  	if (arr.length == 0) {
  		return null;
  	}
  	return arr[arr.length - 1];
  }

  transform(value: CallDetail): string {
  	let pipe = null;
  	switch (this.__last(value.title.split(', '))) {
    case 'сек':
      return (new TimeNumberPipe).transform(value.value);
    case '%':
      return (new PercentPipe('rus')).transform(value.value, '1.0-1');
    case 'шт':
      return (new DecimalPipe('rus')).transform(value.value, '1.0-0');
  	}
  	switch (this.__last(value.name.split('_'))) {
    case 'duration':
      return (new TimeNumberPipe).transform(value.value);
    case 'ratio':
      return (new PercentPipe('rus')).transform(value.value, '1.0-1');
    case 'count':
      return (new DecimalPipe('rus')).transform(value.value, '1.0-0');
  	}
    return (new DecimalPipe('rus')).transform(value.value, '1.0-1');
  }

}
