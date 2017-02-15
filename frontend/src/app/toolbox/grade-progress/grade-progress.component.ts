import { Component, Input } from '@angular/core';

@Component({
  selector: 'grade-progress',
  template: `
<div class="progress dialogue-info-progress">
	<div [style.background-color]="grade | gradeToColor" class="progress-bar" role="progressbar" [attr.aria-valuenow]="grade" aria-valuemin="0" aria-valuemax="10" [style.width.%]="grade | gradeToPercent"></div>
</div>`,
  styleUrls: ['./grade-progress.component.css']
})
export class GradeProgressComponent {
	@Input() grade : number;
}
