import { Component, OnInit } from '@angular/core';
import { DadosService } from './dados-Service';
import { BaseType, ColecaoType, MedicaoType } from './dados.Types';
import { ChartModule } from 'primeng/primeng';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
// tslint:disable-next-line:no-unused-expression

export class AppComponent implements OnInit {
    ListaBases: BaseType[] = [];
    ListaColecoes: ColecaoType[] = [];
    ListaMedicoes: MedicaoType[] = [];
    Base: BaseType;
    Colecao: ColecaoType;
    Medicao: MedicaoType;
    De: Date;
    Ate: Date;
    Grafico: any;
    showGrafico = false;


    constructor(private dados: DadosService) { }
    ngOnInit(): void {
        this.dados.databases().subscribe(p => this.ListaBases = p);
    }

    AtuColecoes(): void {
        this.Colecao = null;
        this.Medicao = null;
        this.showGrafico = false;
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
        this.showGrafico = false;
        this.ListaMedicoes = [];
        if (this.Colecao) {
            const prm = { base: this.Base.name, colecao: this.Colecao.name };
            this.dados.medicao(prm).subscribe(p => this.ListaMedicoes = p);
        }
    }

    GeraGrafico(): void {
        this.showGrafico = false;
        const prm = {
            base: this.Base.name,
            colecao: this.Colecao.name,
            medicao: this.Medicao._id,
            de: this.De,
            ate: this.Ate
        };


        this.Grafico = {
            labels: [],
            datasets: [
                {
                    label: this.Medicao._id,
                    data: [],
                    fill: false
                }
            ]
        };


        this.dados.valores(prm).subscribe(p => {
            p.forEach(vlr => {
                // labels.push(p.Hora);
                // valores.push(p.Valor);
                this.Grafico.labels.push(vlr.Hora);
                this.Grafico.datasets[0].data.push(vlr.Valor);
                this.showGrafico = true;
            });
            // this.Grafico.datasets[0].data = valores;
        });



        /*
                this.data = {
                    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                    datasets: [
                        {
                            label: 'First Dataset',
                            data: [65, 59, 80, 81, 56, 55, 40]
                        }
                    ]
                };
        */
    }




}

