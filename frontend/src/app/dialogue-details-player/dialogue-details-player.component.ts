import { Component, Input } from '@angular/core';

import { CallSource } from '../models';

@Component({
  selector: 'dialogue-details-player',
  templateUrl: './dialogue-details-player.component.html',
  styleUrls: ['./dialogue-details-player.component.css']
})
export class DialogueDetailsPlayerComponent  {
  @Input() id : number;
}
