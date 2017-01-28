export class CallDetail {
    isGroup : boolean;
    title : string;
    value : string;
    grade : number;
}

export class CallTranscript {
    isOperator: boolean;
    transcript: string;
}

export class CallSource {
    source : string;
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
    transcripts : CallTranscript[];
    details : CallDetail[];
    sources : CallSource[];
}
