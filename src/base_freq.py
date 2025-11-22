#!/usr/bin/env python3
# archivo: src/base_freq.py

import argparse
import os
import sys
from typing import Tuple, Dict, List


def parse_args() -> str:
    """Parsea argumentos y devuelve la ruta al archivo FASTA.

    Mantiene el uso actual de argparse para que el script se comporte igual
    cuando se ejecuta desde la línea de comandos.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Calcula la frecuencia de A, T, G y C de un archivo FASTA con UNA sola secuencia."
        )
    )
    parser.add_argument("fasta", help="Archivo FASTA que contiene una sola secuencia.")
    args = parser.parse_args()
    return args.fasta


def read_file(path: str) -> str:
    """Lee el archivo y devuelve su contenido.

    Lanza FileNotFoundError con el mismo texto de error usado en el script original
    o IOError si ocurre un error al leer.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Error: el archivo no existe: {path}")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as e:
        raise IOError(f"Error al leer el archivo: {e}")


def validate_fasta_content(content: str) -> None:
    """Verifica que el contenido parezca un archivo FASTA.

    Lanza ValueError con el mensaje usado originalmente si la comprobación falla.
    """
    if ">" not in content:
        raise ValueError("Error: El archivo no parece estar en formato FASTA.")


def parse_first_fasta_record(content: str) -> Tuple[str, str]:
    """Extrae el primer registro FASTA y devuelve (header, raw_sequence).

    raw_sequence se devuelve en mayúsculas tal como en el script original.
    Lanza ValueError si no hay registros válidos o la secuencia está vacía.
    """
    partes = content.split(">")
    if len(partes) < 2:
        raise ValueError("Error: FASTA vacío o sin secuencia válida.")
    bloque = partes[1].strip().split("\n")
    header = bloque[0]
    sec = "".join(bloque[1:]).strip().upper()
    if len(sec) == 0:
        raise ValueError("Error: la secuencia está vacía.")
    return header, sec


def clean_sequence(seq: str, header: str) -> Tuple[str, List[str]]:
    """Filtra la secuencia conservando solo A,T,G,C (mayúsculas).

    Devuelve una tupla (secuencia_limpia, caracteres_ignorados). Además:
    - Imprime por cada caracter inválido el aviso exactamente igual que el
      script original para mantener el comportamiento CLI.
    """
    bases_validas = ["A", "T", "G", "C"]
    seq_limpia_chars: List[str] = []
    ignored: List[str] = []
    for base in seq:
        if base in bases_validas:
            seq_limpia_chars.append(base)
        else:
            ignored.append(base)
            print(f"Aviso: caracter inválido '{base}' ignorado en la secuencia '{header}'")
    return "".join(seq_limpia_chars), ignored


def calculate_base_frequencies(seq: str) -> Dict[str, int]:
    """Calcula counts por base y devuelve un diccionario con los totales.

    Llave 'total' incluye la longitud de la secuencia limpia.
    """
    return {
        "A": seq.count("A"),
        "T": seq.count("T"),
        "G": seq.count("G"),
        "C": seq.count("C"),
        "total": len(seq),
    }


def format_and_print_results(header: str, freqs: Dict[str, int]) -> None:
    """Imprime los resultados en la misma forma que el script original.

    Se asume que 'total' > 0 cuando se llama a esta función (igual que el
    comportamiento original que realizaba esta comprobación antes).
    """
    total = freqs.get("total", 0)
    a = freqs.get("A", 0)
    t = freqs.get("T", 0)
    g = freqs.get("G", 0)
    c = freqs.get("C", 0)

    print("Encabezado:", header)
    print("Longitud secuencia válida:", total)
    print("Frecuencias:")
    print("A:", a, f"({round((a/total)*100,2)}%)")
    print("T:", t, f"({round((t/total)*100,2)}%)")
    print("G:", g, f"({round((g/total)*100,2)}%)")
    print("C:", c, f"({round((c/total)*100,2)}%)")


def main() -> None:
    """Orquesta el flujo del programa y mantiene los mensajes/exit codes.

    Captura los errores lanzados por las funciones y reproduce los prints
    y sys.exit(1) del script original para no cambiar el comportamiento CLI.
    """
    try:
        ruta = parse_args()
        contenido = read_file(ruta)
        validate_fasta_content(contenido)
        header, raw_seq = parse_first_fasta_record(contenido)
        seq_limpia, _ = clean_sequence(raw_seq, header)

        if len(seq_limpia) == 0:
            print("Error: la secuencia no contiene bases válidas (A,T,G,C).")
            sys.exit(1)

        freqs = calculate_base_frequencies(seq_limpia)
        format_and_print_results(header, freqs)

    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)
    except IOError as e:
        print(str(e))
        sys.exit(1)
    except ValueError as e:
        print(str(e))
        sys.exit(1)
    except Exception as e:
        print("Error inesperado:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
