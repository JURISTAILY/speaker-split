import { Component, ViewEncapsulation, OnInit } from '@angular/core';

import { Call } from '../models';
import { CallService } from '../call.service';

@Component({
  selector: 'app-dialogue-view',
  templateUrl: './dialogue-view.component.html',
  styleUrls: ['./dialogue-view.component.css'],
  encapsulation : ViewEncapsulation.None,
})
export class DialogueViewComponent implements OnInit {
  calls: Call[];

  constructor(private callService: CallService) { }

  getCalls(): void {
    this.callService.getCalls().then(calls => this.calls = calls);
  }

  ngOnInit(): void {
    this.getCalls();
  }


}
