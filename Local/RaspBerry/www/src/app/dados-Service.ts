
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable } from 'rxjs/Observable';
import { BaseType, ColecaoType, MedicaoType } from './dados.Types';

const httpOptions = { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) };


@Injectable()
export class DadosService {
    constructor(
        private http: HttpClient
    ) { }

    private pathUrl = 'dados';

    databases(): Observable<BaseType[]> {
        const url = `${this.pathUrl}/databases`;
        return this.http.get<BaseType[]>(url);
    }

    collections(prm: any): Observable<ColecaoType[]> {
        const url = `${this.pathUrl}/collections`;
        return this.http.post<ColecaoType[]>(url, prm, httpOptions);
    }

    medicao(prm: any): Observable<MedicaoType[]> {
        const url = `${this.pathUrl}/medicao`;
        return this.http.post<MedicaoType[]>(url, prm, httpOptions);
    }

    valores(prm: any): Observable<any[]> {
        const url = `${this.pathUrl}/valores`;
        return this.http.post<any[]>(url, prm, httpOptions);
    }




}

