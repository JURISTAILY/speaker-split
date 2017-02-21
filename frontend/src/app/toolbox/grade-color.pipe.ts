import { Pipe, PipeTransform } from '@angular/core';

declare var d3: any;

@Pipe({name: 'gradeToColor'})
export class GradeColorPipe implements PipeTransform {
  transform(grade: number): string {
    const COLORS = ["#63be7b", "#ffd963", "#fc5456", "#000000"];
    const COLOR_GRADIENT_LINEAR_NODES = [10, 6, 1, 0];
    const GRADE_TO_COLOR_SCALE = d3.scale.linear().range(COLORS).domain(COLOR_GRADIENT_LINEAR_NODES);
    return GRADE_TO_COLOR_SCALE(grade);
  }
}