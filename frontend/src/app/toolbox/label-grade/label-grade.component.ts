import { Component, Input } from '@angular/core';

@Component({
  selector: 'label-grade',
  template: `
  <div class="dialogue-tbl-progress">
  	<div [style.background-color]="grade | gradeToColor">{{ grade | number:'1.0-1' }}</div>
  </div>`,
  styleUrls: ['./label-grade.component.css']
})
export class LabelGradeComponent  {
  @Input() grade : number;
}
