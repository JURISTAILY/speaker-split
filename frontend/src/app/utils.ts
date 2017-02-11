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