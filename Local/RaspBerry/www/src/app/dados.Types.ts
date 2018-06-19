export class SistemaType {
    Id: number;
    Nome: string;
}

export class ModuloType {
    Id: number;
    Id_Sistema: number;
    Nome: string;
}

export class UnidadeType {
    Id_Modulo: number;
    Unidade: string;
    Leituras: number;
    Inicio: Date;
    Termino: Date;
}

export class ValorType{
    Hora: Date;
    Id: number;
    Id_Modulo: number;
    Unidade: String;
    Valor: number;

}