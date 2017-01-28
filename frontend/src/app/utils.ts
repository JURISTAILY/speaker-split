declare var d3: any;

const COLORS = ["#63be7b", "#ffd963", "#fc5456"];
const MAGIC_NUMBERS = [10, 6, 1];
const progressScale = d3.scale.linear().range(COLORS).domain(MAGIC_NUMBERS);

export function gradeToColor(grade: number): string {
  return progressScale(grade);
}
