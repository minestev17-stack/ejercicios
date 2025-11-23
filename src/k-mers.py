#!/usr/bin/env python3
"""kmer_counter.py

Command-line k-mer counter for DNA sequences.

Requirements implemented:
- Uses argparse with a positional sequence argument and an option -k/--kmer_size.
- Validates that the sequence only contains A, T, C, G (case-insensitive).
- Validates that the sequence is not empty and that k is > 0 and <= len(sequence).
- Counts contiguous k-mers of length k using a dictionary.
- Prints results in the format: kmer<TAB>count

Example:
    python kmer_counter.py ATGCGTAC -k 3

Author: PyLIA
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

VALID_NUCLEOTIDES = set("ATCG")


def validate_sequence(seq: str) -> str:
    """Validate and normalize a DNA sequence.

    Converts the input sequence to upper case and checks that it is non-empty
    and contains only the characters A, T, C and G.

    Parameters
    ----------
    seq : str
        Input DNA sequence (may be lower/upper case).

    Returns
    -------
    str
        Upper-cased validated sequence.

    Raises
    ------
    ValueError
        If the sequence is empty or contains invalid characters.
    """
    if seq is None:
        raise ValueError("No sequence provided.")

    seq = seq.strip().upper()

    if len(seq) == 0:
        raise ValueError("Sequence is empty.")

    invalid = set(seq) - VALID_NUCLEOTIDES
    if invalid:
        invalid_chars = ",".join(sorted(invalid))
        raise ValueError(f"Invalid character(s) in sequence: {invalid_chars}. Only A,T,C,G allowed.")

    return seq


def count_kmers(seq: str, k: int) -> Dict[str, int]:
    """Count contiguous k-mers of length k in a DNA sequence.

    Parameters
    ----------
    seq : str
        Validated DNA sequence (upper case, only A/T/C/G).
    k : int
        k-mer size (must be > 0 and <= len(seq)).

    Returns
    -------
    Dict[str, int]
        Dictionary mapping k-mer -> count.

    Raises
    ------
    ValueError
        If k is not a positive integer or if k > len(seq).
    """
    if not isinstance(k, int):
        raise ValueError("k must be an integer.")

    if k <= 0:
        raise ValueError("k must be a positive integer greater than 0.")

    seqlen = len(seq)
    if k > seqlen:
        raise ValueError("k is larger than the length of the sequence.")

    counts: Dict[str, int] = {}
    limit = seqlen - k + 1
    for i in range(limit):
        kmer = seq[i : i + k]
        counts[kmer] = counts.get(kmer, 0) + 1

    return counts


def build_parser() -> argparse.ArgumentParser:
    """Create and return the argparse.ArgumentParser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="kmer_counter",
        description="Count contiguous k-mers in a DNA sequence (A,T,C,G).",
    )

    parser.add_argument(
        "sequence",
        metavar="SEQUENCE",
        type=str,
        help="DNA sequence (only A, T, C, G are allowed).",
    )

    parser.add_argument(
        "-k",
        "--kmer_size",
        dest="k",
        type=int,
        required=True,
        help="k-mer size (positive integer).",
    )

    return parser


def main(argv: list[str] | None = None) -> None:
    """Main entry point for the CLI.

    Parameters
    ----------
    argv : list[str] | None
        Optional list of arguments for testing. If None, uses sys.argv[1:].
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        seq = validate_sequence(args.sequence)
        counts = count_kmers(seq, args.k)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    # Print sorted by k-mer for stable output
    for kmer in sorted(counts.keys()):
        print(f"{kmer}\t{counts[kmer]}")


if __name__ == "__main__":
    main()
