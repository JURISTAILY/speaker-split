import { Component, Input } from '@angular/core';

@Component({
  selector: 'label-call-direction',
  template: '<div [class.incoming]="isIncoming" [class.outgoing]="!isIncoming"></div>',
  styleUrls: ['./label-call-direction.component.css']
})
export class LabelCallDircetionComponent  {
  @Input() isIncoming : boolean;
}
