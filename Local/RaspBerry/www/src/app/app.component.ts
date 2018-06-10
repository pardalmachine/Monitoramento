import { Component, OnInit } from '@angular/core';
import { DadosService } from './dados-Service';
import { BaseType, ColecaoType, MedicaoType } from './dados.Types';
@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
    ListaBases: BaseType[] = [];
    ListaColecoes: ColecaoType[] = [];
    ListaMedicoes: MedicaoType[] = [];
    Base: BaseType;
    Colecao: ColecaoType;
    Medicao: MedicaoType;
    De: Date;
    Ate: Date;
    constructor(private dados: DadosService) { }
    ngOnInit(): void {
        this.dados.databases().subscribe(p => this.ListaBases = p);
    }

    AtuColecoes(): void {
        this.Colecao = null;
        this.Medicao = null;
        this.ListaColecoes = [];
        if (this.Base) {
            const prm = { base: this.Base.name };
            this.dados.collections(prm).subscribe(p => this.ListaColecoes = p);
        } else {
            this.ListaColecoes = [];
        }
    }

    AtuMedicoes(): void {
        this.Medicao = null;
        this.ListaMedicoes = [];
        if (this.Colecao) {
            const prm = { base: this.Base.name, colecao: this.Colecao.name };
            this.dados.medicao(prm).subscribe(p => this.ListaMedicoes = p);
        }
    }

    GeraGrafico(): void {

        const prm = {
            base: this.Base.name,
            colecao: this.Colecao.name,
            medicao: this.Medicao._id,
            de: this.De,
            ate: this.Ate
        };
        this.dados.valores(prm).subscribe(p => this.ListaMedicoes = p);


    }
}
