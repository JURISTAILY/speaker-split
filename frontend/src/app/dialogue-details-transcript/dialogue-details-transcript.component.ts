import { Component, Input } from '@angular/core';

import { CallTranscript } from '../models';

@Component({
  selector: 'dialogue-details-transcript',
  templateUrl: './dialogue-details-transcript.component.html',
  styleUrls: ['./dialogue-details-transcript.component.css']
})
export class DialogueDetailsTranscriptComponent  {
  @Input() transcripts : CallTranscript[];
}
