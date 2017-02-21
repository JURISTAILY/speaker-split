import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
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
    GradePipe
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [CallService],
  bootstrap: [AppComponent]
})
export class AppModule { }
