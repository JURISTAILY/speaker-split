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

export function setNumToString(s : number) : string {
	let h = Math.floor(s / 3600);
	s -= h * 3600;
	let m = Math.floor(s / 60);
	s -= m * 60;
	let ms = s - Math.floor(s);
	s = Math.floor(s);
	let i = 3;
	while (i && ms != Math.floor(ms)) {
		--i;
		ms *= 10;
	}
	ms = Math.round(ms);
	let result = '';
	if (h) {
		result += h;
		if (m > 9) {
			result += ':' + m;
		} else {
			result += ':0' + m;
		}
		if (s > 9) {
			result += ':' + s;
		} else {
			result += ':0' + s;
		}
	} else if (m) {
		result += m;
		if (s > 9) {
			result += ':' + s;
		} else {
			result += ':0' + s;
		}
	} else {
		result += s;
	}
	if (ms) {
		result += '.' + ms;
	}
	return result;
}
