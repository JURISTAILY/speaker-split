import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'call-debug',
  templateUrl: './call-debug.component.html',
  styleUrls: ['./call-debug.component.css']
})
export class CallDebugComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) { }

  fileName : string;

  ngOnInit() {
    this.route.params.forEach(a => this.fileName = a['fileName']);
  }

}
