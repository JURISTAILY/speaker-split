import { Component, Input } from '@angular/core';

import { Call } from '../models';
import { gradeToColor } from '../utils';

@Component({
  selector: '[app-dialogue-item]',
  templateUrl: './dialogue-item.component.html',
  styleUrls: ['./dialogue-item.component.css']
})
export class DialogueItemComponent  {
  @Input() call: Call;
  open: boolean = false;
  switchDetails(): void {
    this.open = !this.open;
  }

  // Static proxy method.
  gradeToColor = gradeToColor;

}
