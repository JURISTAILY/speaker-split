import { Component, Input } from '@angular/core';

import { CallDetail } from '../models';

@Component({
  selector: 'dialogue-details-table',
  template: `<h3>Основные проблемы разговора</h3>
<div class = "dialogue-info">
	<table>
		<tbody>
			<tr *ngFor="let detail of details" [class.dialogue-info-group]="detail.isGroup">
				<td [attr.colspan]="(detail.isGroup ? 2 : null)"><img *ngIf="detail.isGroup" src="img/close.png" alt="show" />{{ detail.title }}</td>
				<td *ngIf="!detail.isGroup">{{ detail.value }}</td>
				<td>
					<div class="progress dialogue-info-progress">
						<div class="progress-bar" role="progressbar" [attr.aria-valuenow]="detail.grade" aria-valuemin="0" aria-valuemax="10" [style.width]="(detail.grade + '0%')"></div>
					</div>
				</td>
				<td>{{ detail.grade }} балл{{ (detail.grade == 1 ? "" : (detail.grade > 1 && detail.grade < 5 ? "а" : "ов")) }}</td>
			</tr>
		</tbody>
	</table>
</div>`
})
export class DialogueDetailsTableComponent  {
	@Input() details : CallDetail[];
}
