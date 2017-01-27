import { Component, Input, ViewEncapsulation } from '@angular/core';

import { Call, CallTranscript, CallSource, CallDetail } from '../models';

@Component({
  selector: 'dialogue-details',
  template: `
<div class="dialogue-details container-fluid">
	<div class="row">
		<div class="col-sm">
			<dialogue-details-table [details]="call.details"></dialogue-details-table>
		</div>
		<div class="col-sm">
			<dialogue-details-player [sources]="call.sources"></dialogue-details-player>
			<dialogue-details-transcript [transcripts]="call.transcripts"></dialogue-details-transcript>
		</div>
	</div>
</div>
<div class="dialogue-details-bottom"></div>`,
	styleUrls: ["app/dialogue/dialogue-details.component.css"],
	encapsulation : ViewEncapsulation.None
})
export class DialogueDetailsComponent  {
	@Input() call : Call;
}
