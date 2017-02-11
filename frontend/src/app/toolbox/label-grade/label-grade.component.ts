import { Component, Input } from '@angular/core';

import { gradeToColor, numberToString } from '../../utils';

@Component({
  selector: 'label-grade',
  template: `
  <div class="dialogue-tbl-progress">
  	<div [style.background-color]="gradeToColor(grade)">{{ numberToString(grade) }}</div>
  </div>`,
  styleUrls: ['./label-grade.component.css']
})
export class LabelGradeComponent  {
  @Input() grade : number;

  gradeToColor = gradeToColor;
  numberToString = numberToString;
}
