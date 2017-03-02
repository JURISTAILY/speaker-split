import { Pipe, PipeTransform } from '@angular/core';

declare var d3: any;

@Pipe({name: 'gradeToPercent'})
export class GradePercentPipe implements PipeTransform {
  transform(grade: number): string {
    const GRADE_TO_PERCENT_SCALE = d3.scaleLinear().range([0, 100]).domain([0, 10]);
    return GRADE_TO_PERCENT_SCALE(grade);
  }
}
