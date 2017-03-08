import { Component, OnInit, ElementRef } from '@angular/core';

import { NaNUniformerPipe } from '../nanuniformer.pipe'

declare var d3: any;

@Component({
  selector: 'hexagon',
  templateUrl: './hexagon.component.html',
  styleUrls: ['./hexagon.component.css']
})
export class HexagonComponent implements OnInit {

  constructor(
    private elementRef: ElementRef
  ) { }

  static readonly R = 100;
  static readonly GONALITY = 6;

  ngOnInit() {
    let r = HexagonComponent.R;
    let gonality = HexagonComponent.GONALITY;
    let anglesD = [];
    for (let i = 0; i < gonality; ++i) {
        anglesD.push(i * 360 / gonality);
    }
    let segmentPath = d3.path();
    segmentPath.moveTo(0, 0);
    segmentPath.lineTo( Math.cos(Math.PI / gonality * 2) * r, -Math.sin(Math.PI / gonality * 2) * r);
    segmentPath.lineTo(-Math.cos(Math.PI / gonality * 2) * r, -Math.sin(Math.PI / gonality * 2) * r);
    segmentPath.closePath();
    let circlePath = d3.path();
    circlePath.moveTo(r, 0);
    for (let i = Math.PI / gonality * 2; i < Math.PI * 1.999; i += Math.PI / gonality * 2) {
        circlePath.lineTo(Math.cos(i) * r, Math.sin(i) * r)
    }
    circlePath.closePath();

    let grade = []
    for (let i = 0; i < gonality; ++i) {
        grade.push(Math.random() * 9 + 1);
    }
    let gradePoints = []
    for (let i = 0; i < grade.length; ++i) {
        gradePoints.push({ 
            x : Math.cos(i * Math.PI / gonality * 2) * r * grade[i] / 10, 
            y : Math.sin(i * Math.PI / gonality * 2) * r * grade[i] / 10
        });
        console.log(grade[i], gradePoints[i].x);
    }

    let gradePath = d3.path();
    gradePath.moveTo(gradePoints[0].x,gradePoints[0].y);
    for (let i = 1; i < grade.length; ++i) {
        gradePath.lineTo(gradePoints[i].x,gradePoints[i].y);
    }
    gradePath.closePath();


    let svg = d3.select(this.elementRef.nativeElement).select("svg");
    let g = svg.append("g").attr("transform","translate(" + r + "," + r * Math.sin(Math.PI / gonality * 2) + ")");


    g.append("g").selectAll("g").data(anglesD).enter().append("g")
      .attr("transform", function(d) { return "rotate(" + d + ")"; })
      .append("path").style("stroke","#2696f9").attr("d", segmentPath.toString()).attr("fill", "url(#linear-gradient)")

    g.append("g").selectAll("g").data([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]).enter().append("g")
      .attr("transform", function(d) { return "scale(" + d + ")"; }).style("fill", "none")
      .append("path").style("stroke","#2696f9").attr("d", circlePath.toString())

    let textG = g.append("g");
    let textR = r * 1.1;
    function textItm(angle) { return textG.append("text").attr("alignment-baseline","middle")
      .style("font-size", 18).attr("x", Math.cos(angle) * textR).attr("y", Math.sin(angle) * textR); }
    textItm(0              ).html("Длительность разговора")
    textItm(Math.PI / 3    ).html("Разборчивость")
    textItm(Math.PI / 3 * 2).html("Перебивания").attr("text-anchor","end")
    textItm(Math.PI        ).html("Вежливость").attr("text-anchor","end")
    textItm(Math.PI / 3 * 4).html("Эффективность").attr("text-anchor","end")
    textItm(Math.PI / 3 * 5).html("Внимательность")

    let tooltip;
    let hideTooltip = function() {
      tooltip.transition().style("opacity", "0");
    }
    let takeTooltip = function(text, pos) {
      tooltip.attr("x", pos.x + 10).attr("y", pos.y).text(text).transition().style("opacity", "1");
    }
    g.append("path").attr("d", gradePath.toString())
      .style("stroke","#2696f9")
      .style("stroke-width", 2)
      .style("fill", "#2696f9")
      .style("fill-opacity", ".3");
    g.append("g").selectAll("circle").data(grade).enter().append("circle")
      .attr("cx", function(d, id) { return gradePoints[id].x; })
      .attr("cy", function(d, id) { return gradePoints[id].y; })
      .attr("r", 5)
      .style("stroke-width", 2)
      .style("stroke","#2696f9")
      .style("fill", "#FFFFFF")
      .on("mouseover", function(d, id) { d3.select(this).transition().attr("r", 8); takeTooltip(NaNUniformerPipe.TRANSFORMER.transform(d, '1.0-1'), gradePoints[id]); })
      .on("mouseout", function() { d3.select(this).transition().attr("r", 5); hideTooltip(); });

    tooltip = g.append("text")
      .style("stroke-width", 0.5)
      .style("font-size", 18)
        .style("fill","#000000");
  }

}
