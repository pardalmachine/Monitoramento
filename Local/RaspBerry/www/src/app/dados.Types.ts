export class BaseType {
    name: string;
    empty: boolean;
    sizeOnDisk: number;

}

export class ColecaoType {
    name: string;
}

export class MedicaoType {
    _id: string;
    Leituras: number;
    De: Date;
    Ate: Date;
}
