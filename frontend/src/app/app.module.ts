import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app/app.component';
import { DialogueViewComponent } from './dialogue-view/dialogue-view.component';
import { DialogueItemComponent } from './dialogue-item/dialogue-item.component';
import { DialogueDetailsComponent } from './dialogue-details/dialogue-details.component';
import { DialogueDetailsTableComponent } from './dialogue-details-table/dialogue-details-table.component';
import { DialogueDetailsTranscriptComponent } from './dialogue-details-transcript/dialogue-details-transcript.component';
import { DialogueDetailsPlayerComponent } from './dialogue-details-player/dialogue-details-player.component';
import { CallService } from './call.service';
import { LabelCallDircetionComponent } from './toolbox/label-call-direction/label-call-direction.component';
import { LabelGradeComponent } from './toolbox/label-grade/label-grade.component';
import { TimeNumberPipe } from './toolbox/time-number.pipe'
import { GradePercentPipe } from './toolbox/grade-percent.pipe'
import { GradeColorPipe } from './toolbox/grade-color.pipe';
import { GradeProgressComponent } from './toolbox/grade-progress/grade-progress.component';
import { GradePipe } from './toolbox/grade.pipe';
import { ValuePipe } from './toolbox/value.pipe';
import { RouterModule, Routes } from '@angular/router';
import { CallDebugComponent } from './call-debug/call-debug.component';
import { MainMenuComponent } from './main-menu/main-menu.component';
import { ReportComponent } from './report/report.component';
import { UnavailableComponent } from './unavailable/unavailable.component';
import { NaNUniformerPipe } from './toolbox/nanuniformer.pipe';
import { DialogueMaskViewComponent } from './dialogue-mask-view/dialogue-mask-view.component';

const appRoutes : Routes = [
  { path: 'debug/:fileName', component: CallDebugComponent },
  {
    path: '',
    redirectTo: '/report',
    pathMatch: 'full'
  },
  {
    path: 'report',
    component: ReportComponent
  },
  { path: '**', component: UnavailableComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    DialogueViewComponent,
    DialogueItemComponent,
    DialogueDetailsComponent,
    DialogueDetailsTableComponent,
    DialogueDetailsTranscriptComponent,
    DialogueDetailsPlayerComponent,
    LabelCallDircetionComponent,
    LabelGradeComponent,
    TimeNumberPipe,
    GradeColorPipe,
    GradePercentPipe,
    GradeProgressComponent,
    GradePipe,
    ValuePipe,
    CallDebugComponent,
    MainMenuComponent,
    ReportComponent,
    UnavailableComponent,
    NaNUniformerPipe,
    DialogueMaskViewComponent
  ],
  imports: [
    RouterModule.forRoot(appRoutes),
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [CallService],
  bootstrap: [AppComponent]
})
export class AppModule { }
