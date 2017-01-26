import { Component, ViewEncapsulation } from '@angular/core';
import { Call } from '../models';


const CALLS: Call[] = [
	{
		id: "#0157",
		duration : 545,
		sa : 123,
		operatorSpeechDuration : 123,
		clientInterruptions : 3,
		operatorInterruptions : 34,
		operatorSilenceDuration : 441,
		legibility : 80,
		isIncoming : true,
		grade : 8,
		transcripts : []
	},
	{
		id: "#0158",
		duration : 1235,
		sa : 154323,
		operatorSpeechDuration : 312542,
		clientInterruptions : 351234,
		operatorInterruptions : 34143,
		operatorSilenceDuration : 4312423,
		legibility : 35,
		isIncoming : false,
		grade : 4,
		transcripts : []
	},
	{
		id: "#0159",
		duration : 545,
		sa : 123,
		operatorSpeechDuration : 123,
		clientInterruptions : 3,
		operatorInterruptions : 34,
		operatorSilenceDuration : 441,
		legibility : 99,
		isIncoming : true,
		grade : 5,
		transcripts : []
	}
];

@Component({
  selector: 'dialogue-view',
  template: `<table class="dialogue-view">
	<thead>
		<tr>
			<td>Название среза</td>
			<td>Длительность разговора</td>
			<td class="dialogue-sa">
				SA<img src="img/interrogatory.png" alt="interrogatory" title="Tooltip on right" />
			</td>
			<td>Доля речи оператора</td>
			<td>Длительность речи оператора</td>
			<td>Клиент перебивает оператора</td>
			<td>Оператор перебивает клиента</td>
			<td>Молчание оператора</td>
			<td>Разборчивость речи оператора</td>
			<td>Тип</td>
			<td>Оценка разговора</td>
			<td>Запись разговора</td>
		</tr>
	</thead>
	<tbody dialogue-item *ngFor="let call of calls" [call]="call">
	</tbody>
</table>
тут скачаю .xls`,
	styleUrls: ["app/dialogue/dialogue-view.component.css"],
	encapsulation : ViewEncapsulation.None
})
export class DialogueViewComponent  {
	calls = CALLS;
}
