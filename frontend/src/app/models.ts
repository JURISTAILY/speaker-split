export class CallDetail {
    children : Array<CallDetail>;
    title : string;
    value : string;
    grade : number;
}

export class CallTranscript {
    isOperator: boolean;
    transcript: string;
    begin : number;
    end : number;
}

export class CallSource {
    source : string;
}

export class Call {
    id : number;
    name: string;
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

    constructor(values : Object) {
        for (let val in values) {
            this[val] = values[val];
        }
    }
}
