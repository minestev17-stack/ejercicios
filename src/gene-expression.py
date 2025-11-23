#!/usr/bin/env python3
"""
Script para filtrar genes por nivel de expresión génica.

Objetivo del programa:
1. Leer un archivo TSV con columnas: gene, expression
2. Leer un threshold desde la línea de comandos
3. Filtrar los genes cuya expresión sea >= threshold
4. Imprimir la lista de genes filtrados

El programa valida que el archivo contenga las columnas requeridas y maneja
valores de expresión numéricos, descartando aquellos que no sean válidos.
"""

import pandas as pd
import argparse  #Hecho por mi


def load_expression_table(path):
    """
    Carga un archivo TSV con columnas 'gene' y 'expression'.

    Args:
        path (str): Ruta al archivo TSV.

    Returns:
        DataFrame: DataFrame con las columnas 'gene' y 'expression'.

    Raises:
        ValueError: Si el archivo no contiene las columnas requeridas.
    """
    df = pd.read_csv(path, sep="\t")  #Hecho por mi

    if "gene" not in df.columns or "expression" not in df.columns:
        raise ValueError("El archivo debe tener columnas 'gene' y 'expression'.")

    df["expression"] = pd.to_numeric(df["expression"], errors="coerce")
    df = df.dropna(subset=["expression"])

    return df


def filter_genes(df, threshold):
    """
    Filtra genes con expresión mayor o igual al threshold.

    Args:
        df (DataFrame): DataFrame con columnas 'gene' y 'expression'.
        threshold (float): Umbral mínimo de expresión.

    Returns:
        DataFrame: Subconjunto filtrado y ordenado alfabéticamente por gen.
    """
    filtered = df[df["expression"] >= threshold]  #Hecho por mi
    filtered = filtered.sort_values("gene")

    return filtered


def build_parser():
    """
    Construye el parser de argumentos.

    Returns:
        ArgumentParser: Parser configurado con archivo y threshold.
    """
    parser = argparse.ArgumentParser(
        description="Filtra genes por expresión usando un archivo TSV y pandas."
    )

    parser.add_argument(
        "file",
        help="Archivo TSV con columnas 'gene' y 'expression'."
    )

    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.0,
        help="Umbral mínimo de expresión (ej. 10.5)."
    )

    return parser


def main():
    """
    Función principal que ejecuta el flujo de filtrado de genes.

    Realiza las siguientes operaciones:
    1. Parsea los argumentos de línea de comandos
    2. Carga la tabla de expresión génica
    3. Filtra los genes según el threshold especificado
    4. Imprime los resultados
    """
    parser = build_parser()
    args = parser.parse_args()

    df = load_expression_table(args.file)
    threshold = args.threshold

    filtered = filter_genes(df, threshold)

    if filtered.empty:
        print("No se encontraron genes por encima del threshold.")
        return

    print("Genes filtrados:")
    for gene in filtered["gene"].tolist():
        print(gene)


if __name__ == "__main__":
    main()  #Por IA
