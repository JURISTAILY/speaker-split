import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent }  from './app.component';
import { DialogueViewComponent } from './dialogue/dialogue-view.component';
import { DialogueItemComponent } from './dialogue/dialogue-item.component';
import { DialogueDetailsComponent } from './dialogue/dialogue-details.component';

@NgModule({
  imports:      [ BrowserModule ],
  declarations: [ AppComponent, DialogueViewComponent, DialogueItemComponent, DialogueDetailsComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
