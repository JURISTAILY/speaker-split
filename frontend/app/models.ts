export class Transcript
{

}

export class Info {
	isGroup : boolean;
	title : string;
	value : number;
	grade : number;	
}

export class Call {
	id: string;
	duration : number;
	sa : number;
	operatorSpeechDuration : number;
	clientInterruptions : number;
	operatorInterruptions : number;
	operatorSilenceDuration : number;
	legibility : number;
	isIncoming : boolean;
	grade : number;
	transcripts : Transcript[];
}

