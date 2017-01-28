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

@NgModule({
  declarations: [
    AppComponent,
    DialogueViewComponent,
    DialogueItemComponent,
    DialogueDetailsComponent,
    DialogueDetailsTableComponent,
    DialogueDetailsTranscriptComponent,
    DialogueDetailsPlayerComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }