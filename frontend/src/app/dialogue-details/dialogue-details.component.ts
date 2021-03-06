import { Component, Input, ViewEncapsulation } from '@angular/core';

import { Call } from '../models';

@Component({
  selector: 'dialogue-details',
  templateUrl: './dialogue-details.component.html',
  styleUrls: ['./dialogue-details.component.css'],
  encapsulation : ViewEncapsulation.None
})
export class DialogueDetailsComponent  {
  @Input() call : Call;

  haveDebug() : boolean {
  	return typeof this.call.debug === 'object';
  }
}
