import { Component, Input } from '@angular/core';
import { DecimalPipe, PercentPipe } from '@angular/common'

import { CallDetail } from '../models';

import { rusNumberTermination } from '../utils';

@Component({
  selector: 'app-dialogue-details-table',
  templateUrl: './dialogue-details-table.component.html',
  styleUrls: ['./dialogue-details-table.component.css']
})
export class DialogueDetailsTableComponent  {
  @Input() details : CallDetail[];

  open: { [ key : string ] : boolean } = {};

  gradeValueAndUnit(num : number) : string {
    if (typeof(num) !== 'undefined' && num === num) {
      return new DecimalPipe('rus').transform(num,'1.0-1') + ' балл' + rusNumberTermination(num);
    }
    return 'нет оценки'
  }


}
