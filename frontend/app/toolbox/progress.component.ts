import { Component } from '@angular/core';

@Component({
  selector: 'progress-bar',
  template: `<div class="progress dialogue-info-progress">
	<div class="progress-bar" role="progressbar" aria-valuenow="{{ now }}" aria-valuemin="{{ min }}" aria-valuemax="{{ max }}" style="width:40%"></div>
</div>`
})
export class AppComponent  {
	min = 0;
	max = 10;
	//scale = d3.scale.linear().domain([0,10]).range([0,100]);
}
