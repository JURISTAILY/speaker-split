import { Component, Input, Output, EventEmitter } from '@angular/core';

import { Call } from '../models';
import { ColumnDescription } from '../dialogue-view/column-description'

@Component({
  selector: '[dialogue-item]',
  templateUrl: './dialogue-item.component.html',
  styleUrls: ['./dialogue-item.component.css']
})
export class DialogueItemComponent  {
  columns = ColumnDescription.DIALOGUE_VIEW_COLUMNS;
  @Input() call: Call;
  @Output() onToggled : EventEmitter<any> = new EventEmitter<any>();
  @Input() isOpen : boolean;

  switchDetails(): void {
    this.onToggled.emit(null);
  }
}
