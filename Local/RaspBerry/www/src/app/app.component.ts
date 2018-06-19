import { Component, OnInit } from '@angular/core';
import { DadosService } from './dados-Service';
import { SistemaType, ModuloType, UnidadeType } from './dados.Types';
import { ChartModule } from 'primeng/primeng';
// import { listener } from '@angular/core/src/render3/instructions';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html'
})


export class AppComponent implements OnInit {
    ListaSistemas: SistemaType[] = [];
    ListaModulos: ModuloType[] = [];
    ListaUnidades: UnidadeType[] = [];

    Sistema: SistemaType;
    Modulo: ModuloType;
    Unidade: UnidadeType;
    De: Date;
    Ate: Date;
    Grafico: any;
    showGrafico = false;


    constructor(private dados: DadosService) { }
    ngOnInit(): void {
        this.dados.sistemas().subscribe(p => this.ListaSistemas = p);
    }

    AtuModulos(): void {
        this.Modulo = null;
        this.Unidade = null;
        this.showGrafico = false;
        this.ListaModulos = [];

        if (this.Sistema) {
            this.dados.modulos(this.Sistema.Id).subscribe(p => this.ListaModulos = p);
        } else {
            this.ListaModulos = [];
        }
    }

    AtuUnidades(): void {
        this.Unidade = null;
        this.showGrafico = false;
        this.ListaUnidades = [];
        if (this.Modulo) {
            this.dados.unidades(this.Modulo.Id).subscribe(p => this.ListaUnidades = p);
        }
    }

    GeraGrafico(): void {
        this.showGrafico = false;
        const prm = {
            modulo: this.Modulo.Id,
            unidade: this.Unidade.Unidade,
            de: this.De,
            ate: this.Ate
        };


        this.Grafico = {
            labels: [],
            datasets: [
                {
                    label: this.Unidade.Unidade,
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

