import { Component, Input } from '@angular/core';

import { CallSource } from '../models';
import { environment } from '../../environments/environment';

@Component({
  selector: 'dialogue-details-player',
  templateUrl: './dialogue-details-player.component.html',
  styleUrls: ['./dialogue-details-player.component.css']
})
export class DialogueDetailsPlayerComponent  {
  PATHS = environment.playerSourcesPaths
  API_URL = environment.apiUrl
  @Input() id : number;
}
