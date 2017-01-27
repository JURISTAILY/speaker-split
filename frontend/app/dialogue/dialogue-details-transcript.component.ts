import { Component, Input } from '@angular/core';

import { CallTranscript } from '../models';

@Component({
  selector: 'dialogue-details-transcript',
  template: `<h3>Расшифровка диалога</h3>
<div class="dialogue-script">
	<table>
		<tbody>
			<tr *ngFor="let transcript of transcripts">
				<td [class.dialogue-script-op]="transcript.isOperator" [class.dialogue-script-cl]="!transcript.isOperator">{{ (transcript.isOperator ? "Оператор" : "Клиент") }}:</td>
				<td>{{ transcript.transcript }}</td>
			</tr>
		</tbody>
	</table>
</div>`
})
export class DialogueDetailsTranscriptComponent  {
	@Input() transcripts : CallTranscript[];
}
