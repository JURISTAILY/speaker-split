import { Component, Input } from '@angular/core';

import { CallSource } from '../models';

@Component({
  selector: 'dialogue-details-player',
  template: `<h3>Запись звонка</h3>
<div style="height:187px;"> 
<audio controls preload>
	<source *ngFor="let source of sources" src="{{ source.source }}">
</audio>
</div>`
})
export class DialogueDetailsPlayerComponent  {
	@Input() sources : CallSource[];
}
