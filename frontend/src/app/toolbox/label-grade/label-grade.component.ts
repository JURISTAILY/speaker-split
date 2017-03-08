import { Component, Input } from '@angular/core';

declare var isNaN: any;

@Component({
  selector: 'label-grade',
  templateUrl: './label-grade.component.html',
  styleUrls: ['./label-grade.component.css']
})
export class LabelGradeComponent  {
  isNaN = isNaN;

  @Input() grade : number;
}
