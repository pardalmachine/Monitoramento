
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable } from 'rxjs/Observable';
import { SistemaType, ModuloType, UnidadeType, ValorType } from './dados.Types';

const httpOptions = { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) };


@Injectable()
export class DadosService {
    constructor(
        private http: HttpClient
    ) { }

    private pathUrl = 'inf';

    sistemas(): Observable<SistemaType[]> {
        const url = `${this.pathUrl}/sistemas`;
        return this.http.get<SistemaType[]>(url);
    }

    modulos(id: number): Observable<ModuloType[]> {
        const url = `${this.pathUrl}/modulos/${id}`;
        return this.http.get<ModuloType[]>(url);
    }

    unidades(id: number): Observable<UnidadeType[]> {
        const url = `${this.pathUrl}/unidades/${id}`;
        return this.http.get<UnidadeType[]>(url);
    }

    valores(prm: any): Observable<ValorType[]> {
        const url = `${this.pathUrl}/valores`;
        return this.http.post<ValorType[]>(url, prm, httpOptions);
    }




}

