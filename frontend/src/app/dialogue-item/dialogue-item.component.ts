import { Component, Input } from '@angular/core';

import { Call } from '../models';


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


}
