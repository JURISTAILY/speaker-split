import { Component, Input } from '@angular/core';

import { CallDetail } from '../models';

import { gradeToColor } from '../utils';

@Component({
  selector: 'app-dialogue-details-table',
  templateUrl: './dialogue-details-table.component.html',
  styleUrls: ['./dialogue-details-table.component.css']
})
export class DialogueDetailsTableComponent  {
  @Input() details : CallDetail[];

  // Static proxy method.
  gradeToColor = gradeToColor;

  open: boolean[] = [];

  switchDetails(item): void {
    this.open[item] = !this.open[item];
  }

}
