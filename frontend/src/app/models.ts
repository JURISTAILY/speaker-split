export class CallDetail {
    children : Array<CallDetail>;
    title : string;
    value : number;
    name : string;
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
    transcripts : CallTranscript[];
    details : CallDetail[];
    sources : CallSource[];
    debug : any;
}
