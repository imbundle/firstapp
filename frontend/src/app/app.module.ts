import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';


import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MdToolbarModule, MdButtonModule } from '@angular/material';
import { NvD3Module } from 'angular2-nvd3';

import { AppComponent } from './app.component';
import { ServerService } from './server.services';
import { ChartComponent } from './chart/chart.component';




@NgModule({
  declarations: [
    AppComponent,
    ChartComponent
  ],
  imports: [
    BrowserModule,
    MdToolbarModule, MdButtonModule,
    HttpModule,
    BrowserAnimationsModule, NvD3Module
  ],
  providers: [ServerService],
  bootstrap: [AppComponent]
})
export class AppModule { }
