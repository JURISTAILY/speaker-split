import { Component, ViewEncapsulation, OnInit } from '@angular/core';
import { DecimalPipe, PercentPipe } from '@angular/common'

import { Call } from '../models';
import { CallService } from '../call.service';

import {
  TimeNumberPipe
} from '../toolbox/time-number.pipe'

export class ColumnDescription {
  readonly title : string;
  readonly pipe : any;
  readonly jsonKey : string;
}

@Component({
  selector: 'app-dialogue-view',
  templateUrl: './dialogue-view.component.html',
  styleUrls: ['./dialogue-view.component.css'],
  encapsulation : ViewEncapsulation.None,
})
export class DialogueViewComponent implements OnInit {
  calls: Call[];
  private currentOpen : number = -1;
  static readonly COLUMNS : Array<ColumnDescription> = [
    {
      title : "Длительность разговора",
      pipe : new TimeNumberPipe(),
      jsonKey : "duration"
    },
    {
      title : '<span class="dialogue-sa">SA<img src="assets/img/interrogatory.png" alt="interrogatory" title="Tooltip on right" /></span>',
      pipe : new DecimalPipe('rus'),
      jsonKey : "sa"
    },
    {
      title : "Доля речи оператора",
      pipe : new PercentPipe('rus'),
      jsonKey : "operator_speech_percent"
    },
    {
      title : "Длительность речи оператора",
      pipe : new TimeNumberPipe(),
      jsonKey : "operator_speech_duration"
    },
    {
      title : "Клиент перебивает оператора",
      pipe : new DecimalPipe('rus'),
      jsonKey : "client_interruptions"
    },
    {
      title : "Оператор перебивает клиента",
      pipe : new DecimalPipe('rus'),
      jsonKey : "operatorInterruptions"
    },
    {
      title : "Молчание оператора",
      pipe : new TimeNumberPipe(),
      jsonKey : "operator_silence_duration"
    },
    {
      title : "Разборчивость речи оператора",
      pipe : new PercentPipe('rus'),
      jsonKey : "legibility"
    }
  ];

  columns = DialogueViewComponent.COLUMNS;

  constructor(private callService: CallService) { }

  getCalls(): void {
    this.callService.getCalls().then(calls => this.calls = calls);
  }

  ngOnInit(): void {
    this.getCalls();
  }

  closeOther(who : any) : void {
    console.log(who);
  }

  toggleItem(who : number) {
    this.currentOpen = this.currentOpen === who ? -1 : who;
  }
}
