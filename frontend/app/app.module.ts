import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent }  from './app.component';
import { DialogueViewComponent } from './dialogue/dialogue-view.component';
import { DialogueItemComponent } from './dialogue/dialogue-item.component';
import { DialogueDetailsComponent } from './dialogue/dialogue-details.component';
import { DialogueDetailsTableComponent } from './dialogue/dialogue-details-table.component';
import { DialogueDetailsPlayerComponent } from './dialogue/dialogue-details-player.component';
import { DialogueDetailsTranscriptComponent } from './dialogue/dialogue-details-transcript.component';

@NgModule({
  imports:      [ BrowserModule ],
  declarations: [ AppComponent, DialogueViewComponent, DialogueItemComponent, DialogueDetailsComponent, DialogueDetailsTableComponent, DialogueDetailsPlayerComponent, DialogueDetailsTranscriptComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
