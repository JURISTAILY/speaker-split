import { Component, Input } from '@angular/core';

import { CallDetail } from '../models';

import { gradeToColor, rusNumberTermination, gradeToPercent } from '../utils';

@Component({
  selector: 'app-dialogue-details-table',
  templateUrl: './dialogue-details-table.component.html',
  styleUrls: ['./dialogue-details-table.component.css']
})
export class DialogueDetailsTableComponent  {
  @Input() details : CallDetail[];

  // Static proxy method.
  gradeToColor = gradeToColor;
  gradeToPercent = gradeToPercent;

  open: { [ key : string ] : boolean } = {};

  switchDetails(item): void {
    if (!(item.title in this.open)) {
      this.open[item] = false;
    }
    this.open[item.title] = !this.open[item.title];
    console.log(item.title, "turned to", this.isOpen(item.title));
  }

  isOpen(item) : boolean {
    if (!(item in this.open)) {
      this.open[item] = false;
    }
    return this.open[item];
  }

  gradeValueAndUnit(num : number) : string {
    if (typeof(num) !== 'undefined' && num === num) {
      return num + ' балл' + rusNumberTermination(num);
    }
    return 'нет оценки'
  }


}
