import { Component, Input, ElementRef, OnInit } from '@angular/core';

declare var d3: any;

@Component({
  selector: 'dialogue-mask-view',
  templateUrl: './dialogue-mask-view.component.html',
  styleUrls: ['./dialogue-mask-view.component.css']
})
export class DialogueMaskViewComponent implements OnInit {

  constructor(
    private elementRef: ElementRef
  ) { }

  array : Array<Array<number>> = [];
  defRole : number = -1;
  length : number = 0;

  private init() {
    if (!this.array.length) {
      return;
    }
    let svg = d3.select(this.elementRef.nativeElement).select("svg");
    let frameWidth = parseFloat(svg.style("width").slice(0,-2));
    let scale = d3.scaleLinear()
      .domain([0, this.length])
      .range([0, frameWidth]);

    let curPos = 0;
    svg.append("g").selectAll("rect").data(this.array).enter().append("rect")
      .attr("x", d => {
        let result = curPos;
        curPos += d[1];
        return scale(result);
      })
      .attr("width", d => scale(d[1]))
      .attr("height", 50)
      .style("fill", d => {
        switch(d[0] >= 0 ? d[0] : this.defRole) {
          case 0:
            return "#008888"
          case 1:
            return "#008800"
          case 2:
            return "#000088"
          case 3:
            return "#880000"
          case -1: default:
            return "#888888"
        }
      })
  }

  @Input() set role(value) {
    this.defRole = value;
    this.init();
  }

  private static compress(data : Array<boolean>) : Array<Array<number>> {
    let result = [];
    let prev = data[0];
    let duration = 0;
    for (let cur of data) {
      if (cur != prev){
        result.push([prev ? -1 : 0, duration]);
        prev = cur;
        duration = 1;
      } else {
        ++duration;
      }
    }
    result.push([prev ? -1 : 0, duration]);
    return result;
  }

  onResize(arg) {
    this.init();
  }

  @Input() set data(value : Array<any>) {
    if (typeof value[0] === "boolean") {
      value = DialogueMaskViewComponent.compress(value);
    }
    this.array = value;

    this.length = 0;
    for (let item of this.array) {
      this.length += item[1];
    }

    this.init();
  }

}
