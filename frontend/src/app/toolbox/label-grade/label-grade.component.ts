import { Component, Input } from '@angular/core';

declare var isNaN: any;

@Component({
  selector: 'label-grade',
  template: `
  <div class="dialogue-tbl-progress">
  	<div [style.background-color]="grade | gradeToColor">{{ (isNaN(grade) ? '—' : (grade | number:'1.0-1')) }}</div>
  </div>`,
  styleUrls: ['./label-grade.component.css']
})
export class LabelGradeComponent  {
  isNaN() : boolean { return isNaN(arguments[0]); }

  @Input() grade : number;
}
