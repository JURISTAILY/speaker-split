import { Component, Input } from '@angular/core';

import { CallDetail } from '../models';

@Component({
  selector: 'app-dialogue-details-table',
  templateUrl: './dialogue-details-table.component.html',
  styleUrls: ['./dialogue-details-table.component.css']
})
export class DialogueDetailsTableComponent  {
  @Input() details : CallDetail[];
}

