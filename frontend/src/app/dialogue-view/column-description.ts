import { TimeNumberPipe } from '../toolbox/time-number.pipe'
import { NaNUniformerPipe } from '../toolbox/nanuniformer.pipe'

export class ColumnDescription {
  readonly title : string;
  readonly pipe : any;
  readonly jsonKey : string;

  static readonly DIALOGUE_VIEW_COLUMNS : Array<ColumnDescription> = [
    {
      title : "Длительность разговора",
      pipe : new TimeNumberPipe(),
      jsonKey : "duration"
    },
    {
      title : '<span class="dialogue-sa">SA<img src="assets/img/interrogatory.png" alt="interrogatory" title="Tooltip on right" /></span>',
      pipe : NaNUniformerPipe.TRANSFORMER,
      jsonKey : "sa"
    },
    {
      title : "Доля речи оператора",
      pipe : NaNUniformerPipe.PERCENT_TANSFORMER,
      jsonKey : "operator_speech_ratio"
    },
    {
      title : "Длительность речи оператора",
      pipe : new TimeNumberPipe(),
      jsonKey : "operator_speech_duration"
    },
    {
      title : "Клиент перебивает оператора",
      pipe : NaNUniformerPipe.TRANSFORMER,
      jsonKey : "client_interruptions_count"
    },
    {
      title : "Оператор перебивает клиента",
      pipe : NaNUniformerPipe.TRANSFORMER,
      jsonKey : "operator_interruptions_count"
    },
    {
      title : "Молчание оператора",
      pipe : new TimeNumberPipe(),
      jsonKey : "operator_silence_duration"
    },
    {
      title : "Разборчивость речи оператора",
      pipe : NaNUniformerPipe.PERCENT_TANSFORMER,
      jsonKey : "legibility_ratio"
    }
  ];
}
