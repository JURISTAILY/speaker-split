import { Component, Input } from '@angular/core';
import { DecimalPipe, PercentPipe } from '@angular/common'
import { GradePipe } from '../toolbox/grade.pipe'

import { CallDetail } from '../models';

import { rusNumberTermination } from '../utils';

@Component({
  selector: 'dialogue-details-table',
  templateUrl: './dialogue-details-table.component.html',
  styleUrls: ['./dialogue-details-table.component.css']
})
export class DialogueDetailsTableComponent  {
  @Input() details : CallDetail[];

  open: { [ key : string ] : boolean } = {};

  gradeValueAndUnit(num : number) : string {
    if (typeof(num) !== 'undefined' && num === num) {
      num = Math.round(num * 10) / 10
      return new DecimalPipe('rus').transform(num,'1.0-1') + ' балл' + rusNumberTermination(num);
    }
    return 'нет оценки'
  }

  orderByGrade(prop : Array<CallDetail>) : Array<CallDetail> {
    var grade = new GradePipe();
    prop.sort((a, b) => grade.transform(a) - grade.transform(b));
    return prop;
  }
}
