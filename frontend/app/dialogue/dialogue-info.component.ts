import { Component, Input, ViewEncapsulation } from '@angular/core';

import { Info } from '../models';

@Component({
  selector: '[dialogue-info]',
  template: `
<tr>
	<td>{{ call.id }}</td>
	<td>{{ call.duration }}</td>
	<td>{{ call.sa }}</td>
	<td>{{ (call.operatorSpeechDuration / call.duration * 1000) / 10 | number: '1.1-1' }}%</td>
	<td>{{ call.operatorSpeechDuration }}</td>
	<td>{{ call.clientInterruptions }}</td>
	<td>{{ call.operatorInterruptions }}</td>
	<td>{{ call.operatorSilenceDuration }}</td>
	<td>{{ call.legibility }}%</td>

	<td><div [class.incoming]="call.isIncoming" [class.outgoing]="!call.isIncoming"></div></td>

	<td><div class="dialogue-tbl-progress"><div>{{ call.grade }}</div></div></td>
	<td><span class="dialogue-tbl-info-trigger" (click)="switchDetails()">{{ (open ? "Свернуть" : "Развернуть") }}</span></td>
</tr>
<tr *ngIf="open">
	<td colspan="12">
		<dialogue-details [call]="call"></dialogue-details>
	</td>
</tr>
`
})
export class DialogueInfoComponent  {
	@Input() info: Info;
}
