import { Component, ViewEncapsulation, OnInit, Input } from '@angular/core';

import { Call } from '../models';
import { CallService } from '../call.service';

import { TimeNumberPipe } from '../toolbox/time-number.pipe';

import { ColumnDescription } from './column-description';

@Component({
  selector: 'dialogue-view',
  templateUrl: './dialogue-view.component.html',
  styleUrls: ['./dialogue-view.component.css'],
  encapsulation : ViewEncapsulation.None,
})
export class DialogueViewComponent implements OnInit {
  calls: Call[] = [];
  private currentOpen : number;

  @Input() debugCall : string = '';
  @Input() open : number = -1;

  private columns = ColumnDescription.DIALOGUE_VIEW_COLUMNS;

  constructor(private callService: CallService) { }

  getCalls(): void {
    var call;
    if (this.debugCall) {
      call = this.callService.getComputedCallDebug(this.debugCall);
    } else {
      call = this.callService.getCalls();
    }
    call.then(calls => this.takeData(calls));
  }

  private takeData(data : Array<Call>) {
    this.calls = data;
  }

  ngOnInit(): void {
    this.getCalls();
    this.toggleItem(this.open);
  }

  toggleItem(who : number) {
    if (this.open >= 0) {
      this.currentOpen = this.open;
    } else {
      this.currentOpen = this.currentOpen === who ? -1 : who;
    }
  }
}
