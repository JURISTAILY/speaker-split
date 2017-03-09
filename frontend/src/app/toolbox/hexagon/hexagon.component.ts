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
    }

    let gradePath = d3.path();
    gradePath.moveTo(gradePoints[0].x,gradePoints[0].y);
    for (i = 1; i < grade.length; ++i) {
      gradePath.lineTo(gradePoints[i].x,gradePoints[i].y);
    }
    gradePath.closePath();

    let tooltipPath = d3.path();
    tooltipPath.moveTo(0,0);
    tooltipPath.lineTo( Math.cos(Math.PI / gonality * 2) * r, -Math.sin(Math.PI / gonality * 2) * r);
    tooltipPath.lineTo(0, -r);
    tooltipPath.lineTo(-Math.cos(Math.PI / gonality * 2) * r, -Math.sin(Math.PI / gonality * 2) * r);
    tooltipPath.closePath();

    let svg = d3.select(this.elementRef.nativeElement).select("svg");
    let g = svg.append("g").attr("transform","translate(" + r + "," + r * Math.sin(Math.PI / gonality * 2) + ")");

    let axesLable = [
      "Длительность разговора",
      "Разборчивость",
      "Перебивания",
      "Вежливость",
      "Эффективность",
      "Внимательность"
    ]

    g.append("g").selectAll("g").data(anglesD).enter().append("g")
      .attr("transform", function(d) { return "rotate(" + d + ")"; })
      .append("path").style("stroke","#2696f9").attr("d", segmentPath.toString()).attr("fill", "url(#linear-gradient)")

    g.append("g").selectAll("g").data([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]).enter().append("g")
      .attr("transform", function(d) { return "scale(" + d + ")"; }).style("fill", "none")
      .append("path").style("stroke","#2696f9").attr("d", circlePath.toString())

    g.append("path").attr("d", gradePath.toString())
        .style("stroke","#2696f9")
      .style("stroke-width", 2)
      .style("fill", "#2696f9")
      .style("fill-opacity", ".3");

    function BuildTooltip() {
      let billet = g.append("rect")
        .attr("fill", "white")
        .attr("rx", "5")
        .attr("ry", "10")
        .style("stroke-width", "2px")
        .style("stroke", "#2696f9")
        .style("pointer-events", "none");
      let tooltip = g.append("text")
        .style("stroke-width", 0.5)
        .style("font-size", 16)
          .style("fill","#000000")
        .style("pointer-events", "none");
      tooltip.billet = billet;
      tooltip.take = function(text, pos) {
        this.attr("x", pos.x + 20).attr("y", pos.y).text(text).transition().style("opacity", "1");
        let box = this.node().getBBox()
        this.billet.attr("width", box.width + 14)
          .attr("height", box.height + 6)
          .attr("x", box.x - 7)
          .attr("y", box.y - 2).transition().style("opacity", "1");
      };
      tooltip.hide = function() {
        this.transition().style("opacity", "0");
        this.billet.transition().style("opacity", "0");
      };
      return tooltip;
    }
    let axisTooltips;
    let tooltip;

    g.append("g").selectAll("path").data(anglesD).enter().append("path")
      .attr("d", tooltipPath.toString())
      .attr("transform", function(d) { return "rotate(" + (d + 540 / gonality) + ")" })
      .style("opacity", "0")
      .on("mouseover", function(d, id) { 
        axisTooltips[id].take(axesLable[id], axisTooltips[id].pos);
      })
      .on("mouseout", function(d, id) { axisTooltips[id].hide(); });

    g.append("g").selectAll("circle").data(grade).enter().append("circle")
      .attr("cx", function(d, id) { return gradePoints[id].x; })
      .attr("cy", function(d, id) { return gradePoints[id].y; })
      .attr("r", 5)
      .style("stroke-width", 2)
        .style("stroke","#2696f9")
      .style("fill", "#FFFFFF")
      .on("mouseover", function(d, id) { 
        d3.select(this).transition().attr("r", 8); tooltip.take(NaNUniformerPipe.TRANSFORMER.transform(d, '1.0-1'), gradePoints[id]); 
        axisTooltips[id].take(axesLable[id], axisTooltips[id].pos);
      })
      .on("mouseout", function(d, id) { d3.select(this).transition().attr("r", 5); tooltip.hide(); axisTooltips[id].hide() });

    axisTooltips = [];
    for (var i = 0; i < gonality; ++i) {
      axisTooltips.push(BuildTooltip());
      if (anglesD[i] > 90 && anglesD[i] < 270) {
        axisTooltips[i].attr("text-anchor","end");
      }
      axisTooltips[i].pos = {
        x : Math.cos(anglesD[i] / 180 * Math.PI) * r - (anglesD[i] > 90 && anglesD[i] < 270 ? (anglesD[i] > 160 && anglesD[i] < 200 ? 30 : 40) : 0),
        y : Math.sin(anglesD[i] / 180 * Math.PI) * r
      };
    }
    tooltip = BuildTooltip();
  }

}
