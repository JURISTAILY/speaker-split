declare var d3: any;

export function gradeToColor(grade: number): string {
	const COLORS = ["#63be7b", "#ffd963", "#fc5456"];
	const COLOR_GRADIENT_LINEAR_NODES = [10, 6, 1];
	const GRADE_TO_COLOR_SCALE = d3.scale.linear().range(COLORS).domain(COLOR_GRADIENT_LINEAR_NODES);
	return GRADE_TO_COLOR_SCALE(grade);
}

export function rusNumberTermination(num : number) : string {
	//Балл['a'|'ов'|''] termination pick
	if (!isFinite(num)) {
		return 'ов';
	}
	if (num == Math.floor(num)) {
		return (num == 1 ? '' : (num > 1 && num < 5 ? 'а' : 'ов'));
	}
	return 'a';
}

export function gradeToPercent(grade : number) : number {
	const GRADE_TO_PERCENT_SCALE = d3.scale.linear().range([0, 100]).domain([0, 10]);
	return GRADE_TO_PERCENT_SCALE(grade);
}

export function numberToPercentsString(s : number) : string {
	return numberToString(s * 100) + ' %';
}

export function picesToString(s : number) : string {
	return numberToString(s) + ' раз';
}

export function numberToString(s : number) : string {
	return s.toString();
}

export function boolToCallDirectionLabel(isIncoming : boolean) : string {
    return '<label-call-direction isIncoming="' + isIncoming + '"></label-call-direction>';
}

export function gradeToGradeLabel(grade : number) : string {
    return '<label-grade grade="' + grade + '"></label-grade>';
}
