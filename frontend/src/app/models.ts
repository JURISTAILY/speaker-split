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
    name : string;
    tableValues : any;
    isIncoming : boolean;
    grade : number;
    transcripts : CallTranscript[];
    details : CallDetail[];
    sources : CallSource[];
}
