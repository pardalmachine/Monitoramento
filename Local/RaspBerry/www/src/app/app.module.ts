import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LOCALE_ID, NgModule } from '@angular/core';
import { registerLocaleData } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';


import { FormsModule, ReactiveFormsModule } from '@angular/forms';


import localePt from '@angular/common/locales/pt';
registerLocaleData(localePt);

import { DadosService } from './dados-Service';

import { AppComponent } from './app.component';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    FormsModule, ReactiveFormsModule,
    BrowserModule, BrowserAnimationsModule, HttpClientModule,

  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'pt' }, DadosService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
