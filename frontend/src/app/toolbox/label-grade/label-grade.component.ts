import { Component, Input, ElementRef, OnInit } from '@angular/core';

declare var d3: any;
declare var isNaN: any;

@Component({
  selector: 'label-grade',
  templateUrl: './label-grade.component.html',
  styleUrls: ['./label-grade.component.css']
})
export class LabelGradeComponent implements OnInit  {
  isNaN = isNaN;

  @Input() grade : number;

  private labelNode;

  constructor(
    private elementRef: ElementRef
  ) {}

  ngOnInit() {
    this.labelNode = d3.select(this.elementRef.nativeElement).select(".value").node();
  }

  mouseover(event, me) {
    this.labelNode.style.zIndex = 100;
  }

  mouseout(event, me) {
    this.labelNode.style.zIndex = 1;
  }
}
