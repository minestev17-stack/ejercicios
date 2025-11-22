#!/usr/bin/env python3
"""
Juego de Piedra, Papel o Tijera (rock, paper, scissors).

Comportamiento:
- Pide al usuario que escriba "rock", "paper" o "scissors".
- Repite en un ciclo hasta que el usuario presione ENTER sin escribir nada.
- La computadora elige aleatoriamente entre las tres opciones.
- Se muestra el resultado de cada ronda. Si el usuario gana, se imprimen emojis.

El módulo usa type hints de Python 3.9+ (por ejemplo: tuple[str, str]).
"""

import random

# Lista de opciones válidas
VALID_CHOICES = ["rock", "paper", "scissors"]


def determine_result(user: str, cpu: str) -> str:
    """
    Determina el resultado desde la perspectiva del usuario.

    Args:
        user: elección del usuario ("rock", "paper" o "scissors").
        cpu: elección de la CPU ("rock", "paper" o "scissors").

    Returns:
        "win" si el usuario gana, "lose" si pierde, "draw" si empatan.
    """
    # Normalizar entradas (se espera que ya sean valores en VALID_CHOICES)
    user = user.lower()
    cpu = cpu.lower()

    if user == cpu:
        return "draw"

    # Mapeo de qué gana a qué
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}

    # Si la opción que vence a la CPU es la del usuario -> win
    if wins.get(user) == cpu:
        return "win"

    return "lose"


def play(user_choice: str) -> tuple[str, str]:
    """
    Ejecuta una ronda de juego validando la entrada del usuario.

    Args:
        user_choice: cadena con la elección del usuario.

    Returns:
        Tupla (eleccion_cpu, resultado) donde resultado es "win", "lose" o "draw".

    Raises:
        ValueError: si la elección del usuario no está en las opciones válidas.
    """
    choice = user_choice.strip().lower()

    if choice not in VALID_CHOICES:
        raise ValueError(f"Invalid choice: {user_choice!r}. Use one of: {', '.join(VALID_CHOICES)}")

    cpu_choice = random.choice(VALID_CHOICES)
    result = determine_result(choice, cpu_choice)
    return cpu_choice, result


def main() -> None:
    """
    Bucle principal del juego. Lee la elección del usuario, ejecuta rondas
    hasta que el usuario presione ENTER sin escribir nada, y muestra
    el resultado de cada ronda.
    """
    print("🎮 Rock, Paper, Scissors Game 🎮")
    print("Escribe rock, paper o scissors.")
    print("Presiona ENTER sin escribir nada para salir.")
    print("-" * 40)

    # Bucle principal del juego
    while True:
        try:
            choice = input("Tu elección > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        # Salir si presionan ENTER sin texto
        if choice == "":
            print("Saliendo. ¡Hasta luego!")
            break

        try:
            cpu_choice, result = play(choice)
        except ValueError as exc:
            print(f"Entrada inválida: {exc}")
            continue

        print(f"CPU: {cpu_choice}")
        print(f"Resultado: {result}")
        if result == "win":
            print("🎉✨🚀")
        print("-" * 40)


if __name__ == "__main__":
    main()
