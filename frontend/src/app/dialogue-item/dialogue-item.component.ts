import { Component, Input, Output, EventEmitter } from '@angular/core';

import { Call } from '../models';
import { DialogueViewComponent } from '../dialogue-view/dialogue-view.component'

@Component({
  selector: '[app-dialogue-item]',
  templateUrl: './dialogue-item.component.html',
  styleUrls: ['./dialogue-item.component.css']
})
export class DialogueItemComponent  {
  columns = DialogueViewComponent.COLUMNS;
  @Input() call: Call;
  @Output() onToggled : EventEmitter<any> = new EventEmitter<any>();
  @Input() isOpen : boolean;
  
  switchDetails(): void {
    this.onToggled.emit(null);
  }
}
